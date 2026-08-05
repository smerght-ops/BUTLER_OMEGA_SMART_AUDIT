from A_03_ENGINES.Vision_Engine.GO import process_image
from pathlib import Path

# Укажи путь к любому PDF, который у тебя лежит в WORKSPACE
test_file = Path('A_06_WORKSPACE/test_scan.pdf')

if test_file.exists():
    print(f'Running check on: {test_file.name}')
    result = process_image(test_file)
    print('--- RESULT ---')
    print(result[:200]) # Вывод первых 200 символов
else:
    print('Place a file named test_scan.pdf in A_06_WORKSPACE to run the test.')
