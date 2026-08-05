# -*- coding: utf-8 -*-

import time
import os
from datetime import datetime
from A_07_MEMORY.memory_facade_v2 import MemoryFacadeV2


LOG_PATH = ".\\A_08_LOGS\\butler_system.log"


class MemorySidecar:
    """
    External log-based observer.
    Reads system log file ONLY.
    No dependency on chat_router, RouterIntegration or runtime.
    """

    def __init__(self):
        self.memory = MemoryFacadeV2()
        self.last_position = 0
        self.running = True

    def parse_line(self, line: str):
        """
        Extract user input lines only:
        Format: 'Виктор > text'
        """
        try:
            if "Виктор >" in line:
                return line.split("Виктор >")[1].strip()
        except Exception:
            pass
        return None

    def run_loop(self):
        """
        File-tail observer loop (like 'tail -f')
        """
        print("[SIDECAR] Log observer started...")

        while self.running:
            try:
                if not os.path.exists(LOG_PATH):
                    time.sleep(1)
                    continue

                with open(LOG_PATH, "r", encoding="utf-8", errors="ignore") as f:
                    f.seek(self.last_position)

                    lines = f.readlines()
                    self.last_position = f.tell()

                for line in lines:
                    user_text = self.parse_line(line)

                    if user_text:
                        self.memory.add_event(
                            event=user_text,
                            meta={
                                "source": "butler_system.log",
                                "timestamp": datetime.now().isoformat()
                            }
                        )
                        print(f"[SIDECAR] captured: {user_text}")

                time.sleep(0.5)

            except Exception as e:
                print(f"[SIDECAR ERROR] {str(e)}")
                time.sleep(1)


# =========================
# STANDALONE EXECUTION
# =========================

if __name__ == "__main__":
    sidecar = MemorySidecar()
    sidecar.run_loop()
