# -*- coding: utf-8 -*-

import json
import pathlib
import requests
import time

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

MODELS = [
    "DeepSeek-GPU:latest",
    "Codestral-Pro:latest",
    "codestral:latest",
    "Mistral-Nemo-Instruct-2407-Q8_0:latest",
    "gemma-4:latest",
    "ibm-granite_granite-4.1-30b-Q5_K_S:latest",
]

USER_PROMPT = (
    "A woman full-length at the beach under a waterfall "
    "with reddish hair, shot from behind."
)

EXPORT = pathlib.Path("A_06_WORKSPACE") / "OLYMPICS"
EXPORT.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("MODEL OLYMPICS")
print("=" * 70)

for model in MODELS:

    print(f"\n=== {model} ===")

    payload = {
        "model": model,
        "prompt": USER_PROMPT,
        "stream": False,
    }

    t0 = time.time()

    r = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300,
    )

    r.raise_for_status()

    prompt = r.json()["response"].strip()

    folder = EXPORT / model.replace(":", "_")
    folder.mkdir(exist_ok=True)

    (folder / "prompt.txt").write_text(
        prompt,
        encoding="utf-8",
    )

    dt = round(time.time() - t0, 1)

    print(f"OK  {dt}s")

print("\nDONE")
