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


def get_fact(section, key, default=None):
    profile = load_profile()

    if section not in profile:
        return default

    if key not in profile[section]:
        return default

    return profile[section][key].get("value", default)


def delete_fact(key):
    profile = load_profile()

    if "facts" not in profile:
        return False

    if key not in profile["facts"]:
        return False

    del profile["facts"][key]
    save_profile(profile)
    return True
def list_facts():
    profile = load_profile()
    return profile.get("facts", {})
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


def get_memory_summary():
    profile = load_profile()

    lines = []
    lines.append("ПОЛЬЗОВАТЕЛЬ")
    lines.append("------------")

    name = profile.get("user_name", {}).get("name", {}).get("value")
    if name:
        lines.append(name)

    lines.append("")

    prefs = profile.get("preferences", {})
    if prefs:
        lines.append("ПРЕДПОЧТЕНИЯ")
        lines.append("------------")

        for key, data in prefs.items():
            if isinstance(data, dict) and "value" in data:
                lines.append(f"{key} = {data['value']}")

        lines.append("")

    facts = profile.get("facts", {})
    if facts:
        lines.append("ФАКТЫ")
        lines.append("------")

        for key, data in facts.items():
            if isinstance(data, dict) and "value" in data:
                lines.append(f"{key} = {data['value']}")

        lines.append("")

    projects = profile.get("projects", {})
    if projects:
        lines.append("ПРОЕКТЫ")
        lines.append("--------")

        for key, data in projects.items():
            if isinstance(data, dict) and "value" in data:
                lines.append(f"{key} = {data['value']}")

    return "\n".join(lines)
if __name__ == "__main__":
    rebuild_user_memory()
    print("PROFILE_MANAGER_OK")






def add_skill(skill_name, level=1.0):
    profile = load_profile()

    if "skills" not in profile:
        profile["skills"] = {}

    profile["skills"][skill_name] = {
        "value": level,
        "confidence": 1.0,
        "updated_at": _now()
    }

    save_profile(profile)


def list_skills():
    profile = load_profile()
    return profile.get("skills", {})


def get_skills_summary():
    profile = load_profile()

    lines = []
    lines.append("НАВЫКИ")
    lines.append("------")

    skills = profile.get("skills", {})

    for k, v in skills.items():
        if isinstance(v, dict) and "value" in v:
            lines.append(f"{k} = {v['value']}")

    return "\n".join(lines)







def list_episodes():
    profile = load_profile()
    return profile.get("episodes", [])


def get_episodes_summary():
    profile = load_profile()

    lines = []
    lines.append("EPISODES")
    lines.append("---------")

    for ep in profile.get("episodes", [])[-20:]:
        lines.append(f"{ep['time']} - {ep['text']}")

    return "\n".join(lines)




def add_episode(text):
    profile = load_profile()

    if 'episodes' not in profile or not isinstance(profile['episodes'], list):
        profile['episodes'] = []

    profile['episodes'].append({
        'text': text,
        'time': _now()
    })

    save_profile(profile)
    save_profile(profile)
