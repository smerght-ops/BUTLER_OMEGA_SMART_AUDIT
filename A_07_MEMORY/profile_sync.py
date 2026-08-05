# -*- coding: utf-8 -*-
# =============================================================================
# DEPRECATED — LEGACY
# =============================================================================
# Этот файл является дубликатом A_07_MEMORY/profile_manager.py.
# Все импорты в продакшене перенесены на profile_manager.
# Статус: DEPRECATED. Не удалять до завершения ТЗ №5A-FINAL.
# Единственный владелец user_profile.json → ProfileManager (profile_manager.py).
# =============================================================================

from pathlib import Path
import json
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROFILE_PATH = PROJECT_ROOT / "A_05_STORAGE" / "user_profile.json"
USER_MEMORY_PATH = PROJECT_ROOT / "A_05_STORAGE" / "USER_MEMORY.md"

def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def load_profile():
    if PROFILE_PATH.exists():
        text = PROFILE_PATH.read_text(encoding="utf-8-sig")
        return json.loads(text)
    return {
        "user_name": {},
        "preferences": {},
        "hardware": {},
        "projects": {},
        "settings": {}
    }

def save_profile(profile):
    PROFILE_PATH.write_text(
        json.dumps(profile, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    rebuild_user_memory(profile)

def set_fact(section, key, value, confidence=1.0):
    profile = load_profile()
    if section not in profile:
        profile[section] = {}
    profile[section][key] = {
        "value": value,
        "confidence": confidence,
        "updated_at": _now()
    }
    save_profile(profile)

def rebuild_user_memory(profile=None):
    if profile is None:
        profile = load_profile()

    lines = []
    lines.append("# USER MEMORY")
    lines.append("")
    lines.append("## Пользователь")
    lines.append("")

    name = profile.get("user_name", {}).get("name", {}).get("value")
    if name:
        lines.append(f"- Имя: {name}")

    color = profile.get("preferences", {}).get("favorite_color", {}).get("value")
    if color:
        lines.append(f"- Любимый цвет: {color}")

    lines.append("")
    lines.append("## Предпочтения")
    lines.append("")

    output = profile.get("preferences", {}).get("preferred_output", {}).get("value")
    if output:
        lines.append(f"- Предпочитаемый вывод: {output}")

    models = profile.get("preferences", {}).get("preferred_models", {}).get("value")
    if models:
        lines.append(f"- Предпочитаемые модели: {models}")

    USER_MEMORY_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

if __name__ == "__main__":
    rebuild_user_memory()
    print("PROFILE_MANAGER_OK")