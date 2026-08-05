# -*- coding: utf-8 -*-

import pathlib
import subprocess
import requests
import time

OLLAMA="http://127.0.0.1:11434/api/generate"

USER="A woman full-length at the beach under a waterfall with reddish hair, shot from behind."

GENERATOR_PROMPT="""
You are a professional Stable Diffusion XL prompt engineer.

Convert the user's request into ONE final English SDXL prompt.

Return ONLY the prompt.
"""

REVIEW_PROMPT="""
You are a senior Prompt Reviewer.

Improve the prompt.

Do NOT change the idea.

Strengthen:

- anatomy
- composition
- cinematic light
- photorealism
- masterpiece
- ultra detailed
- full body
- correct camera angle

Return ONLY the improved prompt.
"""

ROOT=pathlib.Path("A_06_WORKSPACE")/"OLYMPICS_V3"
ROOT.mkdir(parents=True,exist_ok=True)

MODELS=[
"DeepSeek-GPU:latest",
"Codestral-Pro:latest",
"codestral:latest",
"Mistral-Nemo-Instruct-2407-Q8_0:latest",
"gemma-4:latest",
"Gemma:latest",
"ibm-granite_granite-4.1-30b-Q5_K_S:latest",
"qwen35:latest",
"qwen35-ru:latest",
"qwen-3_5:latest"
]

def ask(model,prompt):

    r=requests.post(
        OLLAMA,
        json={
            "model":model,
            "prompt":prompt,
            "stream":False
        },
        timeout=300
    )

    r.raise_for_status()

    return r.json()["response"].strip()

for gen in MODELS:

    for rev in MODELS:

        print(f"{gen}  ->  {rev}")

        folder=ROOT/(gen.replace(":","_")+"__"+rev.replace(":","_"))
        folder.mkdir(parents=True,exist_ok=True)

        t=time.time()

        try:

            draft=ask(
                gen,
                GENERATOR_PROMPT+"\n\n"+USER
            )

            review=ask(
                rev,
                REVIEW_PROMPT+"\n\n"+draft
            )

            (folder/"draft.txt").write_text(draft,encoding="utf-8")
            (folder/"review.txt").write_text(review,encoding="utf-8")
            (folder/"time.txt").write_text(str(round(time.time()-t,1)),encoding="utf-8")

            print("OK")

        except Exception as e:

            (folder/"error.txt").write_text(str(e),encoding="utf-8")

            print("FAILED")

print("DONE")
