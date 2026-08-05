# -*- coding: utf-8 -*-

import argparse
import json
import os
import time
from pathlib import Path

try:
    import requests
except Exception:
    import sys
    sys.modules['requests'] = None
    requests = None

# Импортируем единую интеграционную шину
from A_03_ORCHESTRATION.router_integration import RouterIntegration

OLLAMA_BASE = os.environ.get("BUTLER_OLLAMA_BASE", "http://localhost:11434")
OLLAMA_GENERATE = OLLAMA_BASE.rstrip("/") + "/api/generate"
OLLAMA_TAGS = OLLAMA_BASE.rstrip("/") + "/api/tags"

COMFYUI_BASE = os.environ.get("BUTLER_COMFYUI_BASE", "http://127.0.0.1:8188")

ARTISTS = {
    "1": ("Художник Хоррор", "DeepSeek-GPU:latest"),
    "2": ("Выдумщик", "gemma-4:latest"),
    "3": ("Художник Технарь", "ibm-granite_granite-4.1-30b-Q5_K_S:latest"),
}

TEXT_MODELS = {
    "1": ("Qwen35 RU", "qwen35-ru:latest"),
    "2": ("Qwen 2.5 VL", "qwen2.5-vl:latest"),
    "3": ("DeepSeek Coder", "DeepSeek-Coder-V2-Lite-Instruct-Q6_K:latest"),
    "4": ("Codestral", "codestral:latest"),
}

DRAW_TRIGGERS = [
    "нарисуй мне",
    "нарисуй",
    "сгенерируй",
    "сделай фото",
    "создай картинку",
    "создай изображение",
    "сделай картинку",
]

EXIT_WORDS = {"выход", "exit", "quit", "q"}


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def fetch_ollama_models():
    if requests is None:
        return set(), "requests module is not installed"
    try:
        res = requests.get(OLLAMA_TAGS, timeout=5)
        if res.status_code == 200:
            return {m["name"] for m in res.json().get("models", [])}, None
        return set(), f"Ollama error: {res.status_code}"
    except Exception as e:
        return set(), str(e)


def check_comfyui():
    if requests is None:
        return False, "requests missing"
    try:
        res = requests.get(COMFYUI_BASE, timeout=3)
        return (True, "ONLINE") if res.status_code == 200 else (False, f"Status {res.status_code}")
    except Exception as e:
        return False, str(e)


def print_status():
    print("=" * 70)
    print("   ИНТЕРФЕЙС УПРАВЛЕНИЯ ЛОКАЛЬНЫМИ МОДЕЛЯМИ ЧАТА")
    print("=" * 70)
    models, err = fetch_ollama_models()
    if err:
        print(f"[*] Ollama: Сбой проверки доступности -> {err}")
    else:
        print(f"[*] Ollama: Доступно локальных моделей -> {len(models)}")
    
    comfy_ok, comfy_msg = check_comfyui()
    print(f"[*] ComfyUI: Состояние генератора картинок -> {comfy_msg}")
    print("=" * 70)
    return models


def choose_model(available_models, model_dict, prompt_text):
    print(prompt_text)
    valid_options = {}
    for idx, (label, m_name) in model_dict.items():
        status = "[ОФЛАЙН]" if available_models and m_name not in available_models else "[ОК]"
        print(f"  {idx} -> {label} ({m_name}) {status}")
        valid_options[idx] = (label, m_name)
    
    choice = input("Выбор > ").strip()
    return valid_options.get(choice, None)


def ask_ollama(model_name, prompt, timeout=120):
    if requests is None:
        raise RuntimeError("requests module missing")
    payload = {"model": model_name, "prompt": prompt, "stream": False}
    res = requests.post(OLLAMA_GENERATE, json=payload, timeout=timeout)
    if res.status_code == 200:
        return res.json().get("response", "")
    raise RuntimeError(f"Ollama error {res.status_code}: {res.text}")


