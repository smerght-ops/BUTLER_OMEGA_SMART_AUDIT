import time
from A_01_CORE.orchestrator import MainOrchestrator
from A_03_ORCHESTRATION.worker import Worker

def run_pipeline():
    print("[PIPELINE] === СТАРТ КОНВЕЙЕРА БАТЛЕР-ОМЕГА ===")
    
    # Шаг 1: Запуск Оркестратора для сбора новых файлов
    print("[PIPELINE] Шаг 1: Запуск Оркестратора (Сканирование папки incoming)...")
    orchestrator = MainOrchestrator()
    orchestrator.run()
    print("[PIPELINE] Оркестратор завершил постановку задач в очередь.")
    
    # Шаг 2: Запуск Воркера для обработки очереди jobs
    print("\n[PIPELINE] Шаг 2: Инициализация Воркера и разбор очереди jobs...")
    worker = Worker()
    
    processed_count = 0
    while True:
        # Воркер обрабатывает по одной задаче за раз
        has_job = worker.process_once()
        if not has_job:
            break
        processed_count += 1
        time.sleep(1)  # Небольшая пауза между задачами
        
    print(f"\n[PIPELINE] === КОНВЕЙЕР ЗАВЕРШЕН === Обработано задач: {processed_count}")

if __name__ == '__main__':
    run_pipeline()
