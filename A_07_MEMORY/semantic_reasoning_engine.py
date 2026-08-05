# -*- coding: utf-8 -*-
"""
BUTLER OMEGA SMART
Semantic Reasoning Engine V1

LOCAL FIRST.
No internet.
No cloud.
No API keys.

Purpose:
- semantic normalization
- synonym expansion
- simple meaning-based matching
- explainable search scoring
"""

import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Any


SEMANTIC_GROUPS = {
    "паспорт": [
        "паспорт", "документ личности", "удостоверение", "личный документ",
        "id", "identity", "документы в руках"
    ],
    "договор": [
        "договор", "контракт", "соглашение", "купля продажа",
        "лизинг", "аренда", "документ сделки"
    ],
    "автобус": [
        "автобус", "mb100d", "мерседес", "микроавтобус",
        "машина", "транспорт", "авто"
    ],
    "крыша": [
        "крыша", "кровля", "потолок", "верх", "водосток",
        "желоб", "фольгоизол", "герметик", "битум"
    ],
    "ремонт": [
        "ремонт", "починка", "работа", "техкарта",
        "технологическая карта", "инструкция", "этапы",
        "карта ремонта", "ремонт крыши"
    ],
    "деньги": [
        "деньги", "счета", "оплата", "платежи",
        "долг", "финансы", "бюджет"
    ],
    "план": [
        "план", "дорожная карта", "roadmap", "следующие шаги",
        "что дальше", "задачи"
    ],
    "архитектура": [
        "архитектура", "архитектурный", "архитектурная",
        "архитектурный отчет", "зависимости", "структура",
        "модули", "департаменты", "контур", "система"
    ],
}


@dataclass
class SemanticMatch:
    query: str
    target: str
    score: int
    reasons: List[str]


