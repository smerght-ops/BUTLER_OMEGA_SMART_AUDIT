import urllib.request
import json

url = "http://127.0.0.1:8188/prompt"

# Обновленный, пуленепробиваемый воркфлоу для свежих версий ComfyUI
workflow = {
    "4": {
        "inputs": {
            "ckpt_name": "juggernautXL_ragnarok.safetensors"
        },
        "class_type": "CheckpointLoaderSimple"
    },
    "6": {
        "inputs": {
            "text": "A high-tech cybernetic robot butler, elegant silver suit, glowing blue eyes, photorealistic, masterpiece, 8k resolution, cinematic lighting",
            "clip": ["4", 1]
        },
        "class_type": "CLIPTextEncode"
    },
    "7": {
        "inputs": {
            "text": "text, watermark, low quality, blurry",
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
            "seed": 42,
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
            "filename_prefix": "BUTLER_OMEGA_SMART_Final",
            "images": ["8", 0]
        },
        "class_type": "SaveImage"
    }
}

payload = {"prompt": workflow}
data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

try:
    print("[*] Отправляем обновленный приказ Художнику...")
    response = urllib.request.urlopen(req)
    print("[✓] УРА! Принято без ошибок! Срочно смотри в черное окно ComfyUI — там пошла жара!")
except Exception as e:
    print(f"[-] Ошибка отправки: {e}")
