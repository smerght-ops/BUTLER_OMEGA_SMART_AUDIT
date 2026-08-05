import requests
import sys
from A_01_CORE.manifest_loader import ManifestLoader

sys.stdout.reconfigure(encoding='utf-8')

class ProviderManager:
    def __init__(self):
        config = ManifestLoader.load()
        self.base_url = config.get("ollama_url", "http://127.0.0.1:11434/api/chat").replace("/api/chat", "")
        self.vision_model = config.get("vision_model", "qwen2.5-vl:latest")
        self.analysis_model = config.get("analysis_model", "qwen-3_5:latest")

    def check_ollama_status(self):
        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code == 200:
                print("Ollama СЃРµСЂРІРµСЂ РґРѕСЃС‚СѓРїРµРЅ")
                return True
            return False
        except:
            print("РћС€РёР±РєР° РїРѕРґРєР»СЋС‡РµРЅРёСЏ Рє Ollama")
            return False

    def get_local_models(self):
        if not self.check_ollama_status():
            return []
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = [m["name"] for m in response.json().get("models", [])]
                return models
            return []
        except:
            return []

    def inspect_manifest_models(self):
        models = self.get_local_models()
        print(f"Р”РѕСЃС‚СѓРїРЅС‹Рµ РјРѕРґРµР»Рё: {models}")
        if self.analysis_model in models or f"{self.analysis_model}:latest" in models:
            print(f"РњРѕРґРµР»СЊ {self.analysis_model} РЅР°Р№РґРµРЅР°.")
            return True
        print(f"РњРѕРґРµР»СЊ {self.analysis_model} РќР• РЅР°Р№РґРµРЅР°.")
        return False

if __name__ == "__main__":
    pm = ProviderManager()
    pm.inspect_manifest_models()
