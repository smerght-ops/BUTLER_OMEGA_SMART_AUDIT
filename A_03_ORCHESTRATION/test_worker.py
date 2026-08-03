import sqlite3

from A_03_ORCHESTRATION.worker import Worker

worker = Worker()

worker.process_once()

print("SMOKE TEST DONE")