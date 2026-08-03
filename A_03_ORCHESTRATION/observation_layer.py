# -*- coding: utf-8 -*-

import json
from datetime import datetime
from pathlib import Path


class ObservationLayer:

    def __init__(self):

        self.log_dir = Path("A_08_LOGS")
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.log_file = self.log_dir / "OBSERVATIONS.jsonl"

    def record(
        self,
        source,
        event,
        payload=None
    ):

        if payload is None:
            payload = {}

        row = {
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "event": event,
            "payload": payload
        }

        with open(
            self.log_file,
            "a",
            encoding="utf-8"
        ) as f:

            json.dump(
                row,
                f,
                ensure_ascii=False
            )

            f.write("\n")

        return row
