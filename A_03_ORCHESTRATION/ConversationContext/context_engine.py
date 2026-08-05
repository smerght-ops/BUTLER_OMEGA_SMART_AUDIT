# -*- coding: utf-8 -*-

"""
Stage 11.1

Conversation Context Engine

Understands short follow-up messages.
"""

from A_03_ORCHESTRATION.ConversationContext.ImageSession.image_session import ImageSession


class ConversationContextEngine:

    last_department = None
    last_user_query = ""
    last_was_image_followup = False
    last_referent = None
    last_observation = None
    last_correlation_id = None

    IMAGE_TRIGGERS = (
        "нарисуй",
        "сгенерируй изображение",
        "создай картинку",
        "создай изображение",
        "сделай картинку",
        "сделай фото",
    )

    IMAGE_FOLLOWUP_TRIGGERS = (
        "не лицо",
        "в полный рост",
        "на море",
        "под водопадом",
        "измени фон",
        "добавь ",
        "убери ",
        "ещё вариант",
        "еще вариант",
        "другой вариант",
    )

    IMAGE_EXECUTE_TRIGGERS = ("выполняй", "выполни", "генерируй")
    CHAT_CONTINUE_TRIGGERS = ("выполняй", "выполни", "продолжай", "дальше")

    @classmethod
    def _has_anaphoric_reference(cls, query: str) -> bool:
        low = " ".join(str(query or "").casefold().split())
        words = set(low.replace(",", " ").replace(".", " ").split())
        return bool(words & {
            "этого", "этой", "этом", "этот", "эта", "это",
            "его", "её", "ее", "нём", "нем", "ней",
        })

    @classmethod
    def enrich_context(cls, query: str, context: dict = None) -> dict:
        """Attach a bounded previous-turn observation for a genuine follow-up."""
        context = dict(context or {})
        if not cls.last_referent or not cls._has_anaphoric_reference(query):
            return context
        context["conversation_context"] = {
            "previous_user_query": cls.last_user_query,
            "previous_department": cls.last_department,
            "previous_correlation_id": cls.last_correlation_id,
            "referent": dict(cls.last_referent),
            "previous_observation": dict(cls.last_observation or {}),
        }
        context["resolved_referent"] = dict(cls.last_referent)
        context.setdefault("path", cls.last_referent.get("path"))
        return context

    @classmethod
    def resolve(cls, query: str):

        q = query.strip()
        low = q.lower()
        cls.last_was_image_followup = False

        if any(t in low for t in cls.IMAGE_TRIGGERS):

            ImageSession.update(q)

            return "нарисуй " + ImageSession.current()

        if cls.last_department == "IMAGE" and low in cls.IMAGE_EXECUTE_TRIGGERS:
            cls.last_was_image_followup = True
            return "нарисуй " + ImageSession.current()

        if cls.last_department == "CHAT" and low in cls.CHAT_CONTINUE_TRIGGERS and cls.last_user_query:
            return (
                f"Предыдущий запрос пользователя: {cls.last_user_query}\n"
                f"Текущая команда: {q}. Продолжи предыдущий пользовательский сценарий."
            )

        if cls.last_department == "IMAGE" and any(
            low.startswith(marker) for marker in cls.IMAGE_FOLLOWUP_TRIGGERS
        ):
            cls.last_was_image_followup = True
            return "нарисуй " + ImageSession.update(q)

        if cls.last_department == "IMAGE":
            ImageSession.clear()

        return q


    @classmethod
    def update(cls, original_query: str, result: dict):

        dept = result.get("department")

        if dept:

            cls.last_department = dept

        if dept and result.get("ok", True):
            cls.last_user_query = original_query.strip()

        metadata = result.get("metadata") or {}
        path = metadata.get("path")
        snapshot = metadata.get("analysis_snapshot") or {}
        if path:
            kind = (
                "directory"
                if snapshot.get("root") or metadata.get("action") == "analyze_folder"
                else "artifact"
            )
            cls.last_referent = {"kind": kind, "path": str(path)}
            entries = [
                {
                    "relative_path": item.get("relative_path"),
                    "kind": item.get("kind"),
                    "size": item.get("size"),
                }
                for item in list(snapshot.get("entries") or [])[:100]
                if isinstance(item, dict)
            ]
            cls.last_observation = {
                "department": dept,
                "text": str(result.get("text") or "")[:4000],
                "path": str(path),
                "entries": entries,
                "truncated": len(snapshot.get("entries") or []) > len(entries),
            }
        correlation_id = metadata.get("correlation_id")
        if correlation_id:
            cls.last_correlation_id = str(correlation_id)
