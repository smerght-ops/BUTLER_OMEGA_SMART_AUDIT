import sys, os, time
# Добавляем текущую папку в путь поиска модулей
sys.path.append(os.getcwd())

from A_04_AGENTS.professor import DispatcherAgent

agent = DispatcherAgent()
print("--- [ПРОФЕССОР] Демон запущен и ждет файлы ---")
while True:
    files = list(agent.workspace_dir.glob('*'))
    for f in files:
        if f.is_file():
            print(f"\n[!] Обнаружен файл: {f.name}")
            agent.process_agent_task(f.name, 'auto')
    time.sleep(5)
