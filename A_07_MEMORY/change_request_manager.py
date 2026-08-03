# -*- coding: utf-8 -*-

import re
import json
import hashlib
from datetime import datetime
from pathlib import Path


class ChangeRequestManager:
    """
    V3.1 Deterministic CR Engine:
    - hash-based identity
    - strict contract output
    - ledger-safe writes
    - idempotent protection
    """

    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[1]
        self.ledger_path = self.project_root / "A_08_LOGS" / "PROJECT_LEDGER.txt"

    def _normalize(self, request: str) -> str:
        return request.strip().upper()

    def _hash(self, request: str) -> str:
        return hashlib.sha256(request.encode("utf-8")).hexdigest()

    def is_already_proposed(self, lock_id: str) -> bool:
        if not self.ledger_path.exists():
            return False

        content = self.ledger_path.read_text(encoding="utf-8-sig")

        # Ищем строго 12-символьный LOCK_ID, который реально пишется в лог
        return f"LOCK_ID={lock_id}" in content

    def propose_change(self, request: str) -> dict:
        normalized = self._normalize(request)
        request_hash = self._hash(normalized)
        lock_id = request_hash[:12]

        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        response = {
            "status": "FAIL",
            "accepted": False,
            "request": normalized,
            "request_hash": request_hash,
            "lock_id": lock_id,
            "timestamp": timestamp
        }

        try:
            # Передаем lock_id для точной дедупликации
            if self.is_already_proposed(lock_id):
                response["status"] = "DEDUP"
                return response

            entry = (
                f"\n[CHANGE_REQUEST] "
                f"LOCK_ID={lock_id} "
                f"HASH={request_hash} "
                f"STATUS=PENDING "
                f"SYSTEM_RECORD=TRUE "
                f"STAGE=CR_PHASE "
                f"NEXT={normalized} "
                f"DATE={timestamp}"
            )

            with open(self.ledger_path, "a", encoding="utf-8") as f:
                f.write(entry)

            response["status"] = "OK"
            response["accepted"] = True
            return response

        except Exception as e:
            response["status"] = "FAIL"
            response["error"] = str(e)
            return response
