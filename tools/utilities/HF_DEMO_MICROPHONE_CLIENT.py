import asyncio
import base64
import os
import queue
import threading
import time
import uuid
from typing import AsyncIterator
import difflib

import gradio as gr
import numpy as np

from mistralai import Mistral
from mistralai.extra.realtime import UnknownRealtimeEvent
from mistralai.models import (
    AudioFormat,
    RealtimeTranscriptionError,
    RealtimeTranscriptionSessionCreated,
    TranscriptionStreamDone,
    TranscriptionStreamTextDelta,
)

# Load Voxtral icon as base64
VOXTRAL_ICON_B64 = ""
icon_path = os.path.join(os.path.dirname(__file__), "assets", "voxtral.png")
if os.path.exists(icon_path):
    with open(icon_path, "rb") as f:
        VOXTRAL_ICON_B64 = base64.b64encode(f.read()).decode("utf-8")

SAMPLE_RATE = 16_000
WARMUP_DURATION = 2.0  # seconds of silence for warmup
WPM_WINDOW = 10  # seconds for running mean calculation
CALIBRATION_PERIOD = 5  # seconds before showing WPM
SESSION_TIMEOUT = int(os.environ.get("SESSION_TIMEOUT", "95"))      # Max 90s per session
INACTIVITY_TIMEOUT = int(os.environ.get("INACTIVITY_TIMEOUT", "10"))  # Close after 10s silence
MAX_CONCURRENT_SESSIONS = int(os.environ.get("MAX_SESSIONS", "50"))

# Global config (shared across users)
MISTRAL_BASE_URL = "wss://api.mistral.ai"
MODEL = "voxtral-mini-transcribe-realtime-2602"
_MODEL = "mistralai/Voxtral-Mini-4B-Realtime-2602"

# Global event loop for all websocket connections (runs in single background thread)
_event_loop = None
_loop_thread = None
_loop_lock = threading.Lock()

# Track active sessions for resource management
_active_sessions = {}
_sessions_lock = threading.Lock()

# Global session registry - sessions are stored here and looked up by ID
_session_registry = {}
_registry_lock = threading.Lock()
_last_cleanup = time.time()
SESSION_REGISTRY_CLEANUP_INTERVAL = 90  # seconds
SESSION_MAX_AGE = 90  # 90 seconds - remove sessions older than this

DEFAULT_API_KEY = os.environ.get("DEFAULT_API_KEY", "")

def get_or_create_session(session_id: str = None) -> "UserSession":
    """Get existing session by ID or create a new one."""
    global _last_cleanup
    
    # Periodic cleanup of stale sessions
    now = time.time()
    if now - _last_cleanup > SESSION_REGISTRY_CLEANUP_INTERVAL:
        _cleanup_stale_sessions()
        _last_cleanup = now
    
    with _registry_lock:
        if session_id and session_id in _session_registry:
            session = _session_registry[session_id]
            # Validate the session is actually a UserSession instance
            if isinstance(session, UserSession):
                session._last_accessed = now
                return session
            else:
                # Corrupted registry entry - remove and create new
                print(f"WARNING: Corrupted session registry entry for {session_id}: {type(session)}")
                del _session_registry[session_id]
        
        # Create new session
        session = UserSession()
        session._last_accessed = now
        _session_registry[session.session_id] = session
        return session


def _cleanup_stale_sessions():
    """Remove sessions that haven't been accessed recently."""
    now = time.time()
    to_remove_from_registry = []
    to_remove_from_active = []
    
    # Need both locks to safely check both dictionaries
    with _registry_lock:
        with _sessions_lock:
            # Find stale sessions in registry
            for session_id, session in _session_registry.items():
                # NEVER remove if still in active_sessions (websocket still running)
                if session_id in _active_sessions:
                    continue
                    
                last_accessed = getattr(session, '_last_accessed', 0)
                # Remove if: not running AND not active AND old
                if not session.is_running and (now - last_accessed > SESSION_MAX_AGE):
                    to_remove_from_registry.append(session_id)
            
            # Find orphaned sessions in active_sessions (not in registry anymore)
            for session_id, session in list(_active_sessions.items()):
                if session_id not in _session_registry:
                    # Orphaned - mark for removal
                    if not session.is_running:
                        to_remove_from_active.append(session_id)
            
            # Clean up registry
            for session_id in to_remove_from_registry:
                _session_registry.pop(session_id, None)
            
            # Clean up orphaned active sessions
            for session_id in to_remove_from_active:
                _active_sessions.pop(session_id, None)
            
            active_count = len(_active_sessions)
            registry_count = len(_session_registry)
    
    total_cleaned = len(to_remove_from_registry) + len(to_remove_from_active)
    if total_cleaned > 0:
        print(f"Cleaned up {len(to_remove_from_registry)} stale + {len(to_remove_from_active)} orphaned sessions. Registry: {registry_count}, Active: {active_count}")


def cleanup_session(session_id: str):
    """Remove session from registry."""
    with _registry_lock:
        _session_registry.pop(session_id, None)


