# -*- coding: utf-8 -*-

import os
from datetime import datetime

from A_07_MEMORY.memory_replay import MemoryReplay
from A_07_MEMORY.memory_facade_v2 import MemoryFacadeV2


class MemoryOrchestrator:
    """
    Central memory brain layer (NO PATCH ARCHITECTURE).

    Responsibilities:
    - Reads raw system logs (optional external ingestion)
    - Reconstructs context via MemoryReplay
    - Builds final LLM payload for Ollama
    - Provides unified memory API

    DOES NOT modify:
    - chat_router
    - router_integration
    - runtime flow
    """

    def __init__(self):
        self.replay = MemoryReplay()
        self.memory = MemoryFacadeV2()

        # config
        self.max_context_events = 15

    # =========================
    # 1. CONTEXT BUILDING
    # =========================

    def build_context(self, keyword: str = None):
        """
        Build structured memory context for LLM.
        """
        try:
            if keyword:
                events = self.replay.search_event(keyword)
                events = events[-self.max_context_events:]
            else:
                ctx = self.replay.reconstruct_context()
                events = ctx.get("events", [])[-self.max_context_events:]

            return {
                "timestamp": datetime.now().isoformat(),
                "events": events,
                "count": len(events)
            }
        except Exception:
            return {
                "timestamp": datetime.now().isoformat(),
                "events": [],
                "count": 0
            }

    # =========================
    # 2. PAYLOAD BUILDER
    # =========================

    def build_ollama_payload(self, user_text: str, model: str):
        """
        Final injection layer before LLM call.
        """
        context = self.build_context()

        memory_block = ""
        try:
            if context["events"]:
                memory_block = "\n".join(f"- {e}" for e in context["events"])
        except Exception:
            memory_block = ""

        prompt = f"""
[CONTEXT MEMORY]
{memory_block}

[USER INPUT]
{user_text}
""".strip()

        return {
            "model": model,
            "prompt": prompt,
            "timestamp": context["timestamp"]
        }

    # =========================
    # 3. MEMORY WRITE API
    # =========================

    def log_event(self, text: str, source: str = "orchestrator"):
        """
        Write into L4 memory layer.
        """
        try:
            self.memory.add_event(
                event=text,
                meta={
                    "source": source,
                    "timestamp": datetime.now().isoformat()
                }
            )
        except Exception:
            pass

    # =========================
    # 4. DEBUG / INSPECT
    # =========================

    def debug_dump(self):
        """
        Returns raw memory snapshot for diagnostics.
        """
        try:
            return self.replay.get_full_history()
        except Exception:
            return []


# =========================
# STANDALONE TEST
# =========================
if __name__ == "__main__":
    orch = MemoryOrchestrator()
    print("=== MEMORY ORCHESTRATOR TEST ===")
    orch.log_event("system boot test")
    orch.log_event("user said hello")

    payload = orch.build_ollama_payload(
        user_text="test input",
        model="qwen35-ru:latest"
    )

    print("\n--- PAYLOAD ---")
    print(payload)
    print("\n--- DEBUG SNAPSHOT ---")
    print(orch.debug_dump())
