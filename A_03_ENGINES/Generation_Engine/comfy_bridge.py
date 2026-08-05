# -*- coding: utf-8 -*-
import os
import time
import shutil
import requests
from pathlib import Path

class ComfyUIBridge:
    def __init__(self, server_address="127.0.0.1:8188"):
        self.server_address = server_address
        self.comfy_url = f"http://{server_address}/prompt"
        self.output_dir = Path(r"D:\AI_Studio\ComfyUI_windows_portable\ComfyUI\output")
        self.desktop_output = Path(r"C:\Users\KOS\Desktop\BUTLER_OUTPUT")

        # Гарантируем создание папки на рабочем столе
        self.desktop_output.mkdir(parents=True, exist_ok=True)

    def check_comfy_status(self):
        """Проверка доступности ComfyUI"""
        try:
            response = requests.get(f"http://{self.server_address}/object_info", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def generate_image(self, prompt_text, checkpoint_name="juggernautXL_ragnarok.safetensors"):
        """Отправка проверенного SDXL JSON-воркфлоу в API ComfyUI"""
        print(f"[*] Инициализация генерации. Промпт: '{prompt_text}'")

        if not self.check_comfy_status():
            print(f"[-] Ошибка: ComfyUI не доступен на http://{self.server_address}")
            return False

        # Твой эталонный рабочий воркфлоу (JuggernautXL)
        workflow = {
            "4": {
                "inputs": {
                    "ckpt_name": checkpoint_name
                },
                "class_type": "CheckpointLoaderSimple"
            },
            "6": {
                "inputs": {
                    "text": prompt_text,
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "7": {
                "inputs": {
                    "text": "text, watermark, low quality, blurry, deformed anatomy, bad hands, bad quality, low resolution",
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "5": {
                "inputs": {
                    "width": 1024,
                    "height": 1024,
                    "batch_size": 1
                },
                "class_type": "EmptyLatentImage"
            },
            "3": {
                "inputs": {
                    "seed": int(time.time()),
                    "steps": 25,
                    "cfg": 7.0,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1.0,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0]
                },
                "class_type": "KSampler"
            },
            "8": {
                "inputs": {
                    "samples": ["3", 0],
                    "vae": ["4", 2]
                },
                "class_type": "VAEDecode"
            },
            "9": {
                "inputs": {
                    "filename_prefix": "Butler_Channeled_Gen",
                    "images": ["8", 0]
                },
                "class_type": "SaveImage"
            }
        }

        try:
            # Фиксируем состояние папки до рендера
            files_before = set(os.listdir(self.output_dir)) if self.output_dir.exists() else set()

            print("[*] Отправка стабильной XL-матрицы в рантайм ComfyUI...")
            response = requests.post(self.comfy_url, json={"prompt": workflow}, timeout=30)
            response.raise_for_status()

            prompt_id = response.json().get("prompt_id")
            print(f"[✓] Задача в очереди ComfyUI. ID: {prompt_id}")
            print("[*] Ожидание рендера на RTX 3090 Ti...")

            # Цикл ожидания готового файла (60 секунд)
            for _ in range(60):
                time.sleep(1)
                if not self.output_dir.exists():
                    continue

                files_after = set(os.listdir(self.output_dir))
                new_files = files_after - files_before

                for name in new_files:
                    if name.startswith("Butler_Channeled_Gen") and name.endswith(".png"):
                        src = self.output_dir / name
                        dst = self.desktop_output / name

                        # Копируем на рабочий стол
                        shutil.copy2(src, dst)
                        print(f"[OK] Генерация успешна! Файл скопирован: {dst}")

                        # Автооткрытие картинки в Windows
                        os.startfile(str(dst))
                        return True

            print("[-] Ошибка: Превышено время ожидания рендера.")
            return False

        except Exception as e:
            print(f"[-] Критическая ошибка моста: {e}")
            return False

if __name__ == "__main__":
    bridge = ComfyUIBridge()
    bridge.generate_image("A futuristic cybernetic butler, high tech, 8k resolution, cinematic lighting")
