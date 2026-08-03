from A_01_CORE.manifest_loader import ManifestLoader

def main():
    config = ManifestLoader.load()
    print('[ALARM] Система контроля и безопасности включена.')

if __name__ == '__main__':
    main()
