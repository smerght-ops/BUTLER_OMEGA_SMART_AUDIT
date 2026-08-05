# -*- coding: utf-8 -*-
import requests
import json

OLLAMA_URL = "http://127.0.0.1:11434"

def get_models():
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
        response.raise_for_status()
        return response.json().get("models", [])
    except Exception as e:
        print(f"[ERROR] Не удалось получить список моделей: {e}")
        return []

def print_models(models):
    print("\n=== AVAILABLE OLLAMA MODELS ===")
    for i, m in enumerate(models):
        print(f"{i+1}. {m.get('name', 'unknown')} | {m.get('size', 'unknown')}")
    print("================================\n")

def pick_light_model(models):
    if not models: return None
    keywords = ["tiny", "small", "phi", "llama", "gemma", "qwen"]
    for m in models:
        if any(k in m.get("name", "").lower() for k in keywords):
            return m.get("name")
    return models[0].get("name")

def chat(model, prompt):
    try:
        payload = {"model": model, "prompt": prompt, "stream": False}
        response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=60)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        return f"[ERROR] Запрос не выполнен: {e}"

def main():
    print("\n[OLLAMA BRIDGE INIT] Connecting to local runtime...\n")
    models = get_models()
    if not models:
        print("[FATAL] Модели не найдены или Ollama не запущен.")
        return
    print_models(models)
    model_name = pick_light_model(models)
    if not model_name: return
    print(f"[SELECTED MODEL] {model_name}\n")
    test_prompt = "Привет, Батлер на связи"
    print(f"[REQUEST] {test_prompt}\n")
    print("=== MODEL RESPONSE ===")
    print(chat(model_name, test_prompt))
    print("======================\n")

if __name__ == "__main__":
    main()
