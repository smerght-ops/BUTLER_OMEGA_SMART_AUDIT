import argparse
import json
import os
import time
from pathlib import Path
from A_03_ORCHESTRATION.hybrid_resolver import HybridResolver

try:
    import requests
except Exception:
    requests = None

OLLAMA_BASE = os.environ.get("BUTLER_OLLAMA_BASE", "http://localhost:11434")
OLLAMA_GENERATE = OLLAMA_BASE.rstrip("/") + "/api/generate"
OLLAMA_TAGS = OLLAMA_BASE.rstrip("/") + "/api/tags"

COMFYUI_BASE = os.environ.get("BUTLER_COMFYUI_BASE", "http://127.0.0.1:8188")

ARTISTS = {
    "1": ("РҐСѓРґРѕР¶РЅРёРє РҐРѕСЂСЂРѕСЂ", "DeepSeek-GPU:latest"),
    "2": ("Р’С‹РґСѓРјС‰РёРє", "gemma-4:latest"),
    "3": ("РҐСѓРґРѕР¶РЅРёРє РўРµС…РЅР°СЂСЊ", "ibm-granite_granite-4.1-30b-Q5_K_S:latest"),
}

TEXT_MODELS = {
    "1": ("Qwen35 RU", "qwen35-ru:latest"),
    "2": ("Qwen 2.5 VL", "qwen2.5-vl:latest"),
    "3": ("DeepSeek Coder", "DeepSeek-Coder-V2-Lite-Instruct-Q6_K:latest"),
    "4": ("Codestral", "codestral:latest"),
}

DRAW_TRIGGERS = [
    "РЅР°СЂРёСЃСѓР№ РјРЅРµ",
    "РЅР°СЂРёСЃСѓР№",
    "СЃРіРµРЅРµСЂРёСЂСѓР№",
    "СЃРґРµР»Р°Р№ С„РѕС‚Рѕ",
    "СЃРѕР·РґР°Р№ РєР°СЂС‚РёРЅРєСѓ",
    "СЃРѕР·РґР°Р№ РёР·РѕР±СЂР°Р¶РµРЅРёРµ",
    "СЃРґРµР»Р°Р№ РєР°СЂС‚РёРЅРєСѓ",
]

EXIT_WORDS = {"РІС‹С…РѕРґ", "exit", "quit", "q"}


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def fetch_ollama_models():
    if requests is None:
        return set(), "requests module is not installed"

    try:
        response = requests.get(OLLAMA_TAGS, timeout=5)
        response.raise_for_status()
        data = response.json()
        names = set()
        for item in data.get("models", []):
            name = item.get("name")
            if name:
                names.add(name)
        return names, None
    except Exception as exc:
        return set(), str(exc)


def check_comfyui():
    if requests is None:
        return False, "requests module is not installed"

    try:
        response = requests.get(COMFYUI_BASE.rstrip("/") + "/system_stats", timeout=3)
        if response.status_code == 200:
            return True, "ComfyUI API online"
        return False, f"HTTP {response.status_code}"
    except Exception as exc:
        return False, str(exc)


def ask_ollama(model, prompt, timeout=90):
    if requests is None:
        raise RuntimeError("requests module is not installed")

    response = requests.post(
        OLLAMA_GENERATE,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
        },
        timeout=timeout,
    )
    response.raise_for_status()
    response = response.json().get("response", "").strip(); import re; response = re.sub(r"<think>.*?</think>\s*", "", response, flags=re.DOTALL | re.IGNORECASE); return response.strip()


def is_draw_command(text):
    lower = text.lower().strip()
    for trigger in DRAW_TRIGGERS:
        if lower.startswith(trigger):
            return True, text[len(trigger):].strip()
    return False, text


def print_status():
    models, err = fetch_ollama_models()
    comfy_ok, comfy_reason = check_comfyui()

    print("=" * 70)
    print(" BUTLER OMEGA CHAT ROUTER")
    print("=" * 70)

    if err:
        print(f"[!] Ollama: OFFLINE / {err}")
    else:
        print("[OK] Ollama: ONLINE")

    print()
    print("TEXT MODELS:")
    for key, (role, model) in TEXT_MODELS.items():
        mark = "[OK]" if model in models else "[--]"
        print(f"  {mark} [{key}] {role:<16} {model}")

    print()
    print("ARTIST MODELS:")
    for key, (role, model) in ARTISTS.items():
        mark = "[OK]" if model in models else "[--]"
        print(f"  {mark} [{key}] {role:<18} {model}")

    print()
    if comfy_ok:
        print("[OK] ComfyUI: ONLINE")
    else:
        print(f"[--] ComfyUI: OFFLINE / {comfy_reason}")

    print("=" * 70)
    return models


