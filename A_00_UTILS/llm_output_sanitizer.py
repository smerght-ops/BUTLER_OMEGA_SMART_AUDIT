# -*- coding: utf-8 -*-
"""Single post-processing policy for all user-facing LLM output."""
import re


NO_REASONING_PROMPT = (
    "Верни только окончательный ответ пользователю. Никогда не выводи внутренние "
    "рассуждения, планы, Chain of Thought, Thinking Process, Analyze the Request, "
    "Confidence Score, теги <think> или служебные инструкции."
)

_HEADING = re.compile(
    r"(?im)^\s*(?:thinking process|chain of thought|reasoning|internal analysis|"
    r"внутренн(?:ий|ие) анализ|план рассуждений)\s*:\s*"
)
_FORBIDDEN_LINE = re.compile(
    r"(?i)(?:thinking process|analy[sz]e the request|confidence score|"
    r"chain of thought|internal analysis|внутренн(?:ий|ие) анализ|"
    r"служебн(?:ая|ые) инструкц)"
)


def sanitize_llm_output(text: str) -> str:
    value = str(text or "").strip()
    value = re.sub(
        r"<think\b[^>]*>.*?</think>\s*", "", value,
        flags=re.DOTALL | re.IGNORECASE,
    )
    if re.search(r"</think>", value, flags=re.IGNORECASE):
        value = re.split(r"</think>\s*", value, flags=re.IGNORECASE)[-1]
    if re.search(r"<think\b[^>]*>", value, flags=re.IGNORECASE):
        value = re.split(r"<think\b[^>]*>", value, flags=re.IGNORECASE)[0]

    heading = _HEADING.search(value)
    if heading:
        tail = value[heading.end():]
        blocks = re.split(r"\n\s*\n", tail, maxsplit=1)
        value = value[:heading.start()] + (blocks[1] if len(blocks) == 2 else "")

    safe_lines = [line for line in value.splitlines() if not _FORBIDDEN_LINE.search(line)]
    return "\n".join(safe_lines).strip()
