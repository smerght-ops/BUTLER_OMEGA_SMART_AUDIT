# -*- coding: utf-8 -*-

from A_01_CORE.manifest_loader import ManifestLoader

_cfg = ManifestLoader.load()

MODEL_REGISTRY = {
    "CHAT": _cfg.get("analysis_model","qwen35-ru:latest"),
    "CODING": [
        _cfg.get("coder_model","DeepSeek-Coder-V2-Lite-Instruct-Q6_K:latest"),
        "sub-coder-32b:latest",
        _cfg.get("fallback_model","codestral:latest")
    ],
    "VISION": _cfg.get("vision_model","qwen2.5-vl:latest"),
    "IMAGE": {
        "horror": "DeepSeek-GPU:latest",
        "creative": "gemma-4:latest",
        "technical": "ibm-granite_granite-4.1-30b-Q5_K_S:latest"
    },
    "TEXT": {
        "default": _cfg.get("analysis_model", "qwen35-ru:latest"),
        "analytic": _cfg.get("analysis_model", "qwen35-ru:latest"),
        "writer": "gemma-4:latest",
        "engineer": _cfg.get("coder_model", "DeepSeek-Coder-V2-Lite-Instruct-Q6_K:latest")
    },
    "AUDIO": _cfg.get("analysis_model","qwen35-ru:latest"),
    "VIDEO": _cfg.get("analysis_model","qwen35-ru:latest"),
    "ARCHIVE": _cfg.get("analysis_model","qwen35-ru:latest")
}