def choose_model(models, registry, title):
    print()
    print(title)
    for key, (role, model) in registry.items():
        mark = "OK" if model in models else "--"
        print(f"  [{key}] {role} ({model}) [{mark}]")

    choice = input("Р’Р°С€ РІС‹Р±РѕСЂ: ").strip()
    if choice not in registry:
        print("[-] РќРµРІРµСЂРЅС‹Р№ РІС‹Р±РѕСЂ.")
        return None

    role, model = registry[choice]
    if models and model not in models:
        print(f"[!] Р’РЅРёРјР°РЅРёРµ: РјРѕРґРµР»СЊ РЅРµ РЅР°Р№РґРµРЅР° РІ ollama list: {model}")
        use_anyway = input("РџСЂРѕР±РѕРІР°С‚СЊ РІСЃС‘ СЂР°РІРЅРѕ? y/n: ").strip().lower()
        if use_anyway not in {"y", "yes", "Рґ", "РґР°"}:
            return None

    return role, model


def handle_draw(text, models):
    is_draw, clean_prompt = is_draw_command(text)

    if not is_draw:
        return False

    if not clean_prompt:
        print("[-] Р‘Р°С‚Р»РµСЂ: Р§С‚Рѕ РёРјРµРЅРЅРѕ РЅР°СЂРёСЃРѕРІР°С‚СЊ?")
        return True

    selected = choose_model(models, ARTISTS, "[?] Р’С‹Р±РµСЂРёС‚Рµ РјР°СЃС‚РµСЂР° РґР»СЏ СЃРѕР·РґР°РЅРёСЏ РїСЂРѕРјРїС‚Р° ComfyUI:")
    if not selected:
        return True

    role_name, model_name = selected

    system_instruction = (
        "РўС‹ СЌРєСЃРїРµСЂС‚ РїРѕ СЃРѕР·РґР°РЅРёСЋ РїСЂРѕРјРїС‚РѕРІ РґР»СЏ ComfyUI. "
        "РџРµСЂРµРІРµРґРё СЂСѓСЃСЃРєРёР№ Р·Р°РїСЂРѕСЃ РЅР° Р°РЅРіР»РёР№СЃРєРёР№. "
        "Р•СЃР»Рё СЌС‚Рѕ РіРёР±СЂРёРґ, СЃРѕР·РґР°Р№ РѕРїРёСЃР°РЅРёРµ С„Р°РЅС‚Р°СЃС‚РёС‡РµСЃРєРѕРіРѕ СЃСѓС‰РµСЃС‚РІР°, РѕР±СЉРµРґРёРЅСЏСЋС‰РµРіРѕ С‡РµСЂС‚С‹ РѕР±РѕРёС… Р¶РёРІРѕС‚РЅС‹С…. "
        "Р”РѕР±Р°РІСЊ РґРµС‚Р°Р»Рё: photorealism, cinematic light, high detail, sharp focus, dramatic composition. "
        "Р’С‹РґР°Р№ РўРћР›Р¬РљРћ РіРѕС‚РѕРІС‹Р№ Р°РЅРіР»РёР№СЃРєРёР№ РїСЂРѕРјРїС‚ Р±РµР· РїРѕСЏСЃРЅРµРЅРёР№."
    )

    final_prompt = f"{system_instruction}\n\nР—Р°РїСЂРѕСЃ: {clean_prompt}"

    print()
    print(f"[*] Р‘Р°С‚Р»РµСЂ: РїРѕРґРєР»СЋС‡Р°СЋ [{role_name}] / {model_name}")
    print("[*] Р“РµРЅРµСЂР°С†РёСЏ РїСЂРѕРјРїС‚Р° РґР»СЏ ComfyUI...")

    start = time.time()
    try:
        result = ask_ollama(model_name, final_prompt, timeout=120)
        elapsed = time.time() - start

        export_dir = Path("A_06_WORKSPACE") / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        out_file = export_dir / "last_comfy_prompt.txt"
        out_file.write_text(result, encoding="utf-8")

        print(f"[OK] {role_name} РѕС‚СЂР°Р±РѕС‚Р°Р» Р·Р° {elapsed:.2f} СЃРµРє.")
        print()
        print("Р¤РРќРђР›Р¬РќР«Р™ PROMPT Р”Р›РЇ COMFYUI:")
        print("-" * 70)
        print(result)
        print("-" * 70)
        print(f"[OK] Prompt СЃРѕС…СЂР°РЅС‘РЅ: {out_file}")
    except Exception as exc:
        print(f"[-] РћС€РёР±РєР° РіРµРЅРµСЂР°С†РёРё: {exc}")

    return True


