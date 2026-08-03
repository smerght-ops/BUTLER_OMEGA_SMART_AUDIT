from A_01_CORE.manifest_loader import ManifestLoader

def main():
    config = ManifestLoader.load()
    print('[BILLS] Поиск и анализ счетов запущен.')

if __name__ == '__main__':
    main()