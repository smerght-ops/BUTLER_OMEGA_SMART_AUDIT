# -*- coding: utf-8 -*-

from datetime import datetime
from A_07_MEMORY.memory_replay import MemoryReplay


class AttentionMemory:
    """
    Assigns importance scores to memory events.
    Enables prioritization for context injection.
    """

    def __init__(self):
        self.replay = MemoryReplay()

    # =========================
    # 1. SCORING ENGINE
    # =========================

    def score_event(self, event: str):
        text = str(event).lower()
        score = 0.0

        # SYSTEM CRITICAL EVENTS
        if "error" in text or "fail" in text:
            score += 0.9

        # MEMORY / ARCHITECTURE EVENTS
        if "memory" in text or "replay" in text:
            score += 0.8

        # USER ACTIONS
        if "виктор" in text or "user" in text:
            score += 0.6

        # MODEL / OLLAMA EVENTS
        if "ollama" in text or "model" in text:
            score += 0.7

        # DEBUG / LOW VALUE
        if "debug" in text:
            score += 0.2

        # DEFAULT BASE SIGNAL
        if score == 0.0:
            score = 0.3

        return score

    # =========================
    # 2. SORTED MEMORY STREAM
    # =========================

    def get_weighted_memory(self, limit: int = 50):
        history = self.replay.get_full_history()

        weighted = []

        for h in history[-limit:]:
            event = h.get("event", "")
            score = self.score_event(event)

            weighted.append({
                "event": event,
                "score": score,
                "time": h.get("time")
            })

        # sort by importance
        weighted.sort(key=lambda x: x["score"], reverse=True)

        return weighted

    # =========================
    # 3. TOP CONTEXT FOR LLM
    # =========================

    def build_attention_context(self, limit: int = 10):
        weighted = self.get_weighted_memory()

        top = weighted[:limit]

        return "\n".join(
            f"[{w['score']:.1f}] {w['event']}"
            for w in top
        )

    def rank_records(self, records, query="", limit=12):
        query_words = set(str(query).casefold().split())
        ranked = []
        for record in records or []:
            text = str(record.get("summary") or record.get("value") or "")
            overlap = len(query_words & set(text.casefold().split()))
            ranked.append((overlap + self.score_event(text), record))
        ranked.sort(key=lambda item: item[0], reverse=True)
        return [record for _, record in ranked[:limit]]


# =========================
# STANDALONE TEST
# =========================

if __name__ == "__main__":
    am = AttentionMemory()

    print("=== ATTENTION MEMORY TEST ===")

    print("\nTOP EVENTS:")
    print(am.build_attention_context())