def kill_all_sessions():
    """Emergency cleanup - kill ALL active sessions to free capacity."""
    killed_count = 0
    
    with _sessions_lock:
        sessions_to_kill = list(_active_sessions.values())
    
    for session in sessions_to_kill:
        try:
            session.is_running = False
            session._stopped_by_user = True
            
            # Signal stop event
            if session._stop_event is not None:
                loop = get_event_loop()
                try:
                    asyncio.run_coroutine_threadsafe(
                        _set_stop_event_sync(session._stop_event), loop
                    )
                except Exception:
                    pass
                session._stop_event = None
            
            # Cancel the task
            if session._task is not None:
                session._task.cancel()
                session._task = None
            
            killed_count += 1
        except Exception as e:
            print(f"Error killing session {session.session_id[:8]}: {e}")
    
    # Clear both dictionaries
    with _registry_lock:
        with _sessions_lock:
            _active_sessions.clear()
            _session_registry.clear()
    
    print(f"CAPACITY RESET: Killed {killed_count} sessions. All sessions cleared.")


async def _set_stop_event_sync(event):
    """Helper to set asyncio event."""
    event.set()


def get_event_loop():
    """Get or create the shared event loop."""
    global _event_loop, _loop_thread
    with _loop_lock:
        if _event_loop is None or not _event_loop.is_running():
            _event_loop = asyncio.new_event_loop()
            _loop_thread = threading.Thread(target=_run_event_loop, daemon=True)
            _loop_thread.start()
            # Wait for loop to start
            time.sleep(0.1)
    return _event_loop


def _run_event_loop():
    """Run the event loop in background thread."""
    asyncio.set_event_loop(_event_loop)
    _event_loop.run_forever()


class UserSession:
    """Per-user session state."""
    def __init__(self, api_key: str = ""):
        self.session_id = str(uuid.uuid4())
        self.api_key = api_key
        self.partial_transcript_enabled = False  # Default to disabled
        # Use a thread-safe queue for cross-thread communication
        self._audio_queue = queue.Queue(maxsize=200)
        self.transcription_tuple = ("", "", "")  # For 3 streams
        self.is_running = False
        self.status_message = "ready"
        self.word_timestamps = []
        self.current_wpm = "Calibrating..."
        self.session_start_time = None
        self.last_audio_time = None
        self._start_lock = threading.Lock()
        self._task = None  # Track the async task
        self._stop_event = None  # Event to signal stop
        self._stopped_by_user = False  # Track if user explicitly stopped
        self.new_color_open = '<span style="color: #FFA500";>'
        self.new_color_close = "</span>"
        
        # Enhanced event tracking
        self.stream_events = {
            'stream_1': [],  # List of (timestamp, event_type, event_data) tuples
            'stream_2': []   # List of (timestamp, event_type, event_data) tuples
        }
        self.last_event_timestamp = None
    
    @property
    def audio_queue(self):
        """Return the thread-safe queue."""
        return self._audio_queue
    
    def reset_queue(self):
        """Reset the audio queue."""
        self._audio_queue = queue.Queue(maxsize=200)
    
    def get_event_summary(self):
        """Get a summary of all stream events with timestamps."""
        summary = {
            'stream_1': [],
            'stream_2': [],
            'stats': {
                'stream_1_count': len(self.stream_events['stream_1']),
                'stream_2_count': len(self.stream_events['stream_2']),
                'last_event_time': self.last_event_timestamp,
                'total_events': len(self.stream_events['stream_1']) + len(self.stream_events['stream_2'])
            }
        }
        
        for stream_name in ['stream_1', 'stream_2']:
            for event in self.stream_events[stream_name]:
                summary[stream_name].append({
                    'timestamp': event.get('timestamp', 0),
                    'type': event.get('type', 'unknown'),
                    'data': {k: v for k, v in event.items() if k not in ['timestamp', 'type']}
                })
        
        return summary
    
    def clear_events(self):
        """Clear all event history."""
        self.stream_events = {
            'stream_1': [],
            'stream_2': []
        }
        self.last_event_timestamp = None
        self.transcription_tuple = ("", "", "")

    @staticmethod
    def _normalize_word(word: str) -> str:
        return word.strip(".,!?;:\"'()[]{}").lower()
    
    def _compute_display_texts(self, slow_text, fast_text) -> tuple[str, str]:
        slow_words = slow_text.split()
        fast_words = fast_text.split()

        if not slow_words:
            partial_text = f" {fast_text}".rstrip()
            return "", partial_text

        slow_norm = [self._normalize_word(word) for word in slow_words]
        fast_norm = [self._normalize_word(word) for word in fast_words]

        matcher = difflib.SequenceMatcher(None, slow_norm, fast_norm)
        last_fast_index = 0
        slow_progress = 0
        for block in matcher.get_matching_blocks():
            if block.size == 0:
                continue
            slow_end = block.a + block.size
            if slow_end > slow_progress:
                slow_progress = slow_end
                last_fast_index = block.b + block.size

        if last_fast_index < len(fast_words):
            ahead_words = fast_words[last_fast_index:]
            partial_text = " " + " ".join(ahead_words) if ahead_words else ""
        else:
            partial_text = ""

        return slow_text, partial_text

    def reconstruct_transcription(self):
        """Reconstruct transcription text from stream events."""
        stream1_text = ""
        stream2_text = ""
    
        # Reconstruct from text_delta events
        for event in self.stream_events['stream_1']:
            if event.get('type') == 'text_delta':
                stream1_text += event.get('text', '')
    
        # Only reconstruct Stream 2 if partial_transcript_enabled is True
        if self.partial_transcript_enabled:
            for event in self.stream_events['stream_2']:
                if event.get('type') == 'text_delta':
                    stream2_text += event.get('text', '')
    
        # If partial_transcript_enabled is False, just return Stream 1 for all streams
        if not self.partial_transcript_enabled:
            return (stream1_text, "", stream1_text)
    
        # Stream 3 (merged)
        stream3_final = stream2_text
        stream3_preview = stream1_text
    
        stream3_final, stream3_preview = self._compute_display_texts(stream3_final, stream3_preview)
        stream3_text = stream3_final + self.new_color_open + stream3_preview + self.new_color_close
    
        # Return as tuple for compatibility with HTML function
        return (stream1_text, stream2_text, stream3_text)

