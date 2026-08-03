from A_01_CORE.manifest_loader import ManifestLoader

def main():
    config = ManifestLoader.load()
    model = config.get("vision_model", "qwen2.5-vl:latest")
    endpoint = config.get("ollama_url", "http://127.0.0.1:11434/api/chat")

    print(f'[VISION TOOL] Инспекция движка зрения:')
    print(f'  |-- Активная модель: {model}')
    print(f'  |-- Точка подключения: {endpoint}')

if __name__ == '__main__':
    main()
