# -*- coding: utf-8 -*-

import json
import pathlib
import subprocess
import time

import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

SYSTEM_PROMPT = """
You are a professional Prompt Engineer for Stable Diffusion XL and ComfyUI.

Your task:

Convert the user's request into ONE final English image generation prompt.

Rules:

- English only.
- No explanations.
- No markdown.
- No title.
- No notes.
- Return ONLY the final prompt.
- Highly detailed.
- Photorealistic.
- Cinematic.
- Full composition.
- Suitable for SDXL / ComfyUI.
"""

USER_PROMPT = (
    "A woman full-length at the beach under a waterfall "
    "with reddish hair, shot from behind."
)

EXPORT = pathlib.Path("A_06_WORKSPACE") / "OLYMPICS_V2"
EXPORT.mkdir(parents=True, exist_ok=True)


def installed_models():

    out = subprocess.check_output(
        ["ollama", "list"],
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    result = []

    for line in out.splitlines()[1:]:

        line=line.strip()

        if not line:
            continue

        model=line.split()[0]

        result.append(model)

    return result


def ask(model):

    payload = {
        "model": model,
        "prompt": SYSTEM_PROMPT + "\n\nUser:\n" + USER_PROMPT,
        "stream": False
    }

    r = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300
    )

    r.raise_for_status()

    return r.json()["response"].strip()


models = installed_models()

print("=" * 70)
print("MODEL OLYMPICS V2")
print("=" * 70)

summary=[]

for model in models:

    print(f"\n=== {model} ===")

    folder = EXPORT / model.replace(":","_")
    folder.mkdir(parents=True,exist_ok=True)

    t0=time.time()

    try:

        prompt=ask(model)

        dt=round(time.time()-t0,1)

        (folder/"prompt.txt").write_text(
            prompt,
            encoding="utf-8"
        )

        (folder/"time.txt").write_text(
            str(dt),
            encoding="utf-8"
        )

        print(f"OK {dt}s")

        summary.append((model,"OK",dt))

    except Exception as e:

        (folder/"error.txt").write_text(
            str(e),
            encoding="utf-8"
        )

        print("FAILED")

        summary.append((model,"FAILED","-"))

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)

for m,s,t in summary:
    print(f"{m:<45} {s:<8} {t}")

print()
print("DONE")
