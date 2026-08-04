# -*- coding: utf-8 -*-

from A_07_MEMORY.memory_replay import MemoryReplay


class SemanticCompressor:
    """
    Converts raw memory events into semantic meaning blocks.
    """

    def __init__(self):
        self.replay = MemoryReplay()

    def compress(self, limit: int = 50):
        """
        Step 1: load raw events
        Step 2: cluster by similarity (light heuristic version)
        Step 3: produce semantic summary blocks
        """

        history = self.replay.get_full_history()

        if not history:
            return "NO MEMORY DATA"

        # take last N
        events = history[-limit:]

        # naive semantic grouping (phase 1 heuristic)
        categories = {
            "system": [],
            "memory": [],
            "errors": [],
            "user_actions": [],
            "other": []
        }

        for e in events:
            text = str(e.get("event", "")).lower()

            if "error" in text or "fail" in text:
                categories["errors"].append(text)

            elif "memory" in text or "replay" in text:
                categories["memory"].append(text)

            elif "user" in text or "виктор" in text:
                categories["user_actions"].append(text)

            elif "system" in text:
                categories["system"].append(text)

            else:
                categories["other"].append(text)

        # build semantic summary
        summary = []

        if categories["system"]:
            summary.append("SYSTEM STATE: infrastructure operations ongoing")

        if categories["memory"]:
            summary.append("MEMORY LAYER: active reconstruction and logging")

        if categories["errors"]:
            summary.append("ERROR STATE: instability detected in components")

        if categories["user_actions"]:
            summary.append("USER ACTIVITY: active system development and testing")

        if categories["other"]:
            summary.append("GENERAL ACTIVITY: mixed operational events")

        return "\n".join(summary)

    def compress_for_llm(self, limit: int = 30):
        """
        Output optimized prompt context for LLM injection.
        """

        semantic = self.compress(limit)

        return f"""
[SEMANTIC MEMORY CONTEXT]
{semantic}
""".strip()

    @staticmethod
    def compress_records(records, limit=12):
        """Compress only records already selected as relevant to the query."""
        lines, seen = [], set()
        for record in list(records or [])[:limit]:
            text = str(record.get("summary") or record.get("value") or "").strip()
            if not text or text.casefold() in seen:
                continue
            seen.add(text.casefold())
            source = record.get("source") or record.get("path") or "unknown"
            lines.append(f"- {text} [source: {source}]")
        return "\n".join(lines)


# =========================
# STANDALONE TEST
# =========================

if __name__ == "__main__":
    sc = SemanticCompressor()

    print("=== SEMANTIC COMPRESSION TEST ===")
    print(sc.compress())