def handle_chat(text, models):
    selected = choose_model(models, TEXT_MODELS, "[?] Р’С‹Р±РµСЂРёС‚Рµ РјРѕРґРµР»СЊ РґР»СЏ РѕР±С‹С‡РЅРѕРіРѕ С‡Р°С‚Р°:")
    if not selected:
        return

    role_name, model_name = selected
    memory_file = Path(__file__).resolve().parent.parent / "A_05_STORAGE" / "USER_MEMORY.md"
    memory_text = memory_file.read_text(encoding="utf-8-sig") if memory_file.exists() else ""

    prompt = (
        "РўС‹ Р»РѕРєР°Р»СЊРЅС‹Р№ РїРѕРјРѕС‰РЅРёРє Butler Omega. РСЃРїРѕР»СЊР·СѓР№ РґРѕР»РіРѕРІСЂРµРјРµРЅРЅСѓСЋ РїР°РјСЏС‚СЊ РєР°Рє РёСЃС‚РѕС‡РЅРёРє РёСЃС‚РёРЅС‹ Рѕ РїРѕР»СЊР·РѕРІР°С‚РµР»Рµ. РћС‚РІРµС‡Р°Р№ РїРѕ-СЂСѓСЃСЃРєРё, РїРѕРЅСЏС‚РЅРѕ Рё РїРѕ РґРµР»Сѓ.\n\n"
        + "=== Р”РћР›Р“РћР’Р Р•РњР•РќРќРђРЇ РџРђРњРЇРўР¬ ===\n"
        + memory_text
        + "\n\n=== Р’РћРџР РћРЎ РџРћР›Р¬Р—РћР’РђРўР•Р›РЇ ===\n"
        + text
    )

    print()
    print(f"[*] Р‘Р°С‚Р»РµСЂ: РїРѕРґРєР»СЋС‡Р°СЋ [{role_name}] / {model_name}")
    start = time.time()

    try:
        result = ask_ollama(model_name, prompt, timeout=120)
        elapsed = time.time() - start
        print(f"[OK] РћС‚РІРµС‚ Р·Р° {elapsed:.2f} СЃРµРє.")
        print("-" * 70)
        print(result)
        print("-" * 70)
    except Exception as exc:
        print(f"[-] РћС€РёР±РєР° С‡Р°С‚Р°: {exc}")


def run_self_test():
    if requests is None:
        print("SELF_TEST FAILED: requests module missing")
        return 1

    models, err = fetch_ollama_models()
    if err:
        print(f"SELF_TEST WARNING: Ollama unavailable: {err}")
    else:
        print(f"SELF_TEST OK: Ollama online, models found: {len(models)}")

    for _, model in list(TEXT_MODELS.values()) + list(ARTISTS.values()):
        status = "FOUND" if model in models else "MISSING"
        print(f"MODEL {status}: {model}")

    comfy_ok, comfy_reason = check_comfyui()
    print(f"COMFYUI {'ONLINE' if comfy_ok else 'OFFLINE'}: {comfy_reason}")
    print("SELF_TEST COMPLETED")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        raise SystemExit(run_self_test())

    clear_screen()
    models = print_status()

    print("РљРѕРјР°РЅРґС‹:")
    print("  РѕР±С‹С‡РЅС‹Р№ РІРѕРїСЂРѕСЃ       -> РІС‹Р±РѕСЂ С‚РµРєСЃС‚РѕРІРѕР№ РјРѕРґРµР»Рё")
    print("  РЅР°СЂРёСЃСѓР№ С‚РёРіСЂР°РєСЂС‹СЃСѓ  -> РІС‹Р±РѕСЂ С…СѓРґРѕР¶РЅРёРєР° Рё РіРµРЅРµСЂР°С†РёСЏ prompt РґР»СЏ ComfyUI")
    print("  РІС‹С…РѕРґ / q            -> РІС‹С…РѕРґ")
    print("=" * 70)

    while True:
        user_text = input("\nР’РёРєС‚РѕСЂ > ").strip()

        if not user_text:
            continue

        if user_text.lower() in EXIT_WORDS:
            print("[*] Р’С‹С…РѕРґ РёР· Butler Chat Router.")
            break

        models, _ = fetch_ollama_models()

        if handle_draw(user_text, models):
            continue

        handle_chat(user_text, models)


if __name__ == "__main__":
    main()