# Load CSS from external file
css_path = os.path.join(os.path.dirname(__file__), "style.css")
with open(css_path, "r") as f:
    CUSTOM_CSS = f.read()


def get_header_html() -> str:
    """Generate the header HTML with Voxtral logo."""
    if VOXTRAL_ICON_B64:
        logo_html = f'<img src="data:image/png;base64,{VOXTRAL_ICON_B64}" alt="Voxtral" class="header-logo" />'
    else:
        logo_html = ''
    
    return f"""
    <div class="header-card">
        <h1 class="header-title">{logo_html}Real-time Speech Transcription</h1>
        <p class="header-subtitle">Enter your Mistral API key below, then click the microphone to start streaming transcriptions.</p>
        <p class="header-subtitle">Talk naturally. Talk fast. Talk ridiculously fast. I can handle it.</p>
    </div>
    """


def get_status_html(status: str) -> str:
    """Generate status badge HTML based on current status."""
    status_configs = {
        "ready": ("STANDBY", "status-ready", ""),
        "connecting": ("CONNECTING", "status-connecting", "fast"),
        "warming": ("WARMING UP", "status-warming", "fast"),
        "listening": ("LISTENING", "status-listening", "animate"),
        "timeout": ("TIMEOUT", "status-timeout", ""),
        "error": ("ERROR", "status-error", ""),
    }
    label, css_class, dot_class = status_configs.get(status, status_configs["ready"])
    dot_anim = f" {dot_class}" if dot_class else ""
    
    return f"""<div class="status-badge {css_class}"><span class="status-dot{dot_anim}"></span><span style="color: inherit !important;">{label}</span></div>"""


def get_transcription_html(transcripts: tuple, status: str, wpm: str = "Calibrating...", partial_transcript_enabled: bool = False) -> str:
    """Generate the full transcription card HTML."""
    status_badge = get_status_html(status)
    wpm_badge = f'<div class="wpm-badge"><span style="color: #1E1E1E !important;">{wpm}</span></div>'

    if transcripts:
        # If partial_transcript_enabled is False, only show Stream 1
        if not partial_transcript_enabled:
            stream1_content = transcripts[0]
            cursor_html = '<span class="transcript-cursor"></span>' if status == "listening" else ""
            content_html = f"""
            <div class="transcript-text" style="color: #000000 !important;">
{stream1_content}{cursor_html}
            </div>
            """
        else:
            # Show all streams if partial_transcript_enabled is True
            if len(transcripts) >= 3 and transcripts[0] and transcripts[1] and transcripts[2]:
                # Split into three streams
                stream1_content, stream2_content, stream3_content = transcripts

                cursor_html = '<span class="transcript-cursor"></span>' if status == "listening" else ""
                content_html = f"""
                <div class="triple-stream-container">
                    <div class="stream-box">
                        <div class="stream-label">Stream 1 (Preview - 240ms)</div>
                        <div class="transcript-text" style="color: #000000 !important;">
{stream1_content}{cursor_html}
                        </div>
                    </div>
                    <div class="stream-box">
                        <div class="stream-label">Stream 2 (Final - 2.4s)</div>
                        <div class="transcript-text" style="color: #000000 !important;">
{stream2_content}{cursor_html}
                        </div>
                    </div>
                    <div class="stream-box">
                        <div class="stream-label">Stream 3 (Merged)</div>
                        <div class="transcript-text" style="color: #000000 !important;">
{stream3_content}{cursor_html}
                        </div>
                    </div>
                </div>
                """
            elif len(transcripts) >= 3 and transcripts[0] and transcripts[1] and transcripts[2]:
                # Show only the merged stream when partial transcript is disabled
                stream3_content = transcripts[2]

                cursor_html = '<span class="transcript-cursor"></span>' if status == "listening" else ""
                content_html = f"""
                <div class="transcript-text" style="color: #000000 !important;">
{stream3_content}{cursor_html}
                </div>
                """
            elif transcripts[0] and transcripts[1]:
                # Split the transcript into two streams
                stream1_content, stream2_content = transcripts

                cursor_html = '<span class="transcript-cursor"></span>' if status == "listening" else ""
                content_html = f"""
                <div class="dual-stream-container">
                    <div class="stream-box">
                        <div class="stream-label">Stream 1</div>
                        <div class="transcript-text" style="color: #000000 !important;">
{stream1_content}{cursor_html}
                        </div>
                    </div>
                    <div class="stream-box">
                        <div class="stream-label">Stream 2</div>
                        <div class="transcript-text" style="color: #000000 !important;">
{stream2_content}{cursor_html}
                        </div>
                    </div>
                </div>
                """
            else:
                # Single stream (backward compatibility)
                cursor_html = '<span class="transcript-cursor"></span>' if status == "listening" else ""
                content_html = f"""
                <div class="transcript-text" style="color: #000000 !important;">
{transcripts[0]}{cursor_html}
                </div>
                """
    elif status in ["listening", "warming", "connecting"]:
        content_html = """
        <div class="empty-state">
            <div class="empty-dots">
                <div class="empty-dot"></div>
                <div class="empty-dot"></div>
                <div class="empty-dot"></div>
            </div>
            <p class="empty-text" style="color: #555555 !important;">Listening for audio...</p>
        </div>
        """
    elif status == "timeout":
        content_html = """
        <div class="empty-state">
            <p class="empty-text" style="color: #B30400 !important;">Session timeout (5 minutes)</p>
            <p class="empty-text" style="color: #555555 !important;">Click 'Clear History' and refresh to restart.</p>
        </div>
        """
    else:
        content_html = """
        <div class="empty-state">
            <p class="empty-text" style="color: #555555 !important;">// Awaiting audio input...</p>
            <p class="empty-text" style="color: #555555 !important;">// Click the microphone to start.</p>
        </div>
        """

    # Use base64 image if available
    if VOXTRAL_ICON_B64:
        icon_html = f'<img src="data:image/png;base64,{VOXTRAL_ICON_B64}" alt="Voxtral" class="voxtral-icon" />'
    else:
        icon_html = '<span style="font-size:20px;">🎙️</span>'

    return f"""
    <div class="transcription-card">
        <div class="card-header">
            <div class="card-header-left">
                {icon_html}
                <span class="card-title" style="color: #1E1E1E !important;">Transcription Output</span>
            </div>
            <div class="card-header-right">
                {wpm_badge}
                {status_badge}
            </div>
        </div>
        <div class="card-content">
            {content_html}
        </div>
        <div class="card-footer">
            <span style="color: #555555 !important;">Voxtral Mini</span>
            <span style="color: #555555 !important;">Real-time Audio Transcription</span>
        </div>
    </div>
    """


