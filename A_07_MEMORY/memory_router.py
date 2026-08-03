# -*- coding: utf-8 -*-

from A_07_MEMORY.profile_manager import set_fact


def route_memory(key: str):
    key = key.strip().lower()

    if key in {"мое имя", "моё имя", "имя"}:
        return "user_name", "name"
    if key in {"любимый цвет", "мой любимый цвет"}:
        return "preferences", "favorite_color"
    if key == "навык":
        return "skills", "skill"
    if key == "проект":
        return "projects", "project"

    return "facts", None


def parse_memory_command(text: str):
    text = (text or "").strip()
    if not text.lower().startswith("запомни"):
        return None

    payload = text[len("запомни"):].strip().lstrip(":").strip()
    separator = next(
        (item for item in ("=", "—", "–", ":") if item in payload),
        None,
    )
    if not separator:
        return None

    key, value = payload.split(separator, 1)
    key = key.strip()
    value = value.strip().rstrip(".").strip()
    if not key or not value:
        return None

    section, fixed_key = route_memory(key)
    return section, fixed_key or key.lower(), value


def remember(text: str):
    parsed = parse_memory_command(text)
    if not parsed:
        return False

    section, key, value = parsed
    set_fact(section, key, value)
    return True
