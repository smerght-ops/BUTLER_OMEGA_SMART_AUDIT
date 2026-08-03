# -*- coding: utf-8 -*-

from A_02_MANAGERS.session_manager import ButlerSessionManager
from A_07_MEMORY.agent_planner import AgentPlannerV2
from A_07_MEMORY.execution_registry import ExecutionRegistry
from A_07_MEMORY.memory_facade import MemoryFacade
from A_07_MEMORY.project_history import ProjectHistory
from A_07_MEMORY.semantic_memory import SemanticMemory


class MemoryFacadeV2:
    """DK02 bridge delegating L1-L6 to the existing memory components."""

    def __init__(self):
        self.l1 = MemoryFacade()
        self.l2 = ButlerSessionManager()
        self.l3_l6 = AgentPlannerV2()
        self.l4 = ProjectHistory()
        self.l5 = SemanticMemory()
        self.execution = ExecutionRegistry()

    def get_passport_string(self):
        return self.l1.get_passport_string()

    def add_session_event(self, role, text):
        self.l2.append(role, text)
        return {"ok": True, "role": role}

    def get_session_context(self, limit=12):
        return self.l2.get_recent(limit=limit)

    def get_tasks(self):
        return self.l3_l6.get_current_action_plan()

    def update_task(self, task_id, completed=False, phase=None):
        if completed:
            return {"ok": self.l3_l6.complete_task(task_id), "task_id": task_id}
        if phase:
            key = self.execution.mark_done(phase, task_id)
            return {"ok": True, "task_id": task_id, "registry_key": key}
        return {"ok": False, "error": "TASK_UPDATE_NOT_SPECIFIED"}

    def get_history(self, limit=100):
        return self.l2.get_events(limit=limit)

    def get_project_history(self):
        return self.l4.get_closed_milestones()

    def add_history_event(self, role, text):
        return self.add_session_event(role, text)

    def add_event(self, event, meta=None):
        meta = dict(meta or {})
        return self.add_session_event(meta.get("source", "system"), event)

    def index_semantic(self, text, *, path="memory://runtime", tags=None, entities=None):
        self.l5.append(
            path=path,
            handler="MemoryFacadeV2",
            summary=str(text),
            tags=list(tags or []),
            entities=list(entities or []),
            doc_type="memory",
            source="dk02_runtime",
        )
        return {"ok": True, "path": path}

    def search_semantic(self, query):
        return self.l5.search_by_text(query)

    def evolve_knowledge(self, key, value, provenance="runtime", related_media=None):
        return self.l5.evolve_knowledge(key, value, provenance, related_media=related_media)

    def rollback_knowledge(self, key, version):
        return self.l5.rollback_knowledge(key, version)

    def link_knowledge_media(self, key, media_type, path, source=None, fragment=None):
        return self.l5.link_media(key, media_type, path, source=source, fragment=fragment)

    def search_knowledge(self, query):
        return self.l5.knowledge_search(query)

    def get_media_links(self):
        return self.l5.media_links()

    def get_strategy(self):
        return {
            "plan": self.l3_l6.get_current_action_plan(),
            "execution": self.execution.load(),
        }

    def build_context(self, semantic_query=None, session_limit=12):
        return {
            "l1_passport": self.get_passport_string(),
            "l2_session": self.get_session_context(limit=session_limit),
            "l3_tasks": self.get_tasks(),
            "l4_history": {
                "session": self.get_history(),
                "project": self.get_project_history(),
            },
            "l5_semantic": self.search_semantic(semantic_query) if semantic_query else [],
            "l6_strategy": self.get_strategy(),
        }


if __name__ == "__main__":
    facade = MemoryFacadeV2()
    print(facade.get_passport_string())