def calculate_wpm(session):
    """Calculate words per minute based on running mean of last WPM_WINDOW seconds."""
    if session.session_start_time is not None:
        elapsed = time.time() - session.session_start_time
        if elapsed < CALIBRATION_PERIOD:
            return "Calibrating..."
    
    if len(session.word_timestamps) < 2:
        return "0.0 WPM"
    
    current_time = time.time()
    cutoff_time = current_time - WPM_WINDOW
    session.word_timestamps = [ts for ts in session.word_timestamps if ts >= cutoff_time]
    
    if len(session.word_timestamps) < 2:
        return "0.0 WPM"
    
    time_span = current_time - session.word_timestamps[0]
    if time_span == 0:
        return "0.0 WPM"
    
    word_count = len(session.word_timestamps)
    wpm = (word_count / time_span) * 60
    return f"{round(wpm, 1)} WPM"


async def audio_stream_from_queue(session) -> AsyncIterator[bytes]:
    """Async generator that yields audio bytes from the session queue."""
    # First, send silence for warmup
    session.status_message = "warming"
    num_samples = int(SAMPLE_RATE * WARMUP_DURATION)
    silence = np.zeros(num_samples, dtype=np.int16)
    chunk_size = int(SAMPLE_RATE * 0.1)  # 100ms chunks
    
    for i in range(0, num_samples, chunk_size):
        if not session.is_running:
            return
        chunk = silence[i:i + chunk_size]
        yield chunk.tobytes()
        await asyncio.sleep(0.05)
    
    session.status_message = "listening"
    
    # Then stream real audio from the queue
    while session.is_running:
        # Check for inactivity timeout
        if session.last_audio_time is not None:
            idle = time.time() - session.last_audio_time
            if idle >= INACTIVITY_TIMEOUT:
                session.is_running = False
                session.status_message = "ready"
                return
        
        # Check for session timeout
        if session.session_start_time is not None:
            elapsed = time.time() - session.session_start_time
            if elapsed >= SESSION_TIMEOUT:
                session.is_running = False
                session.status_message = "timeout"
                return
        
        # Check if stop was requested
        if session._stop_event and session._stop_event.is_set():
            return
        
        # Get audio from queue
        try:
            # The queue contains base64-encoded PCM16 audio
            b64_chunk = session.audio_queue.get_nowait()
            # Decode base64 to raw bytes
            audio_bytes = base64.b64decode(b64_chunk)
            yield audio_bytes
        except queue.Empty:
            # No audio available, yield control briefly
            await asyncio.sleep(0.05)
            continue


class AudioStreamDuplicator:
    """Duplicates an audio stream so it can be consumed by multiple consumers."""
    
    def __init__(self, session):
        self.session = session
        self.consumers = []
        self.buffer = []
        self.consumer_positions = {}  # Track position for each consumer
        self.lock = asyncio.Lock()
        
    async def add_consumer(self):
        """Add a new consumer to the duplicator."""
        consumer_id = len(self.consumers)
        self.consumers.append(consumer_id)
        self.consumer_positions[consumer_id] = 0  # Start at beginning
        return self._create_consumer_stream(consumer_id)
    
    async def _create_consumer_stream(self, consumer_id):
        """Create a stream for a specific consumer."""
        # First yield warmup silence for this consumer
        num_samples = int(SAMPLE_RATE * WARMUP_DURATION)
        silence = np.zeros(num_samples, dtype=np.int16)
        chunk_size = int(SAMPLE_RATE * 0.1)  # 100ms chunks
        
        for i in range(0, num_samples, chunk_size):
            if not self.session.is_running:
                return
            chunk = silence[i:i + chunk_size]
            yield chunk.tobytes()
            await asyncio.sleep(0.05)
        
        # Then stream from the shared buffer
        while self.session.is_running:
            # Check for inactivity timeout
            if self.session.last_audio_time is not None:
                idle = time.time() - self.session.last_audio_time
                if idle >= INACTIVITY_TIMEOUT:
                    self.session.is_running = False
                    self.session.status_message = "ready"
                    return
            
            # Check for session timeout
            if self.session.session_start_time is not None:
                elapsed = time.time() - self.session.session_start_time
                if elapsed >= SESSION_TIMEOUT:
                    self.session.is_running = False
                    self.session.status_message = "timeout"
                    return
            
            # Check if stop was requested
            if self.session._stop_event and self.session._stop_event.is_set():
                return
            
            # Get audio from the shared buffer - each consumer gets all chunks
            async with self.lock:
                position = self.consumer_positions[consumer_id]
                if position < len(self.buffer):
                    audio_bytes = self.buffer[position]
                    self.consumer_positions[consumer_id] += 1
                    yield audio_bytes
                else:
                    # No audio available, yield control briefly
                    await asyncio.sleep(0.05)
                    continue


