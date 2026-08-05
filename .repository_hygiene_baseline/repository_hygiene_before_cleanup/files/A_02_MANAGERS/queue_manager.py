"""
=============================================================================
АРХИТЕКТУРНЫЙ ПАСПОРТ СВЯЗЕЙ МОДУЛЯ [queue_manager.py] (v1.1 Foundation)
=============================================================================
РОЛЬ: Менеджер распределения очередей задач и координации параллельных воркеров.
ВХОДНЫЕ СВЯЗИ (Кто вызывает этот модуль):
  <- [Внешние фоновые воркеры / Контейнеры] (Запрашивают следующую задачу)
ВЫХОДНЫЕ СВЯЗИ (К кому ведет дорога из этого модуля):
  -> [A_02_MANAGERS/catalog_manager.py] (Использует общую СУБД SQLite WAL)
  -> [A_01_CORE/manifest_loader.py] (Чтение параметров тайм-аута задач)
=============================================================================
"""

import sqlite3
import time
from pathlib import Path
from A_01_CORE.manifest_loader import ManifestLoader

class QueueManager:
    def __init__(self):
        print("[СВЯЗЬ] Инициализация QueueManager. Подключение к СУБД каталога...")
        self.PROJECT_ROOT = Path(__file__).resolve().parent.parent
        self.db_path = self.PROJECT_ROOT / "A_05_STORAGE" / "catalog.db"
        
        # Загружаем конфигурацию для таймаутов
        try:
            self.config = ManifestLoader.load()
            self.timeout_limit = self.config.get("worker_timeout_seconds", 600) # 10 минут по умолчанию
        except Exception:
            self.timeout_limit = 600

    def _get_connection(self):
        """Создает оптимизированное соединение с поддержкой WAL."""
        conn = sqlite3.connect(str(self.db_path), timeout=30.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def get_next_task(self, worker_id="default_worker"):
        """
        Бронебойный захват задачи с использованием транзакции BEGIN IMMEDIATE.
        Исключает Race Condition (состояние гонки) при работе нескольких воркеров.
        """
        # Сначала чистим зависшие воркеры
        self._recycle_dead_workers()

        conn = self._get_connection()
        try:
            # Выставляем эксклюзивную блокировку на запись прямо в начале транзакции
            conn.execute("BEGIN IMMEDIATE")
            
            cursor = conn.cursor()
            # Ищем первую задачу в очереди
            cursor.execute(
                "SELECT id, filepath FROM documents WHERE status='queued' ORDER BY registered_at ASC LIMIT 1"
            )
            row = cursor.fetchone()
            
            if row:
                doc_id, filepath = row
                current_time = int(time.time())
                
                # Мгновенно обновляем статус под конкретный воркер
                cursor.execute(
                    "UPDATE documents SET status='processing', updated_at=?, summary=? WHERE id=?",
                    (current_time, f"Worker: {worker_id}", doc_id)
                )
                conn.commit()
                print(f"[ОЧЕРЕДЬ -> {worker_id}] Успешно захвачена задача ID {doc_id}: {filepath}")
                return {"task_id": doc_id, "filepath": filepath}
                
            conn.commit() # Если задач нет, просто закрываем транзакцию
            return None
            
        except sqlite3.OperationalError as e:
            print(f"[-] База заблокирована параллельным процессом, ожидание: {e}")
            return None
        except Exception as e:
            print(f"[-] Критическая ошибка при захвате задачи из очереди: {e}")
            try:
                conn.rollback()
            except Exception:
                pass
            return None
        finally:
            conn.close()

    def _recycle_dead_workers(self):
        """Автоматически возвращает в очередь задачи, которые зависли в обработке дольше лимита."""
        conn = self._get_connection()
        try:
            conn.execute("BEGIN IMMEDIATE")
            cursor = conn.cursor()
            threshold_time = int(time.time()) - self.timeout_limit
            
            # Находим задачи, которые застряли в 'processing' и долго не обновлялись
            cursor.execute(
                "SELECT id, filepath FROM documents WHERE status='processing' AND updated_at < ?",
                (threshold_time,)
            )
            dead_tasks = cursor.fetchall()
            
            if dead_tasks:
                print(f"[СВЯЗЬ -> Восстановление] Обнаружено упавших/зависших задач: {len(dead_tasks)}")
                for doc_id, filepath in dead_tasks:
                    cursor.execute(
                        "UPDATE documents SET status='queued', updated_at=? WHERE id=?",
                        (int(time.time()), doc_id)
                    )
                    print(f"  -> Задача ID {doc_id} ({filepath}) возвращена в очередь.")
            conn.commit()
        except Exception as e:
            print(f"[-] Ошибка при циклической переработке упавших воркеров: {e}")
            try:
                conn.rollback()
            except Exception:
                pass
        finally:
            conn.close()
