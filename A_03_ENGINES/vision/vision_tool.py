import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config, requests
def main():
    print(f'[VISION] Модель: {config.VISION_MODEL}')
if __name__ == '__main__':
    main()