async def audio_stream_duplicator_from_queue(session):
    """Create a duplicator that can serve multiple audio streams."""
    duplicator = AudioStreamDuplicator(session)
    
    # Start a background task to fill the buffer from the queue
    async def fill_buffer():
        while session.is_running:
            try:
                # The queue contains base64-encoded PCM16 audio
                b64_chunk = session.audio_queue.get_nowait()
                # Decode base64 to raw bytes
                audio_bytes = base64.b64decode(b64_chunk)
                
                async with duplicator.lock:
                    # Add to buffer - all consumers will get this chunk
                    duplicator.buffer.append(audio_bytes)
            except queue.Empty:
                # No audio available, yield control briefly
                await asyncio.sleep(0.05)
                continue
    
    # Start the buffer filler task
    asyncio.create_task(fill_buffer())
    
    return duplicator

async def mistral_transcription_handler(session):
    """Connect to Mistral realtime API and handle transcription with 1 or 2 parallel streams."""
    try:
        if not session.api_key:
            session.status_message = "error"
            print(f"Session {session.session_id[:8]}: No API key provided")
            return

        # Create Mistral client
        client = Mistral(api_key=session.api_key, server_url=MISTRAL_BASE_URL)
        audio_format = AudioFormat(encoding="pcm_s16le", sample_rate=SAMPLE_RATE)

        session.status_message = "connecting"

        print(f"Session {session.session_id[:8]}: Connecting to Mistral realtime API...")

        # Create a duplicator that can serve multiple audio streams
        duplicator = await audio_stream_duplicator_from_queue(session)
        print(f"Session {session.session_id[:8]}: Created audio stream duplicator for parallel processing")

        # Always create Stream 1 (fast, 240ms delay)
        audio_stream_1 = await duplicator.add_consumer()
        print(f"Session {session.session_id[:8]}: Created Stream 1 (240ms delay)")

        # Only create Stream 2 if partial_transcript_enabled is True
        audio_stream_2 = None
        if session.partial_transcript_enabled:
            audio_stream_2 = await duplicator.add_consumer()
            print(f"Session {session.session_id[:8]}: Created Stream 2 (2400ms delay)")

        # Create tasks for transcription streams
        async def process_stream_1():
            async for event_1 in client.audio.realtime.transcribe_stream(
                audio_stream=audio_stream_1,
                model=MODEL,
                audio_format=audio_format,
                target_streaming_delay_ms=240 if session.partial_transcript_enabled else 480
            ):
                if not session.is_running:
                    break

                current_time = time.time()

                if isinstance(event_1, RealtimeTranscriptionSessionCreated):
                    event_data = {
                        'type': 'session_created',
                        'timestamp': current_time,
                        'session_id': event_1.session_id if hasattr(event_1, 'session_id') else None
                    }
                    session.stream_events['stream_1'].append(event_data)
                    session.last_event_timestamp = current_time
                    print(f"Session {session.session_id[:8]}: Stream 1 connected to Mistral - {current_time:.3f}")

                elif isinstance(event_1, TranscriptionStreamTextDelta):
                    delta = event_1.text

                    # Get current full text by reconstructing from events
                    current_full_text = ""
                    for e in session.stream_events['stream_1']:
                        if e.get('type') == 'text_delta':
                            current_full_text += e.get('text', '')
                    current_full_text += delta

                    event_data = {
                        'type': 'text_delta',
                        'timestamp': current_time,
                        'text': delta,
                        'full_text': current_full_text
                    }
                    session.stream_events['stream_1'].append(event_data)
                    session.last_event_timestamp = current_time

                    words = delta.split()
                    for _ in words:
                        session.word_timestamps.append(time.time())

                    session.current_wpm = calculate_wpm(session)

                elif isinstance(event_1, TranscriptionStreamDone):
                    event_data = {
                        'type': 'stream_done',
                        'timestamp': current_time
                    }
                    session.stream_events['stream_1'].append(event_data)
                    session.last_event_timestamp = current_time
                    print(f"Session {session.session_id[:8]}: Stream 1 transcription done - {current_time:.3f}")
                    break

                elif isinstance(event_1, RealtimeTranscriptionError):
                    event_data = {
                        'type': 'error',
                        'timestamp': current_time,
                        'error': str(event_1.error)
                    }
                    session.stream_events['stream_1'].append(event_data)
                    session.last_event_timestamp = current_time
                    print(f"Session {session.session_id[:8]}: Stream 1 error - {event_1.error} - {current_time:.3f}")
                    break

                elif isinstance(event_1, UnknownRealtimeEvent):
                    event_data = {
                        'type': 'unknown_event',
                        'timestamp': current_time,
                        'event': str(event_1)
                    }
                    session.stream_events['stream_1'].append(event_data)
                    session.last_event_timestamp = current_time
                    continue  # Ignore unknown events

        async def process_stream_2():
            # Only process Stream 2 if it exists and partial_transcript_enabled is True
            if not session.partial_transcript_enabled or audio_stream_2 is None:
                return

            async for event_2 in client.audio.realtime.transcribe_stream(
                audio_stream=audio_stream_2,
                model=MODEL,
                audio_format=audio_format,
                target_streaming_delay_ms=2400
            ):
                if not session.is_running:
                    break

                current_time = time.time()

                if isinstance(event_2, RealtimeTranscriptionSessionCreated):
                    event_data = {
                        'type': 'session_created',
                        'timestamp': current_time,
                        'session_id': event_2.session_id if hasattr(event_2, 'session_id') else None
                    }
                    session.stream_events['stream_2'].append(event_data)
                    session.last_event_timestamp = current_time
                    print(f"Session {session.session_id[:8]}: Stream 2 connected to Mistral - {current_time:.3f}")

                elif isinstance(event_2, TranscriptionStreamTextDelta):
                    delta = event_2.text

                    # Get current full text by reconstructing from events
                    current_full_text = ""
                    for e in session.stream_events['stream_2']:
                        if e.get('type') == 'text_delta':
                            current_full_text += e.get('text', '')
                    current_full_text += delta

                    event_data = {
                        'type': 'text_delta',
                        'timestamp': current_time,
                        'text': delta,
                        'full_text': current_full_text
                    }
                    session.stream_events['stream_2'].append(event_data)
                    session.last_event_timestamp = current_time

                    session.current_wpm = calculate_wpm(session)

                elif isinstance(event_2, TranscriptionStreamDone):
                    event_data = {
                        'type': 'stream_done',
                        'timestamp': current_time
                    }
                    session.stream_events['stream_2'].append(event_data)
                    session.last_event_timestamp = current_time
                    print(f"Session {session.session_id[:8]}: Stream 2 transcription done - {current_time:.3f}")
                    break

                elif isinstance(event_2, RealtimeTranscriptionError):
                    event_data = {
                        'type': 'error',
                        'timestamp': current_time,
                        'error': str(event_2.error)
                    }
                    session.stream_events['stream_2'].append(event_data)
                    session.last_event_timestamp = current_time
                    print(f"Session {session.session_id[:8]}: Stream 2 error - {event_2.error} - {current_time:.3f}")
                    break

                elif isinstance(event_2, UnknownRealtimeEvent):
                    event_data = {
                        'type': 'unknown_event',
                        'timestamp': current_time,
                        'event': str(event_2)
                    }
                    session.stream_events['stream_2'].append(event_data)
                    session.last_event_timestamp = current_time
                    continue  # Ignore unknown events

        # Run Stream 1 always
        stream1_task = asyncio.create_task(process_stream_1())

        # Run Stream 2 only if partial_transcript_enabled is True
        stream2_task = None
        if session.partial_transcript_enabled:
            stream2_task = asyncio.create_task(process_stream_2())

        # Wait for streams to complete
        if stream2_task:
            await asyncio.gather(stream1_task, stream2_task)
        else:
            await stream1_task

        # Final transcription is already reconstructed from events
        # Just add stats to the display
        event_summary = session.get_event_summary()
        stats_text = f"Events: {event_summary['stats']['total_events']} (S1: {event_summary['stats']['stream_1_count']}, S2: {event_summary['stats']['stream_2_count']})"

        # Store the reconstructed transcription as tuple
        session.transcription_tuple = session.reconstruct_transcription()

    except asyncio.CancelledError:
        pass  # Normal cancellation
    except Exception as e:
        error_msg = str(e) if str(e) else type(e).__name__
        if "ConnectionReset" not in error_msg and "CancelledError" not in error_msg:
            print(f"Session {session.session_id[:8]}: Mistral API error - {error_msg}")
        session.status_message = "error"
    finally:
        session.is_running = False

        # Only remove and log if not already handled by stop_session
        if not session._stopped_by_user:
            with _sessions_lock:
                removed = _active_sessions.pop(session.session_id, None)
                active_count = len(_active_sessions)
            if removed:
                print(f"Session {session.session_id[:8]} ended. Active sessions: {active_count}")

