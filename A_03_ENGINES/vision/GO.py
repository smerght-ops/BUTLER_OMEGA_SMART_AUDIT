import sys, os, requests, base64
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def process_image(image_path):
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    
    payload = {
        "model": config.VISION_MODEL,
        "messages": [
            {"role": "system", "content": "Ты - помощник, который отвечает ИСКЛЮЧИТЕЛЬНО на русском языке."},
            {"role": "user", "content": "Опиши это изображение максимально подробно на русском языке.", "images": [data]}
        ],
        "stream": False
    }
    
    try:
        r = requests.post(config.OLLAMA_URL, json=payload, timeout=600)
        if r.status_code == 200:
            return r.json().get("message", {}).get("content", "Нет данных")
        else:
            return f"API Error {r.status_code}: {r.text}"
    except Exception as e:
        return f"Критическая ошибка: {str(e)}"