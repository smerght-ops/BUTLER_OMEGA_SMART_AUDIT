# -*- coding: utf-8 -*-

from A_02_MANAGERS.smart_dispatcher_v2 import SmartDispatcherV2
from A_02_MANAGERS.Planner.planner_engine import PlannerEngine
from A_03_ORCHESTRATION.ConversationContext.context_engine import ConversationContextEngine

_dispatcher = SmartDispatcherV2()


def dispatch(query: str, context: dict = None):

    original_query = query
    context = dict(context or {})

    query = ConversationContextEngine.resolve(query)
    context["image_followup"] = ConversationContextEngine.last_was_image_followup

    if PlannerEngine.can_handle(query):

        PlannerEngine.execute(query)

        result = {
            "ok": True,
            "department": "PLANNER",
            "model": "PlannerEngine",
            "text": "Goal accepted.",
            "latency_ms": 0
        }

        ConversationContextEngine.update(original_query, result)

        return result

    result = _dispatcher.dispatch(query, context)

    ConversationContextEngine.update(original_query, result)

    return result