def start_transcription(session):
    """Start Mistral transcription using the shared event loop."""
    session.is_running = True
    session._stop_event = asyncio.Event()
    
    # Register this session
    with _sessions_lock:
        _active_sessions[session.session_id] = session
        active_count = len(_active_sessions)
    
    print(f"Starting session {session.session_id[:8]}. Active sessions: {active_count}")
    
    # Submit to the shared event loop
    loop = get_event_loop()
    future = asyncio.run_coroutine_threadsafe(mistral_transcription_handler(session), loop)
    session._task = future
    
    # Don't block - the coroutine runs in the background
    # Cleanup happens in mistral_transcription_handler's finally block


def ensure_session(session_id):
    """Get or create a valid UserSession from a session_id."""
    # Handle various invalid inputs
    if session_id is None or callable(session_id):
        session = get_or_create_session()
        return session
    
    # If it's already a UserSession object (legacy), return it
    if isinstance(session_id, UserSession):
        return session_id
    
    # Otherwise treat it as a session_id string
    session = get_or_create_session(str(session_id))
    
    # Defensive check - this should never happen but helps debug
    if not isinstance(session, UserSession):
        print(f"WARNING: ensure_session returned non-UserSession: {type(session)}")
        return get_or_create_session()
    
    return session


def auto_start_recording(session):
    """Automatically start the transcription service when audio begins."""
    # Protect against startup races: Gradio can call `process_audio` concurrently.
    with session._start_lock:
        if session.is_running:
            return get_transcription_html(session.reconstruct_transcription(), session.status_message, session.current_wpm, session.partial_transcript_enabled)
        
        # Check if API key is set
        if not session.api_key:
            session.status_message = "error"
            return get_transcription_html(("Please enter your Mistral API key above to start transcription.","",""), "error", "", False)
        
        # Check if we've hit max concurrent sessions - kill all if so
        with _sessions_lock:
            active_at_capacity = len(_active_sessions) >= MAX_CONCURRENT_SESSIONS
        with _registry_lock:
            registry_over = len(_session_registry) > MAX_CONCURRENT_SESSIONS
        
        if active_at_capacity or registry_over:
            kill_all_sessions()
            session.status_message = "error"
            return get_transcription_html(("Server reset due to capacity. Please click the microphone to restart.","",""), "error", "", False)
        
        session.word_timestamps = []
        session.current_wpm = "Calibrating..."
        session.session_start_time = time.time()
        session.last_audio_time = time.time()
        session.status_message = "connecting"
        session.stream_events = {
            'stream_1': [],
            'stream_2': []
        }
        
        # Start Mistral transcription (now non-blocking, uses shared event loop)
        start_transcription(session)
    
    return get_transcription_html(session.reconstruct_transcription(), session.status_message, session.current_wpm, session.partial_transcript_enabled)


