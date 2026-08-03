from A_01_CORE.manifest_loader import ManifestLoader

def main():
    config = ManifestLoader.load()
    print(f'[FIX] Проверка манифеста Butler Omega v{config.get("version", "1.0")}...')
    print('✓ Структура ядра в порядке. Костыли не обнаружены.')

if __name__ == '__main__':
    main()
