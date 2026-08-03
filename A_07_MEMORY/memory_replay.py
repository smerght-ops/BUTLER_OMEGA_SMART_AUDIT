# -*- coding: utf-8 -*-

from A_07_MEMORY.memory_facade_v2 import MemoryFacadeV2


class MemoryReplay:
    """
    Deterministic replay engine for L4 history.
    Reads MemoryFacadeV2 history and reconstructs context.
    """

    def __init__(self):
        self.memory = MemoryFacadeV2()

    def get_full_history(self):
        return self.memory.get_history(limit=1000)

    def replay_last_n(self, n: int = 10):
        history = self.memory.get_history(limit=n)

        replay = []
        for item in history:
            replay.append(f"[{item.get('time')}] {item.get('event')}")

        return replay

    def reconstruct_context(self):
        """
        Builds lightweight context snapshot for AI usage.
        """
        history = self.memory.get_history(limit=20)

        context = {
            "events": [h.get("event") for h in history],
            "count": len(history)
        }

        return context

    def search_event(self, keyword: str):
        history = self.memory.get_history(limit=1000)

        results = []
        for item in history:
            if keyword.lower() in str(item.get("event", "")).lower():
                results.append(item)

        return results


# =========================
# STANDALONE TEST
# =========================

if __name__ == "__main__":
    replay = MemoryReplay()

    print("=== MEMORY REPLAY TEST ===")

    print("\nLAST 5 EVENTS:")
    for line in replay.replay_last_n(5):
        print(line)

    print("\nCONTEXT SNAPSHOT:")
    print(replay.reconstruct_context())