def stop_session(session_id, api_key=None, partial_transcript=False):
    """Stop the transcription and invalidate the session.
    
    Returns None for session_id so a fresh session is created on next recording.
    This prevents duplicate session issues when users stop and restart quickly.
    """
    session = ensure_session(session_id)
    old_transcripts = session.reconstruct_transcription()
    old_wpm = session.current_wpm
    
    if session.is_running:
        session.is_running = False
        session.last_audio_time = None
        session._stopped_by_user = True  # Mark as user-stopped to avoid duplicate logging
        
        # Signal the stop event to terminate the audio stream
        if session._stop_event is not None:
            loop = get_event_loop()
            try:
                asyncio.run_coroutine_threadsafe(
                    _set_stop_event(session._stop_event), loop
                )
            except Exception:
                pass
            session._stop_event = None
        
        # Cancel the running task if any
        if session._task is not None:
            session._task.cancel()
            session._task = None
        
        # Remove from active sessions
        with _sessions_lock:
            _active_sessions.pop(session.session_id, None)
            active_count = len(_active_sessions)
        
        print(f"Mic stopped - session {session.session_id[:8]} ended. Active sessions: {active_count}")
    
    # Remove from registry - the session is done
    cleanup_session(session.session_id)
    
    # Return None for session_id - a fresh session will be created on next recording
    # This ensures no duplicate sessions when users stop/start quickly
    return get_transcription_html(old_transcripts, "ready", old_wpm, partial_transcript), None


async def _set_stop_event(event):
    """Helper to set asyncio event from sync context."""
    event.set()


def clear_history(session_id, api_key=None, partial_transcript=False):
    """Stop the transcription and clear all history."""
    session = ensure_session(session_id)
    session.is_running = False
    session.last_audio_time = None
    session._stopped_by_user = True  # Mark as user-stopped
    
    # Signal the stop event
    if session._stop_event is not None:
        loop = get_event_loop()
        try:
            asyncio.run_coroutine_threadsafe(
                _set_stop_event(session._stop_event), loop
            )
        except Exception:
            pass
        session._stop_event = None
    
    # Cancel the running task if any
    if session._task is not None:
        session._task.cancel()
        session._task = None
    
    # Remove from active sessions
    with _sessions_lock:
        _active_sessions.pop(session.session_id, None)
    
    # Reset the queue
    session.reset_queue()
    
    # Clear event history
    session.clear_events()
    
    session.word_timestamps = []
    session.current_wpm = "Calibrating..."
    session.session_start_time = None
    session.status_message = "ready"
    session.stream_events = {
        'stream_1': [],
        'stream_2': []
    }
    
    # Return the session_id to maintain state
    return get_transcription_html(("",), "ready", "Calibrating...", False), None, session.session_id


