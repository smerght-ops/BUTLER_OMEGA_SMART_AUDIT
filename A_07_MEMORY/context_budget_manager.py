# -*- coding: utf-8 -*-

from A_07_MEMORY.attention_memory import AttentionMemory
from A_07_MEMORY.memory_orchestrator import MemoryOrchestrator


class ContextBudgetManager:
    """
    Final layer of memory system.
    Controls token budget and builds optimal LLM context.
    """

    def __init__(self, token_budget: int = 3000):
        self.token_budget = token_budget
        self.attention = AttentionMemory()
        self.orchestrator = MemoryOrchestrator()

    # =========================
    # 1. TOKEN ESTIMATION
    # =========================

    def estimate_tokens(self, text: str) -> int:
        # simple heuristic (4 chars ≈ 1 token)
        return max(1, len(str(text)) // 4)

    # =========================
    # 2. BUILD PRIORITIZED CONTEXT
    # =========================

    def build_context(self):
        weighted = self.attention.get_weighted_memory()

        final_context = []
        used_tokens = 0

        for item in weighted:
            event = item["event"]
            score = item["score"]

            # combine semantic + attention
            priority_score = score

            estimated = self.estimate_tokens(event)

            # budget check
            if used_tokens + estimated > self.token_budget:
                break

            # keep only meaningful events
            if priority_score < 0.2:
                continue

            final_context.append(f"[{priority_score:.2f}] {event}")
            used_tokens += estimated

        return "\n".join(final_context)

    # =========================
    # 3. FINAL PAYLOAD FOR LLM
    # =========================

    def build_payload(self, user_input: str):
        context = self.build_context()

        return {
            "system_context": context,
            "user_input": user_input,
            "token_budget": self.token_budget
        }

    def fit_text(self, text):
        """Apply this manager's budget to an already relevance-ranked context."""
        lines, used = [], 0
        for line in str(text or "").splitlines():
            cost = self.estimate_tokens(line)
            if used + cost > self.token_budget:
                break
            lines.append(line)
            used += cost
        return {"system_context": "\n".join(lines), "used_tokens": used,
                "token_budget": self.token_budget}


# =========================
# TEST MODE
# =========================

if __name__ == "__main__":
    cb = ContextBudgetManager()

    print("=== CONTEXT BUDGET MANAGER TEST ===\n")

    payload = cb.build_payload("test query")

    print(payload["system_context"])