class SemanticReasoningEngine:

    def __init__(self):
        self.groups = SEMANTIC_GROUPS

    def normalize(self, text: str) -> str:
        text = (text or "").lower()
        text = text.replace("ё", "е")
        # Use Unicode property classes for proper Cyrillic handling
        text = re.sub(r"[^\w\sа-яё0-9_\-]+", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def tokens(self, text: str) -> List[str]:
        return [t for t in self.normalize(text).split(" ") if t]

    def detect_intent(
        self,
        text: str,
        inherited_intent: str = None,
    ) -> Dict[str, Any]:
        """Classify requests for knowledge about Butler itself, not user data."""
        normalized = self.normalize(text)
        tokens = self.tokens(normalized)

        def has_stem(*stems):
            return any(token.startswith(stem) for token in tokens for stem in stems)

        named_project_component = any(
            token.endswith(("department", "agent")) for token in tokens
        )
        asks_for_information = has_stem(
            "что", "как", "какие", "какой", "покаж", "расскаж", "где", "из", "нужн",
        )
        explicit_project_object = named_project_component or has_stem(
            "butler", "проект", "систем", "архитектур", "внутрен",
        )
        project_knowledge_dimension = has_stem(
            "знан", "состав", "компонент", "модул", "department", "департамент",
            "отдел", "возможност", "реализ", "состояни", "устро", "runtime",
            "inspector", "архитектур", "сделан", "создан", "остал", "заверш", "уме",
            "повторн", "дубл",
        )
        project_knowledge_dimension = project_knowledge_dimension or named_project_component
        lifecycle_ellipsis = has_stem("сделан", "создан", "остал", "заверш")
        inherits_project_object = inherited_intent == "PROJECT_SELF_KNOWLEDGE"

        # An operation on a concrete user object is not a question about Butler
        # merely because its wording also contains words such as "создан" or
        # "компонент".  Operational ownership must win over project vocabulary.
        has_concrete_file = bool(re.search(
            r"(?:[a-z]:[\\/]|\.(?:docx?|pdf|png|jpe?g|webp|bmp|txt|zip|mp3|mp4)\b)",
            str(text or ""), re.IGNORECASE,
        ))
        operational_action = has_stem(
            "создай", "создат", "добав", "сохран", "открой", "скачай",
            "загруз", "извлек", "проанализ", "распоз", "удал", "переимен",
            "свяж", "запомн", "откат",
        )
        operational_object = has_concrete_file or has_stem(
            "файл", "документ", "word", "docx", "pdf", "изображ", "фото",
            "картин", "аудио", "видео", "архив", "папк", "url",
            "знан", "памят",
        )
        explicit_operation = operational_action and operational_object
        personal_memory_subject = (
            has_stem("памят", "помн", "запом", "любим", "предпоч", "favorite_")
            and bool(re.search(r"\b(?:я|мо[йяеёию]|мне|меня|обо\s+мне)\b", normalized))
            and not has_stem("архитектур", "компонент", "runtime", "внутрен")
        )

        reasons = []
        if asks_for_information:
            reasons.append("information_request")
        if explicit_project_object:
            reasons.append("project_self_reference")
        if named_project_component:
            reasons.append("named_project_component")
        if project_knowledge_dimension:
            reasons.append("project_knowledge_dimension")
        if lifecycle_ellipsis:
            reasons.append("project_lifecycle_ellipsis")
        if inherits_project_object:
            reasons.append("inherited_project_self_reference")

        matched = (not explicit_operation) and (not personal_memory_subject) and asks_for_information and (
            (explicit_project_object and project_knowledge_dimension)
            or (explicit_project_object and has_stem("зна", "уме", "расскаж"))
            or (inherits_project_object and project_knowledge_dimension)
            or (inherits_project_object and lifecycle_ellipsis)
        )
        if lifecycle_ellipsis:
            focus = "PROJECT_LIFECYCLE"
        elif has_stem("department", "департамент", "отдел"):
            focus = "PROJECT_DEPARTMENTS"
        else:
            focus = "PROJECT_OVERVIEW"
        return {
            "name": "PROJECT_SELF_KNOWLEDGE" if matched else None,
            "matched": matched,
            "confidence": 1.0 if matched else 0.0,
            "focus": focus if matched else None,
            "object": "BUTLER_OMEGA_SMART" if matched else None,
            "inherited": bool(matched and inherits_project_object and not explicit_project_object),
            "reasons": reasons,
            "normalized_query": normalized,
        }

    def expand(self, text: str) -> List[str]:
        norm = self.normalize(text)
        result = set(self.tokens(norm))

        for key, words in self.groups.items():
            for w in words:
                if self.normalize(w) in norm:
                    result.add(key)
                    for item in words:
                        result.update(self.tokens(item))

        return sorted(result)

    def score(self, query: str, target: str) -> SemanticMatch:
        q_tokens = set(self.expand(query))
        t_tokens = set(self.expand(target))

        direct = q_tokens & t_tokens

        score = 0
        reasons = []

        if direct:
            score += len(direct) * 10
            reasons.append("token_overlap:" + ",".join(sorted(direct)))

        q_norm = self.normalize(query)
        t_norm = self.normalize(target)

        if q_norm and q_norm in t_norm:
            score += 50
            reasons.append("direct_phrase")

        for key, words in self.groups.items():
            q_hit = any(self.normalize(w) in q_norm for w in words)
            t_hit = any(self.normalize(w) in t_norm for w in words)
            if q_hit and t_hit:
                score += 25
                reasons.append("semantic_group:" + key)

        return SemanticMatch(
            query=query,
            target=target,
            score=score,
            reasons=reasons
        )

    def rank(self, query: str, candidates: List[str], limit: int = 10) -> List[Dict[str, Any]]:
        matches = [self.score(query, c) for c in candidates]
        matches = [m for m in matches if m.score > 0]
        matches.sort(key=lambda x: x.score, reverse=True)
        return [asdict(m) for m in matches[:limit]]

    def enrich(self, query: str, matches: list):

        if not matches:
            return matches

        try:

            ranked=self.rank(
                query,
                [m.get("handler","") for m in matches]
            )

            order={}

            for i,item in enumerate(ranked):
                order[item["target"].upper()]=i

            matches=sorted(
                matches,
                key=lambda m:order.get(
                    str(m.get("handler","")).upper(),
                    9999
                )
            )

        except Exception:
            pass

        return matches

    def reason(self, query: str, candidates: list):

        ranked = self.rank(query, candidates)

        return {
            "query": query,
            "tokens": self.expand(query),
            "matches": self.enrich(query, ranked)
        }

    def build_task_contract(self, query: str) -> Dict[str, Any]:
        """
        Build a minimal Semantic Task Contract from the query.
        Returns:
        {
            "intent": "",  # SEARCH | CREATE | TRANSFORM | EDIT
            "entities": [],  # recognized entities
            "missing_information": [],  # missing identifiers
            "execution_ready": bool  # true if no missing info
        }
        """
        # Work with raw bytes to avoid terminal encoding issues
        query_bytes = query.encode('utf-8')

        intent = ""
        entities = []
        missing_information = []

        # 1. Intent recognition: SEARCH, CREATE, TRANSFORM, EDIT (using byte patterns)
        intent_patterns = [
            (["найди", "где", "покаж", "открой"], "SEARCH"),
            (["создай", "добавь", "создат", "добав"], "CREATE"),
            (["преобразуй", "конвертируй", "переведи", "измени формат"], "TRANSFORM"),
            (["измен", "отредактируй", "поправь", "обнови", "сделай как"], "EDIT"),
        ]

        for stems, intent_name in intent_patterns:
            if any(stem.lower() in query.lower() for stem in stems):
                intent = intent_name
                break

        # 2. Entity recognition: прошлый, новый, последний, только, не меняй
        entity_patterns = [
            ("прошлый", "past"),
            ("новый", "new"),
            ("последний", "last"),
            ("только", "only"),
            ("не меняй", "do_not_change"),
        ]

        for pattern, entity_type in entity_patterns:
            if pattern.lower() in query.lower():
                entities.append(entity_type)

        # 3. Missing information check using byte patterns
        reference_patterns = [
            (r"прошлый.*?договор", "прошлый документ (нет идентификатора)"),
            (r"последний.*?расчёт", "последний расчёт (нет идентификатора)"),
            (r"новый.*?объект", "новый объект (нет идентификатора)"),
        ]

        # Check if there is a specific identifier (number, name, date, etc.)
        has_identifier = bool(re.search(
            r"(?:\w+|id|\d\s+[\d]+)",
            query,
            re.IGNORECASE
        ))

        for pattern, missing_msg in reference_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                if not has_identifier:
                    missing_information.append(missing_msg)
        # 4. execution_ready: true only if missing_information is empty
        execution_ready = len(missing_information) == 0

        return {
            "intent": intent,
            "entities": entities,
            "missing_information": missing_information,
            "execution_ready": execution_ready,
        }


if __name__ == "__main__":
    engine = SemanticReasoningEngine()

    candidates = [
        "Паспорт Евгений Иванович jpg",
        "Договор купли продажи автобуса MB100D",
        "Технологическая карта ремонта крыши автобуса",
        "Счета и платежи за июль",
        "ROADMAP_6_0_BUTLER_OMEGA_SMART.md",
        "Архитектурный отчет Project Documentation Department"
    ]

    tests = [
        "найди документ личности",
        "где договор на машину",
        "что по крыше мерседеса",
        "какие платежи",
        "что дальше по проекту",
        "покажи архитектуру"
    ]

    for q in tests:

        print("=" * 70)
        print("QUERY:", q)
        print("-" * 70)

        result = engine.reason(q, candidates)

        print("TOKENS")
        print(result["tokens"])

        print()

        print("MATCHES")

        for r in result["matches"]:
            print(r)