def process_audio(audio, session_id, api_key, partial_transcript=False):
    """Process incoming audio and queue for streaming."""
    # Check capacity - if at or above max, kill ALL sessions to reset
    with _sessions_lock:
        active_count = len(_active_sessions)
        is_active_user = session_id and any(s.session_id == session_id for s in _active_sessions.values())
    
    with _registry_lock:
        registry_count = len(_session_registry)
    
    # Kill all if:
    # 1. Registry exceeds limit (memory safety)
    # 2. Active sessions exceed limit
    # 3. At active capacity AND new user trying to join
    if registry_count > MAX_CONCURRENT_SESSIONS or active_count > MAX_CONCURRENT_SESSIONS or (active_count >= MAX_CONCURRENT_SESSIONS and not is_active_user):
        kill_all_sessions()
        return get_transcription_html(
            ("Server reset due to capacity. Please click the microphone to restart.","",""), 
            "error", 
            "",
            False
        ), None
    
    # Check if API key is provided
    if not api_key or not api_key.strip():
        # return get_transcription_html(
        #     ("Please enter your Mistral API key above to start transcription.","",""), 
        #     "error", 
        #     ""
        # ), None
        api_key = DEFAULT_API_KEY
    
    # Always ensure we have a valid session first
    try:
        session = ensure_session(session_id)
        # Update API key on the session
        session.api_key = api_key.strip()
        # Store partial transcript preference on the session
        session.partial_transcript_enabled = partial_transcript
    except Exception as e:
        print(f"Error creating session: {e}")
        # Create a fresh session if ensure_session fails
        session = UserSession(api_key=api_key.strip())
        session.partial_transcript_enabled = partial_transcript
        _session_registry[session.session_id] = session
    
    # Cache session_id early in case of later errors
    current_session_id = session.session_id
    
    try:
        # Quick return if audio is None
        if audio is None:
            wpm = session.current_wpm if session.is_running else "Calibrating..."
            return get_transcription_html(session.reconstruct_transcription(), session.status_message, wpm, session.partial_transcript_enabled), current_session_id

        # Update last audio time for inactivity tracking
        session.last_audio_time = time.time()

        # Auto-start if not running
        if not session.is_running and session.status_message not in ["timeout", "error"]:
            auto_start_recording(session)

        # Skip processing if session stopped
        if not session.is_running:
            return get_transcription_html(session.reconstruct_transcription(), session.status_message, session.current_wpm, session.partial_transcript_enabled), current_session_id

        sample_rate, audio_data = audio

        # Convert to mono if stereo
        if len(audio_data.shape) > 1:
            audio_data = audio_data.mean(axis=1)

        # Normalize to float
        if audio_data.dtype == np.int16:
            audio_float = audio_data.astype(np.float32) / 32767.0
        else:
            audio_float = audio_data.astype(np.float32)

        # Resample to 16kHz if needed
        if sample_rate != SAMPLE_RATE:
            num_samples = int(len(audio_float) * SAMPLE_RATE / sample_rate)
            audio_float = np.interp(
                np.linspace(0, len(audio_float) - 1, num_samples),
                np.arange(len(audio_float)),
                audio_float,
            )

        # Convert to PCM16 and base64 encode
        pcm16 = (audio_float * 32767).astype(np.int16)
        b64_chunk = base64.b64encode(pcm16.tobytes()).decode("utf-8")
        
        # Put directly into thread-safe queue (no event loop needed)
        try:
            session.audio_queue.put_nowait(b64_chunk)
        except Exception:
            pass  # Skip if queue is full

        return get_transcription_html(session.reconstruct_transcription(), session.status_message, session.current_wpm, session.partial_transcript_enabled), current_session_id
    except Exception as e:
        print(f"Error processing audio: {e}")
        # Return safe defaults - always include session_id to maintain state
        return get_transcription_html(("",), "error", "", False), current_session_id

# Gradio interface
with gr.Blocks(title="Voxtral Real-time Transcription") as demo:
    # Store just the session_id string - much more reliable than complex objects
    session_state = gr.State(value=None)
    
    # Header
    gr.HTML(get_header_html())
    
    # API Key input with partial transcript checkbox
    with gr.Row():
        api_key_input = gr.Textbox(
            label="Mistral API Key (optional)",
            placeholder="Enter your own Mistral API key if you encounter issues.",
            type="password",
            elem_id="api-key-input",
            info="Get your API key from console.mistral.ai",
            scale=4
        )
        partial_transcript_checkbox = gr.Checkbox(
            label="Partial Transcript",
            info="Enable to show 2 streams + merged output",
            value=False,
            elem_id="partial-transcript-checkbox",
            scale=1
        )
    
    # Transcription output
    transcription_display = gr.HTML(
        value=get_transcription_html(("","",""), "ready", "Calibrating...", False),
        elem_id="transcription-output"
    )
    
    # Audio input
    audio_input = gr.Audio(
        sources=["microphone"],
        streaming=True,
        type="numpy",
        format="wav",
        elem_id="audio-input",
        label="Microphone Input"
    )
    
    # Clear button
    clear_btn = gr.Button(
        "Clear History",
        elem_classes=["clear-btn"]
    )
    
    # Info text
    gr.HTML('<p class="info-text">To start again - click on Clear History AND refresh your website.</p>')

    # Event handlers
    clear_btn.click(
        clear_history,
        inputs=[session_state, api_key_input, partial_transcript_checkbox],
        outputs=[transcription_display, audio_input, session_state]
    )
    
   
    audio_input.stop_recording(
        stop_session,
        inputs=[session_state, api_key_input, partial_transcript_checkbox],
        outputs=[transcription_display, session_state]
    )
    
    audio_input.stream(
        process_audio,
        inputs=[audio_input, session_state, api_key_input, partial_transcript_checkbox],
        outputs=[transcription_display, session_state],
        show_progress="hidden",
        concurrency_limit=500,  
    )

get_event_loop()

demo.queue(default_concurrency_limit=200)
demo.launch(css=CUSTOM_CSS, theme=gr.themes.Base(), ssr_mode=False, max_threads=200)