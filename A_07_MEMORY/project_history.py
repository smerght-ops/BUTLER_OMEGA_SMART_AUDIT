# -*- coding: utf-8 -*-

import re
from pathlib import Path


class ProjectHistory:

    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[1]
        self.ledger_path = self.project_root / "A_08_LOGS" / "PROJECT_LEDGER.txt"

    def get_closed_milestones(self):
        """Парсит Леджер и возвращает СТРОГО валидированные системные вехи."""
        if not self.ledger_path.exists():
            return []

        milestones = []
        content = self.ledger_path.read_text(encoding="utf-8-sig")
        pattern = r"\[([^\]]+)\]\s+(.*)$"

        for line in content.splitlines():
            line = line.strip()
            if not line or not line.startswith("["):
                continue

            match = re.match(pattern, line)
            if match:
                tag = match.group(1)
                kv_body = match.group(2)

                # Извлекаем KV-пары через regex
                kv_pairs = dict(re.findall(r"([A-Z_]+)=([^\s]+)", kv_body))

                milestones.append({
                    "tag": tag,
                    "status": kv_pairs.get("STATUS", "UNKNOWN"),
                    "system_record": kv_pairs.get("SYSTEM_RECORD", "FALSE").upper(),
                    "stage": kv_pairs.get("STAGE", "4.14.1_LEGACY"),
                    "next": kv_pairs.get("NEXT", "CHANGE_REQUEST_MANAGER"),
                    "previous": kv_pairs.get("PREVIOUS", "NONE"),
                    "date": kv_pairs.get("DATE", "UNKNOWN")
                })

        # ТВОЙ ПАТЧ: Жесткий фильтр безопасности на выходе
        valid_milestones = [
            m for m in milestones
            if m["system_record"] == "TRUE" and m["status"] in ("STABLE", "GREEN")
        ]
        return valid_milestones

    def get_lesson_summary(self):
        """Динамическая сводка истории из чистого Леджера."""
        records = self.get_closed_milestones()
        if not records:
            return "=== PROJECT LEDGER IS EMPTY OR NO VALID SYSTEM RECORDS ==="

        lines = [
            "=" * 70,
            "   СВОДКА ИСТОРИИ ИЗ ЧИСТОГО PROJECT LEDGER",
            "=" * 70
        ]
        for r in records:
            lines.append(f"  ✓ [{r['date']}] {r['tag']} -> {r['status']} (Stage: {r['stage']})")
        lines.append("=" * 70)
        return "\n".join(lines)


if __name__ == "__main__":
    ph = ProjectHistory()
    print(ph.get_lesson_summary())
