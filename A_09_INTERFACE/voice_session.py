"""Full-duplex voice session orchestration for Butler.

Audio transport and model implementations are injected.  This module owns only
voice turn state; recognized text is always executed by AgentCoreCoordinator.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol
from uuid import uuid4


class StreamingSTT(Protocol):
    def start(self) -> None: ...
    def feed(self, audio: bytes) -> None: ...
    def finish(self) -> str: ...
    def cancel(self) -> None: ...


class StreamingTTS(Protocol):
    def start(self, text: str) -> None: ...
    def cancel(self) -> None: ...


class VoiceCoordinator(Protocol):
    def execute(self, query: str, context: dict | None = None) -> dict: ...


@dataclass(frozen=True)
class VoiceSessionSnapshot:
    session_id: str
    state: str
    turns: int
    interrupted: bool
    error: str | None


class VoiceActivityDetector:
    """Energy-based VAD with deterministic end-of-turn detection."""

    def __init__(self, threshold: float = 0.008, end_silence_chunks: int = 3):
        if threshold < 0 or end_silence_chunks < 1:
            raise ValueError("Invalid VAD configuration")
        self.threshold = threshold
        self.end_silence_chunks = end_silence_chunks
        self.speaking = False
        self._silence_chunks = 0

    def observe(self, energy: float) -> str:
        voiced = energy >= self.threshold
        if voiced:
            self._silence_chunks = 0
            if not self.speaking:
                self.speaking = True
                return "speech_start"
            return "speech"
        if not self.speaking:
            return "silence"
        self._silence_chunks += 1
        if self._silence_chunks >= self.end_silence_chunks:
            self.speaking = False
            self._silence_chunks = 0
            return "speech_end"
        return "speech_pause"

    def reset(self) -> None:
        self.speaking = False
        self._silence_chunks = 0


class VoiceSessionManager:
    """Coordinate continuous STT, Butler turns, TTS, and barge-in."""

    STATES = {"idle", "listening", "thinking", "speaking", "closed"}

    def __init__(self, coordinator: VoiceCoordinator, stt: StreamingSTT,
                 tts: StreamingTTS, vad: VoiceActivityDetector | None = None):
        self.coordinator = coordinator
        self.stt = stt
        self.tts = tts
        self.vad = vad or VoiceActivityDetector()
        self.session_id = uuid4().hex
        self.state = "idle"
        self.turns = 0
        self.interrupted = False
        self.error: str | None = None

    def snapshot(self) -> VoiceSessionSnapshot:
        return VoiceSessionSnapshot(
            self.session_id, self.state, self.turns, self.interrupted, self.error,
        )

    def accept_audio(self, audio: bytes, energy: float) -> dict | None:
        """Accept one audio chunk and return a completed Butler turn, if any."""
        if self.state == "closed":
            raise RuntimeError("VOICE_SESSION_CLOSED")
        activity = self.vad.observe(energy)

        if activity == "speech_start":
            if self.state == "speaking":
                self.tts.cancel()
                self.interrupted = True
            if self.state not in {"idle", "speaking"}:
                return None
            self.stt.start()
            self.state = "listening"
            self.stt.feed(audio)
            return None

        if self.state == "listening" and activity in {"speech", "speech_pause"}:
            self.stt.feed(audio)
            return None

        if self.state == "listening" and activity == "speech_end":
            return self._complete_turn()
        return None

    def _complete_turn(self) -> dict | None:
        try:
            transcript = self.stt.finish().strip()
            if not transcript:
                self.state = "idle"
                return None
            self.state = "thinking"
            result = self.coordinator.execute(transcript, context={
                "input_method": "voice",
                "voice_session_id": self.session_id,
            })
            self.turns += 1
            response = str(result.get("text") or "").strip()
            if result.get("ok") and response:
                self.tts.start(response)
                self.state = "speaking"
            else:
                self.state = "idle"
            return {"transcript": transcript, "result": result, "session": self.snapshot()}
        except Exception as exc:
            self.error = f"{type(exc).__name__}: {exc}"
            self.state = "idle"
            return {"transcript": "", "result": {"ok": False, "error": self.error},
                    "session": self.snapshot()}

    def tts_completed(self) -> None:
        if self.state == "speaking":
            self.state = "idle"

    def close(self) -> None:
        if self.state == "listening":
            self.stt.cancel()
        if self.state == "speaking":
            self.tts.cancel()
        self.vad.reset()
        self.state = "closed"
