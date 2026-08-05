# -*- coding: utf-8 -*-

from A_07_MEMORY.semantic_compression import SemanticCompressor
from A_07_MEMORY.attention_memory import AttentionMemory
from A_07_MEMORY.context_budget_manager import ContextBudgetManager
from A_07_MEMORY.memory_replay import MemoryReplay
from A_07_MEMORY.memory_facade_v2 import MemoryFacadeV2
from A_07_MEMORY.search_engine import SemanticSearchEngine
from A_07_MEMORY.semantic_core import SemanticCore
from A_07_MEMORY.profile_manager import load_profile


_production_memory_orchestrator = None


def get_memory_orchestrator(token_budget: int = 1200):
    """Return the single process-wide production memory orchestrator."""
    global _production_memory_orchestrator
    if _production_memory_orchestrator is None:
        _production_memory_orchestrator = MemoryOrchestratorV2(token_budget=token_budget)
    return _production_memory_orchestrator


class MemoryOrchestratorV2:
    """
    FINAL MEMORY CONTROLLER
    Unifies all memory layers into single LLM-ready payload.
    """

    def __init__(self, token_budget: int = 3000):
        self.replay = MemoryReplay()
        self.semantic = SemanticCompressor()
        self.attention = AttentionMemory()
        self.budget = ContextBudgetManager(token_budget)
        self.facade = MemoryFacadeV2()
        self.search = SemanticSearchEngine()
        self.graph = SemanticCore()

    # =========================
    # 1. CORE PIPELINE
    # =========================

    def build_memory_packet(self, user_input: str):
        """
        Full deterministic memory pipeline.
        """

        # Select first, then rank/compress. Never inject the whole memory store.
        lexical = self.facade.search_semantic(user_input)[:20]
        weighted = [record for _, record in self.search.search(user_input, limit=20)]
        knowledge = self.facade.search_knowledge(user_input)
        merged, seen = [], set()
        for record in lexical + weighted:
            identity = (record.get("path"), record.get("summary"))
            if identity == (None, None):
                identity = record.get("knowledge_id") or identity
            if identity not in seen:
                seen.add(identity)
                merged.append(record)
        ranked = self.attention.rank_records(merged, user_input, limit=12)
        semantic_context = self.semantic.compress_records(ranked)
        attention_context = "\n".join(
            f"- {row.get('summary', '')} [source: {row.get('source') or row.get('path')}]"
            for row in ranked[:8]
        )
        profile_context = self._profile_context(user_input)
        knowledge_context = "\n".join(
            f"- {item.get('knowledge', {}).get('key')}: "
            f"{item.get('knowledge', {}).get('value')} "
            f"[source: {item.get('knowledge', {}).get('source') or item.get('knowledge', {}).get('path')}]"
            for item in knowledge[:8]
        )
        try:
            graph_context = self.graph.analyze(user_input)
        except Exception:
            graph_context = {"relations": []}
        raw_text = ""
        combined = "\n".join(part for part in (
            profile_context, knowledge_context, semantic_context, attention_context,
            str(graph_context.get("relations") or ""),
        ) if part)
        budget_payload = self.budget.fit_text(combined)

        # =========================
        # FINAL ASSEMBLY
        # =========================

        final_packet = {
            "semantic_context": semantic_context,
            "profile_context": profile_context,
            "knowledge_context": knowledge_context,
            "attention_context": attention_context,
            "raw_context": raw_text,
            "budget_context": budget_payload.get("system_context", ""),
            "retrieval": {
                "lexical": lexical, "weighted_semantic": weighted,
                "graph": graph_context, "knowledge": knowledge,
            },
            "provenance": sorted({str(row.get("source") or row.get("path")) for row in ranked}),
            "used_tokens": budget_payload.get("used_tokens", 0),
            "user_input": user_input
        }

        return final_packet

    @staticmethod
    def _profile_context(user_input: str):
        """Select relevant personal facts without dumping the whole profile."""
        try:
            profile = load_profile()
        except Exception:
            return ""
        q = str(user_input or "").casefold().replace("ё", "е")
        query_words = {word for word in q.replace("_", " ").split() if len(word) >= 3}
        asks_preferences = any(stem in q for stem in (
            "предпоч", "лучше", "какой формат", "каком языке", "какой язык",
            "что ты знаешь обо мне", "учитывая то, что ты знаешь обо мне",
        ))
        selected = []
        for section, values in profile.items():
            if not isinstance(values, dict):
                continue
            for key, payload in values.items():
                value = payload.get("value") if isinstance(payload, dict) else payload
                if value is None:
                    continue
                searchable = f"{section} {key} {value}".casefold().replace("_", " ")
                relevant = bool(query_words & set(searchable.split()))
                if section == "preferences" and asks_preferences:
                    relevant = True
                if relevant:
                    selected.append(f"- {key} = {value} [source: user_profile.json]")
        return "\n".join(selected[:8])

    # =========================
    # 2. LLM READY OUTPUT
    # =========================

    def build_llm_prompt(self, user_input: str):
        packet = self.build_memory_packet(user_input)

        return f"""
[MEMORY ORCHESTRATOR v2 CONTEXT]

--- SEMANTIC ---
{packet['semantic_context']}

--- ATTENTION ---
{packet['attention_context']}

--- RECENT EVENTS ---
{packet['raw_context']}

--- BUDGET FILTERED ---
{packet['budget_context']}

--- USER INPUT ---
{packet['user_input']}
""".strip()

    def add_session_event(self, *args, **kwargs):
        return self.facade.add_session_event(*args, **kwargs)

    def build_context(self, *args, **kwargs):
        return self.facade.build_context(*args, **kwargs)

    def evolve_knowledge(self, *args, **kwargs):
        return self.facade.evolve_knowledge(*args, **kwargs)

    def get_media_links(self, *args, **kwargs):
        return self.facade.get_media_links(*args, **kwargs)

    def index_semantic(self, *args, **kwargs):
        return self.facade.index_semantic(*args, **kwargs)

    def link_knowledge_media(self, *args, **kwargs):
        return self.facade.link_knowledge_media(*args, **kwargs)

    def rollback_knowledge(self, *args, **kwargs):
        return self.facade.rollback_knowledge(*args, **kwargs)

    def search_knowledge(self, *args, **kwargs):
        return self.facade.search_knowledge(*args, **kwargs)


# =========================
# STANDALONE TEST
# =========================

if __name__ == "__main__":
    mo = get_memory_orchestrator()

    print("=== MEMORY ORCHESTRATOR v2 TEST ===\n")

    print(mo.build_llm_prompt("test input"))
