# -*- coding: utf-8 -*-
import urllib.request
import json
import os
import time

def draw_by_command(user_input):
    ui_lower = user_input.strip().lower()
    if not (ui_lower.startswith("нарисуй") or ui_lower.startswith("создай картинку")):
        return False

    clean_p = ui_lower.replace("нарисуй мне", "").replace("нарисуй", "").replace("создай картинку", "").strip()
    if not clean_p:
        print("\n[-] Батлер: Что именно нарисовать? Пример: 'Нарисуй автомобиль'")
        return True

    OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
    COMFY_URL = "http://127.0.0.1:8188/prompt"
    OUTPUT_DIR = r"D:\AI_Studio\ComfyUI_windows_portable\ComfyUI_windows_portable\ComfyUI\output"

    print("\n[*] Батлер: Отправляю запрос в Ollama для адаптации промпта...")
    prompt_to_ollama = f"Переведи этот промпт на английский язык для генерации изображений в Stable Diffusion XL. Выдай ТОЛЬКО чистый английский перевод, без лишнего текста и комментариев: {clean_p}"
    ollama_data = json.dumps({"model": "qwen35-ru", "prompt": prompt_to_ollama, "stream": False}).encode('utf-8')

    try:
        req_ollama = urllib.request.Request(OLLAMA_URL, data=ollama_data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req_ollama) as response:
            res = json.loads(response.read().decode('utf-8'))
            eng_prompt = res.get('response', '').strip()
        print(f"[✓] Батлер: Сформирован английский промпт: {eng_prompt}")
    except Exception as e:
        print(f"[-] Батлер: Ошибка Ollama ({e})")
        eng_prompt = "A high-tech cybernetic robot butler, elegant silver suit, photorealistic, 8k resolution"

    workflow = {
        "4": {"inputs": {"ckpt_name": "juggernautXL_ragnarok.safetensors"}, "class_type": "CheckpointLoaderSimple"},
        "6": {"inputs": {"text": eng_prompt, "clip": ["4", 1]}, "class_type": "CLIPTextEncode"},
        "7": {"inputs": {"text": "text, watermark, low quality, blurry, deformed anatomy, bad hands", "clip": ["4", 1]}, "class_type": "CLIPTextEncode"},
        "5": {"inputs": {"width": 1024, "height": 1024, "batch_size": 1}, "class_type": "EmptyLatentImage"},
        "3": {
            "inputs": {
                "seed": int(time.time()), "steps": 25, "cfg": 7.0, "sampler_name": "euler", "scheduler": "normal", "denoise": 1.0,
                "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0]
            },
            "class_type": "KSampler"
        },
        "8": {"inputs": {"samples": ["3", 0], "vae": ["4", 2]}, "class_type": "VAEDecode"},
        "9": {"inputs": {"filename_prefix": "Butler_Channeled_Gen", "images": ["8", 0]}, "class_type": "SaveImage"}
    }

    try:
        files_before = set(os.listdir(OUTPUT_DIR)) if os.path.exists(OUTPUT_DIR) else set()
        payload = {"prompt": workflow}
        comfy_data = json.dumps(payload).encode('utf-8')
        req_comfy = urllib.request.Request(COMFY_URL, data=comfy_data, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req_comfy)
        print("[✓] Батлер: Задача принята Художником. Пошла генерация...")

        new_file_path = None
        for _ in range(60):
            time.sleep(1)
            files_after = set(os.listdir(OUTPUT_DIR)) if os.path.exists(OUTPUT_DIR) else set()
            new_files = files_after - files_before
            if new_files:
                for f in new_files:
                    if f.startswith("Butler_Channeled_Gen") and f.endswith(".png"):
                        new_file_path = os.path.join(OUTPUT_DIR, f)
                        break
            if new_file_path:
                break

        if new_file_path:
            print(f"\n[✓] Батлер: Рисунок готов!")
            os.system(f'explorer.exe /select,"{new_file_path}"')
        else:
            print("\n[-] Батлер: Тайм-аут генерации.")
    except Exception as e:
        print(f"\n[-] Ошибка ComfyUI: {e}")
    return True
