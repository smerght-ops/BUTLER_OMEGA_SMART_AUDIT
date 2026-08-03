# -*- coding: utf-8 -*-
"""Minimal Whisper Audio Engine for AudioDepartment."""

import os
import subprocess
from pathlib import Path


WHISPER_RUNTIME = r"D:\AI_Hub\Voice_Models\Whisper\runtime"
PYTHON_EXECUTABLE = r"D:\AI_Hub\Voice_Models\Whisper\runtime\Scripts\python.exe"
MODELS_PATH = r"D:\AI_Hub\Voice_Models\Whisper\models"

AVAILABLE_MODELS = ["turbo", "large-v3"]
DEFAULT_MODEL = "turbo"


class WhisperEngine:
    """Minimal Whisper engine compatible with AudioDepartment contract."""

    def __init__(self, model: str = None):
        self.model_name = model or DEFAULT_MODEL

    def __call__(self, mode: str, payload: str, context: dict = None) -> dict:
        """
        Callable compatible with AudioDepartment contract.

        Args:
            mode: "recognize" or other (only recognize supported).
            payload: path to audio file for recognition.
            context: optional dict with whisper_model override.

        Returns:
            {"text": "<recognized text>"} on success.
            Raises ValueError on unsupported mode or errors.
        """
        context = context or {}

        if mode != "recognize":
            raise ValueError(f"UNSUPPORTED_AUDIO_MODE: {mode}")

        audio_path = Path(payload)
        if not audio_path.exists():
            raise FileNotFoundError(f"AUDIO_FILE_NOT_FOUND: {payload}")

        model_override = context.get("whisper_model")
        model_to_use = model_override or self.model_name
        model_filename_map = {
            "turbo": "large-v3-turbo.pt",
            "large-v3": "large-v3.pt",
        }
        model_filename = model_filename_map.get(model_to_use, f"{model_to_use}.pt")
        model_pt = Path(MODELS_PATH) / model_filename

        if not model_pt.exists():
            raise FileNotFoundError(f"MODEL_NOT_FOUND: {model_pt}")

        if model_to_use not in AVAILABLE_MODELS:
            raise ValueError(f"UNSUPPORTED_WHISPER_MODEL: {model_to_use}")

        runner_code = (
            "import whisper,sys; "
            "m=whisper.load_model(sys.argv[1], device='cuda', download_root=sys.argv[3]); "
            "r=m.transcribe(sys.argv[2], language='ru'); "
            "print(r.get('text','').strip())"
        )

        cmd = [PYTHON_EXECUTABLE, "-c", runner_code, model_to_use, str(audio_path), MODELS_PATH]

        try:
            result = subprocess.run(
                cmd,
                cwd=WHISPER_RUNTIME,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=300,
                env={**os.environ, "CUDA_VISIBLE_DEVICES": "0", "PATH": r"C:\Users\KOS\Desktop\Butler_Agent\MEDIA_PILOT\tools\ffmpeg-8.1.2-essentials_build\bin" + os.pathsep + os.environ.get("PATH", "")},
            )

            if result.returncode != 0:
                raise RuntimeError(f"Whisper execution failed: {result.stderr}")

            return {"text": result.stdout.strip()}

        except subprocess.TimeoutExpired:
            raise RuntimeError("Whisper transcription timed out")


def create_audio_engine(model: str = None):
    """Factory function to create audio engine instance."""
    return WhisperEngine(model=model)