def handle_draw(text, models):
    clean_text = text.lower()
    is_draw = any(trigger in clean_text for trigger in DRAW_TRIGGERS)
    if not is_draw:
        return False

    selected = choose_model(models, ARTISTS, "[?] Выберите художника для генерации промпта ComfyUI:")
    if not selected:
        print("[-] Отменено пользователем.")
        return True

    role_name, model_name = selected
    system_instruction = (
        "Ты профессиональный prompt-engineer для Stable Diffusion / ComfyUI.\n"
        "Твоя задача — перевести запрос пользователя на английский язык, детализировать его, "
        "добавить стили, освещение, проработать детали фасадов или окружения.\n"
        "Выдавай СТРОГО финальный промпт на английском языке. Никаких вводных слов и объяснений!"
    )
    
    clean_prompt = text
    for t in DRAW_TRIGGERS:
        clean_prompt = clean_prompt.replace(t, "")
    clean_prompt = clean_prompt.strip()

    final_prompt = f"{system_instruction}\n\nЗапрос: {clean_prompt}"

    print()
    print(f"[*] Батлер: подключаю [{role_name}] / {model_name}")
    print("[*] Генерация промпта для ComfyUI...")

    start = time.time()
    try:
        result = ask_ollama(model_name, final_prompt, timeout=120)
        elapsed = time.time() - start

        export_dir = Path("A_06_WORKSPACE") / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        out_file = export_dir / "last_comfy_prompt.txt"
        out_file.write_text(result, encoding="utf-8")

        # === ЧИСТЫЙ АРХИТЕКТУРНЫЙ МОСТ ВЕХИ 4.15.4 ===
        try:
            from A_03_ORCHESTRATION.dispatcher_bridge_v2 import dispatch
            from A_03_ORCHESTRATION.permission import DepartmentExecutionGateway
            from A_04_AGENTS.ImageDepartment.runner import ImageDepartment
            print("\n[*] Роутер: Активирую контур IMAGE напрямую...")
            
            # Image уже выбран: вызываем его через permission gateway
            img_dept = ImageDepartment()
            dispatch_result = DepartmentExecutionGateway().execute(
                img_dept, f"нарисуй {result}"
            )
            
            print("\n" + "="*50)
            print("[✓] РЕЗУЛЬТАТ ГЕНЕРАЦИИ КОНТУРА:")
            print(dispatch_result)
            print("="*50 + "\n")
        except Exception as bridge_err:
            print(f"[!] Ошибка конвейера генерации: {bridge_err}")

        print(f"[OK] {role_name} отработал за {elapsed:.2f} сек.")
        print()
        print("ФИНАЛЬНЫЙ PROMPT ДЛЯ COMFYUI:")
        print("-" * 70)
        print(result)
        print("-" * 70)
        print(f"[OK] Prompt сохранён: {out_file}")
    except Exception as exc:
        print(f"[-] Ошибка генерации: {exc}")

    return True


def handle_chat(text, models):
    selected = choose_model(models, TEXT_MODELS, "[?] Выберите модель для обычного чата:")
    if not selected:
        return

    role_name, model_name = selected
    memory_file = Path(__file__).resolve().parent.parent / "A_05_STORAGE" / "USER_MEMORY.md"
    memory_text = memory_file.read_text(encoding="utf-8-sig") if memory_file.exists() else ""

    prompt = (
        "Ты локальный помощник Butler Omega. Используй долговременную память как источник истины о пользователе. Отвечай по-русски, понятно и по делу.\n\n"
        + "=== ДОЛГОВРЕМЕННАЯ ПАМЯТЬ ===\n"
        + memory_text
        + "\n\n=== ВОПРОС ПОЛЬЗОВАТЕЛЯ ===\n"
        + text
    )

    print()
    print(f"[*] Батлер: подключаю [{role_name}] / {model_name}")
    start = time.time()

    try:
        result = ask_ollama(model_name, prompt, timeout=120)
        elapsed = time.time() - start
        print(f"[OK] Ответ за {elapsed:.2f} сек.")
        print("-" * 70)
        print(result)
        print("-" * 70)
    except Exception as exc:
        print(f"[-] Ошибка чата: {exc}")


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

    # Инициализируем диспетчер интеграции
    router_bus = RouterIntegration()

    print("Команды:")
    print("  обычный вопрос       -> выбор текстовой модели")
    print("  нарисуй тигра        -> выбор художника и генерация prompt для ComfyUI")
    print("  кто ты / что сделано -> мгновенный ответ системной памяти проекта")
    print("  выход / q            -> выход")
    print("=" * 70)

    while True:
        user_text = input("\nВиктор > ").strip()

        if not user_text:
            continue

        if user_text.lower() in EXIT_WORDS:
            print("[*] Выход из Butler Chat Router.")
            break

        # СЛОЙ ПЕРЕХВАТА СИСТЕМНЫХ КОМАНД (Паспорт + История)
        # Если роутер вернул не дефолтный fallback и перехватил команду — выводим на экран
        response = router_bus.dispatch(user_text)
        system_markers = [
            "BUTLER OMEGA SMART PASSPORT",
            "PROJECT OMEGA SMART MEMORY",
            "NEXT ROADMAP TASKS",
            "СВОДКА ИСТОРИИ",
            "ФАКТИЧЕСКИЙ СТАТУС",
            "СЛЕДУЮЩИЙ ШАГ"
        ]
        if "[Fallback]" not in response and any(marker in response for marker in system_markers):
            print(response)
            continue

        models, _ = fetch_ollama_models()

        if handle_draw(user_text, models):
            continue

        handle_chat(user_text, models)


if __name__ == "__main__":
    main()

