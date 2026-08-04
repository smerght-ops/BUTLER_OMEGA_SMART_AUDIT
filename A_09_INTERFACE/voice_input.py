# -*- coding: utf-8 -*-
"""Voice-first input and long-form secretary capture for Butler."""
from __future__ import annotations

import queue
import threading
import time
from datetime import datetime
from pathlib import Path

try:
    import numpy as np
    import sounddevice as sd
    from scipy.io import wavfile
    _HAS_AUDIO = True
except ImportError:
    _HAS_AUDIO = False


def _voice_inbox():
    path = Path(__file__).resolve().parents[1] / "A_06_WORKSPACE" / "STAGE4_OUTPUT" / "voice_inbox"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _stop_on_enter(stop):
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass
    stop.set()


def _record_until_user_stops(fs=16000, silence_seconds=None):
    if not _HAS_AUDIO:
        raise RuntimeError("VOICE_DEPENDENCIES_MISSING: pip install sounddevice scipy numpy")
    chunks, stop = [], threading.Event()
    started = last_voice = time.monotonic()

    def callback(indata, frames, time_info, status):
        nonlocal last_voice
        chunks.append(indata.copy())
        if float(np.abs(indata).mean()) >= 0.008:
            last_voice = time.monotonic()

    print("[VOICE] RECORDING — нажмите Enter, когда закончите.")
    threading.Thread(target=_stop_on_enter, args=(stop,), daemon=True).start()
    try:
        with sd.InputStream(samplerate=fs, channels=1, dtype="float32", callback=callback):
            while not stop.wait(0.25):
                elapsed = time.monotonic() - started
                beat = "●" if int(elapsed * 2) % 2 == 0 else "○"
                print(f"\r[VOICE] RECORDING {beat} {elapsed:6.1f}s", end="", flush=True)
                if silence_seconds and chunks and elapsed > 1 and time.monotonic() - last_voice >= silence_seconds:
                    break
    except KeyboardInterrupt:
        stop.set()
    print()
    return np.concatenate([c.reshape(-1) for c in chunks]).astype(np.float32) if chunks else None


def _recognize_audio(audio, fs=16000):
    from A_03_ENGINES.Audio_Engine.whisper_engine import create_audio_engine
    from A_03_ORCHESTRATION.permission import DepartmentExecutionGateway
    from A_04_AGENTS.AudioDepartment.runner import AudioDepartment
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S_%f")
    wav_path = _voice_inbox() / f".{stamp}_processing.wav"
    wavfile.write(str(wav_path), fs, audio)
    try:
        result = DepartmentExecutionGateway().execute(
            AudioDepartment(),
            "распознай речь",
            context={"attachments": [str(wav_path)], "audio_engine": create_audio_engine()},
        )
        if not result.get("ok"):
            raise RuntimeError(result.get("error") or "VOICE_RECOGNITION_FAILED")
        return (result.get("text") or "").strip()
    finally:
        wav_path.unlink(missing_ok=True)


def capture_voice_turn():
    audio = _record_until_user_stops()
    if audio is None:
        return ""
    print("[VOICE] PROCESSING")
    transcript = _recognize_audio(audio)
    print(f"[VOICE] Вы: {transcript}")
    return transcript


def _merge_overlap(parts):
    merged = []
    for part in parts:
        words = part.split()
        limit = min(24, len(merged), len(words))
        overlap = next((n for n in range(limit, 0, -1)
                        if [w.casefold() for w in merged[-n:]]
                        == [w.casefold() for w in words[:n]]), 0)
        merged.extend(words[overlap:])
    return " ".join(merged)


def _persist_ramble(transcript):
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S_%f")
    raw_path = _voice_inbox() / f"{stamp}_raw_transcript.md"
    raw_path.write_text(transcript, encoding="utf-8")
    from A_07_MEMORY.dki_compiler import DKICompiler
    from A_07_MEMORY.semantic_memory import SemanticMemory
    compiled = DKICompiler(memory=SemanticMemory()).compile(
        str(raw_path), transcript, model_name="butler-router-70b:latest")
    return {"ok": True, "department": "VOICE", "model": "Whisper",
            "latency_ms": 0, "text": transcript, "error": None,
            "metadata": {"voice_inbox": {"ok": True, "path": str(raw_path)},
                         "dki_compile": compiled, "mode": "ramble"}}


def ramble_session(chunk_seconds=25, overlap_seconds=1):
    if not _HAS_AUDIO:
        raise RuntimeError("VOICE_DEPENDENCIES_MISSING: pip install sounddevice scipy numpy")
    fs, audio_queue, stop = 16000, queue.Queue(), threading.Event()
    transcripts, started = [], time.monotonic()
    chunk_frames, overlap_frames = int(chunk_seconds * fs), int(overlap_seconds * fs)
    pending = np.empty(0, dtype=np.float32)

    def callback(indata, frames, time_info, status):
        audio_queue.put(indata.copy().reshape(-1))

    print("[VOICE] RECORDING — режим секретаря. Нажмите Enter для завершения.")
    threading.Thread(target=_stop_on_enter, args=(stop,), daemon=True).start()
    with sd.InputStream(samplerate=fs, channels=1, dtype="float32", callback=callback):
        while not stop.is_set() or not audio_queue.empty():
            try:
                pending = np.concatenate((pending, audio_queue.get(timeout=.25)))
            except queue.Empty:
                pass
            elapsed = time.monotonic() - started
            beat = "●" if int(elapsed * 2) % 2 == 0 else "○"
            print(f"\r[VOICE] RECORDING {beat} {elapsed:6.1f}s", end="", flush=True)
            if len(pending) >= chunk_frames:
                print("\n[VOICE] PROCESSING chunk")
                text = _recognize_audio(pending[:chunk_frames])
                if text:
                    transcripts.append(text)
                    print(f"[VOICE] {text}")
                pending = pending[chunk_frames - overlap_frames:]
    if len(pending) > int(.25 * fs):
        print("\n[VOICE] PROCESSING final chunk")
        text = _recognize_audio(pending)
        if text:
            transcripts.append(text)
    transcript = _merge_overlap(transcripts).strip()
    if not transcript:
        return {"ok": False, "department": "VOICE", "error": "EMPTY_TRANSCRIPT", "text": ""}
    print("[VOICE] SAVING")
    result = _persist_ramble(transcript)
    print("[VOICE] DONE")
    return result


def voice_command(agent_execute=None, request_envelope_factory=None):
    envelope = (
        request_envelope_factory("", input_method="voice")
        if request_envelope_factory else None
    )
    transcript = capture_voice_turn()
    if not transcript:
        return None
    if agent_execute:
        print("[VOICE] Отправляю Butler...")
        if envelope is not None:
            envelope["original_text"] = transcript
            return agent_execute(envelope)
        return agent_execute(transcript)
    return {"ok": True, "department": "VOICE", "model": "Whisper",
            "text": transcript, "error": None}


if __name__ == "__main__":
    voice_command()
