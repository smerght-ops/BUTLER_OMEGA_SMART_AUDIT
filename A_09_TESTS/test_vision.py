from A_01_CORE.manifest_loader import ManifestLoader
from A_03_ENGINES.Vision_Engine.GO import process_image

def main():
    config = ManifestLoader.load()
    print('[TEST] Инициализация диагностического теста для qwen2.5-vl...')
    print(f'✓ Связь с манифестом установлена. Движок готов к проверке.')

if __name__ == '__main__':
    main()
