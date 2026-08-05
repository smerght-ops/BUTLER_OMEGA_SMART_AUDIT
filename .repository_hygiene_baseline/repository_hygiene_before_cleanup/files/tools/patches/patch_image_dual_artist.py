from pathlib import Path

p=Path(r".\A_04_AGENTS\ImageDepartment\runner.py")
text=p.read_text(encoding="utf-8")

old="""        prompt = self._ask_artist(
            model_name,
            artist_prompt
        )

        print("[*] IMAGE prompt generated")
"""

new="""        draft_prompt = self._ask_artist(
            "DeepSeek-GPU:latest",
            artist_prompt
        )

        print("[*] IMAGE draft prompt generated")

        review_prompt = (
            "You are a senior Stable Diffusion prompt reviewer. "
            "Improve the following prompt without changing its meaning. "
            "Return ONLY the final prompt.\\n\\n"
            + draft_prompt
        )

        prompt = self._ask_artist(
            "gemma-4:latest",
            review_prompt
        )

        role_name = "DeepSeek → gemma-4"
        model_name = "DeepSeek-GPU:latest -> gemma-4:latest"

        print("[*] IMAGE reviewed prompt generated")
"""

if old not in text:
    raise SystemExit("Target block not found.")

text=text.replace(old,new,1)
p.write_text(text,encoding="utf-8")
print("PATCH OK")
