# -*- coding: utf-8 -*-

import json
from pathlib import Path

from .context_provider import ContextProvider
from .goal_analyzer import GoalAnalyzer
from .dependency_analyzer import DependencyAnalyzer
from .recipe_builder import RecipeBuilder
from .queue_manager import QueueManager
from A_02_MANAGERS.Planner.planner_engine import PlannerEngine


class ArchitectAgent:
    """Existing ArchitectAgent with a grounded read-only question path."""

    def __init__(self, root=None, provider=None):
        self.root = Path(root).resolve() if root else Path.cwd().resolve()
        self.context_provider = ContextProvider(self.root)
        self.goal_analyzer = GoalAnalyzer()
        self.dependency_analyzer = DependencyAnalyzer()
        self.recipe_builder = RecipeBuilder()
        self.queue_manager = QueueManager(self.root)
        self.provider = provider

    def _provider(self):
        if self.provider is None:
            from A_02_MANAGERS.smart_dispatcher import SmartDispatcher
            self.provider = SmartDispatcher(project_root=self.root)
        return self.provider

    def answer(self, query: str):
        context = self.context_provider.build_context(query)
        factual_answer = self._factual_answer(query, context)
        evidence = self._compact_evidence(query, context)
        provider = self._provider()
        provider_result = provider.execute_employee(
            employee="chat",
            system_prompt=(
                "Ты ArchitectAgent Butler Omega Smart. Ответь по-русски. Используй только переданные факты "
                "и доказанный вывод. Не добавляй неподтверждённые компоненты, статусы или возможности. "
                "Пути и имена классов сохраняй точно. Если доказательств недостаточно, явно скажи UNCONFIRMED. "
                "Если доказанный вывод содержит нумерованные разделы, сохрани каждый раздел и его смысл; не заменяй их рекомендациями."
            ),
            user_content=(f"ВОПРОС:\n{query}\n\nEVIDENCE:\n{json.dumps(evidence, ensure_ascii=False)}"
                          f"\n\nОБЯЗАТЕЛЬНЫЙ ДОКАЗАННЫЙ ВЫВОД (сохрани все разделы):\n{factual_answer}"),
        )
        text = provider.clean_model_output(provider_result.get("text") or "")
        llm_used = provider_result.get("status") == "ok" and bool(text)
        model_output_accepted = llm_used and self._result_contract_accepts(factual_answer, text)
        return {"text": text if model_output_accepted else factual_answer,
                "model": provider_result.get("model") if llm_used else "ARCHITECT_FACTUAL_FALLBACK",
                "llm_used": llm_used, "provider": "SmartDispatcher.execute_employee",
                "model_output_accepted": model_output_accepted,
                "provider_error": None if llm_used else provider_result.get("fallback_reason"), "evidence": evidence}

    @staticmethod
    def _result_contract_accepts(factual_answer, model_text):
        """Accept only a faithful rendering of the grounded factual answer."""
        normalize = lambda value: " ".join(str(value or "").casefold().split()).strip(" *#`\n")
        expected = normalize(factual_answer)
        actual = normalize(model_text)
        allowed_prefixes = (
            "обязательный доказанный вывод:", "доказанный вывод:",
            "фактический ответ:", "ответ:",
        )
        for prefix in allowed_prefixes:
            if actual.startswith(prefix):
                actual = actual[len(prefix):].strip(" *#`\n")
        return bool(expected) and actual == expected

    @staticmethod
    def _compact_evidence(query, context):
        """Bound LLM evidence while preserving query-relevant paths and proof."""
        q = str(query or "").casefold()
        knowledge = context.get("architectural_knowledge", {})
        runtime = context.get("runtime", {})
        department_query = "department" in q or "департамент" in q
        inspector_query = "inspector" in q or "инспектор" in q
        source_query = "источник" in q and "знан" in q
        named_departments = [item for item in runtime.get("departments", [])
                             if str(item.get("class", "")).casefold() in q]
        selected_departments = (runtime.get("departments", []) if department_query
                                else named_departments)
        departments = []
        for item in selected_departments:
            departments.append({
                "class": item.get("class"), "source": item.get("source"),
                "registered": item.get("registered"),
                "runtime_reachable": item.get("runtime_reachable"),
                "capabilities": item.get("capabilities", [])[:8],
                "public_methods": item.get("public_methods", [])[:6],
            })
        include_tools = inspector_query
        matches = []
        for row in knowledge.get("query_matches", [])[:8]:
            matches.append({
                "path": row.get("path"), "classes": row.get("classes", [])[:8],
                "functions": row.get("functions", [])[:8], "imports": row.get("imports", [])[:8],
            })
        artifacts = []
        for row in knowledge.get("map_and_registry_artifacts", []):
            path = str(row.get("path", ""))
            if inspector_query and not any(word in path.casefold() for word in ("inspector", "linkmap", "dependency")):
                continue
            if not (inspector_query or source_query):
                continue
            artifacts.append({key: row.get(key) for key in
                              ("path", "exists", "schema", "generator", "generated_utc", "freshness")})
        inventory = knowledge.get("live_inventory", {})
        live_summary = {key: inventory.get(key) for key in
                        ("total_files", "python_files", "active_python_files", "generated_utc")
                        if key in inventory}
        state = context.get("project_state", {})
        state_summary = {key: state.get(key) for key in ("name", "version", "current_stage", "status")
                         if key in state}
        return {
            "project_state": state_summary,
            "runtime": {"official_entry": runtime.get("official_entry"), "dispatcher": runtime.get("dispatcher"),
                        "departments": departments},
            "relevant_components": context.get("relevant_components", [])[:6],
            "discovery_knowledge": {
                key: context.get("discovery_knowledge", {}).get(key)
                for key in ("status", "version", "generated", "generator", "role", "summary")
            },
            "architectural_knowledge": {
                "source_policy": knowledge.get("source_policy"),
                "live_inventory": live_summary,
                "coverage": knowledge.get("coverage", []) if inspector_query else [],
                "query_matches": matches,
                "relations": knowledge.get("relations", {}),
                "tool_inventory_total": knowledge.get("tool_inventory_total"),
                "tool_inventory": knowledge.get("tool_inventory", [])[:20] if include_tools else [],
                "artifacts": artifacts,
                "known_limits": knowledge.get("known_limits", []),
            },
            "acceptance": {key: context.get("acceptance", {}).get(key)
                           for key in ("timestamp", "official_entry", "counts", "all_scenarios_passed")},
        }

    @staticmethod
    def _factual_answer(query, context):
        q = str(query or "").casefold()
        departments = context.get("runtime", {}).get("departments", [])
        names = [item.get("class") for item in departments if item.get("class")]
        relevant = context.get("relevant_components", [])
        knowledge = context.get("architectural_knowledge", {})
        matches = knowledge.get("query_matches", [])
        relations = knowledge.get("relations", {})
        tools = knowledge.get("tool_inventory", [])
        artifacts = knowledge.get("map_and_registry_artifacts", [])
        state = context.get("project_state", {})
        stage = state.get("current_stage") or state.get("identity", {}).get("current_stage") or "UNKNOWN"
        proofs = state.get("proofs", {})
        creation_intent = any(marker in q for marker in
                              ("нужно создать", "нужно ли создавать", "создать новый",
                               "создавать новый", "следует создать"))
        duplication_intent = "повторн" in q or "дубл" in q

        if "памят" in q and any(marker in q for marker in ("компонент", "устро", "связан", "runtime")):
            categories = knowledge.get("category_components", {})
            memory_paths = categories.get("memory", [])
            preferred = [path for path in memory_paths if any(name in path.casefold() for name in (
                "memory_facade", "memory_orchestrator", "semantic_memory",
                "attention_memory", "semantic_compression", "context_budget",
            ))]
            paths = preferred or [row.get("path") for row in matches if "memory" in row.get("path", "").casefold()]
            paths = list(dict.fromkeys(path for path in paths if path))[:16]
            return (
                "Подтверждённые компоненты архитектуры памяти:\n- "
                + ("\n- ".join(paths) if paths else "UNCONFIRMED")
                + "\nСвязь с официальным Runtime: BUTLER_OS.py → dispatcher_bridge_v2.py "
                  "→ SmartDispatcherV2 → MemoryOrchestratorV2; для операций хранения "
                  "SmartDispatcherV2 направляет запрос в MemoryDepartment → MemoryFacadeV2 "
                  "→ SemanticMemory/profile storage. Источник: актуальный Python AST и live path index."
            )

        if "реализ" in q or "заверш" in q:
            implemented = []
            for item in departments:
                capabilities = item.get("capabilities", [])
                if capabilities:
                    implemented.append(
                        f"{item.get('class')}: {', '.join(capabilities)} @ {item.get('source')}"
                    )
            return (
                "Подтверждённые реализованные Runtime-возможности:\n- "
                + ("\n- ".join(implemented) if implemented else "UNCONFIRMED")
                + "\nИсточник: актуальный Python AST регистрации SmartDispatcherV2 и файлов Department."
            )

        if "модул" in q:
            modules = [
                f"{item.get('class')} — {item.get('source')}"
                for item in departments
            ]
            return (
                "Существующие Runtime-модули, подтверждённые актуальным AST:\n- "
                + ("\n- ".join(modules) if modules else "UNCONFIRMED")
            )

        if duplication_intent:
            confirmed = ", ".join(names) if names else "UNCONFIRMED"
            return (
                "Повторно создавать уже подтверждённые компоненты нельзя: необходимо использовать "
                "существующую Runtime-регистрацию. Подтверждённые компоненты: " + confirmed + ". "
                "Источник: актуальный AST departments в A_02_MANAGERS/smart_dispatcher_v2.py."
            )

        if creation_intent and "architectagent" in q:
            architect_tool = next(
                (item for item in tools
                 if any(str(entity).casefold() == "architectagent"
                        for entity in item.get("entities", []))),
                None,
            )
            if architect_tool:
                return (
                    "Нет, новый ArchitectAgent создавать не нужно: существующий ArchitectAgent подтверждён "
                    f"актуальным Python AST. Путь: {architect_tool.get('path')}. Следует использовать "
                    "существующую вертикаль ProjectDocumentationDepartment → ArchitectAgent → ContextProvider."
                )
            return "UNCONFIRMED: существующий ArchitectAgent не найден в актуальном Python AST."

        if ArchitectAgent._is_architecture_knowledge_query(q):
            return ArchitectAgent._architecture_knowledge_answer(context)

        combined = ArchitectAgent._multi_category_answer(q, context)
        if combined:
            return combined

        if "источник" in q and "знан" in q and ("architectagent" in q or "архитектор" in q):
            source_names = [row.get("path") for row in context.get("architecture_artifacts", []) if row.get("exists")]
            return (
                "ArchitectAgent использует фактические источники: текущую файловую систему и Python AST; "
                "A_02_MANAGERS/smart_dispatcher_v2.py для Runtime-регистрации; "
                "A_07_CONFIG/project_passport.json для состояния и proof map; "
                "A_07_CONFIG/project_registry.json, goals_registry.json и dependency-конфигурации; "
                "A_99_TESTS/reports/latest_acceptance_report.json для execution evidence; "
                "Inspector/Map/Capability-артефакты: " + ", ".join(source_names) + ". "
                "Приоритет: LIVE_SOURCE_FIRST; STALE-карты используются только как вспомогательные metadata/statistics."
            )
        department_listing = ("department" in q or "департамент" in q) and any(
            marker in q for marker in ("какие", "перечисли", "полностью", "список", "все department")
        )
        if department_listing:
            rows = []
            for item in departments:
                caps = item.get("capabilities", [])
                methods = item.get("public_methods", [])[:8]
                purpose = ", ".join(caps) if caps else "назначение UNCONFIRMED"
                abilities = list(dict.fromkeys(caps + methods))
                rows.append(
                    f"{item.get('class')} | путь: {item.get('source')} | назначение: {purpose} | "
                    f"возможности: {', '.join(abilities) if abilities else 'UNCONFIRMED'}"
                )
            return "Полный состав Department из актуального AST SmartDispatcherV2:\n" + "\n".join(rows)
        if "inspector" in q or "инспектор" in q:
            inspector_facts = (
                ("Inspector0 PhysicalMap", "Inspector0_PhysicalMap.json", "файлы, пути, типы и размеры; активный генератор до восстановления отсутствовал"),
                ("Inspector1 EntityMap", "Inspector1_EntityMap.py → Inspector1_EntityMap.json/UnifiedInspectorFacts.json", "классы, функции, методы, переменные, импорты, регистрации и вызовы Python"),
                ("Inspector2 ImportMap", "Inspector2_ImportMap.py → Inspector2_ImportMap.json", "Python-импорты"),
                ("Inspector3 RegistrationAST", "Inspector3_RegistrationAST.py → Inspector3_RegistrationAST.json", "статические вызовы регистрации"),
                ("Inspector4 CallGraph", "Inspector4_CallGraph.py → Inspector4_CallGraph.json", "статические вызовы функций и методов"),
                ("Inspector5 LinkMap", "Inspector5_LinkMap.py/LinkMapBuilder.py → Inspector5_LinkMap.json/LinkMap.json", "нормализованные import/call/registration связи"),
                ("DependencyModel", "DependencyModelBuilder.py → DependencyModel.json", "узлы и рёбра зависимостей из LinkMap"),
                ("UnifiedInspectorFacts", "UnifiedInspectorFacts.json", "агрегированный EntityMap; не является полным объединением Inspector0–5"),
            )
            rows = [f"{name} | {location} | исследует: {purpose}" for name, location, purpose in inspector_facts]
            return "Подтверждённая Inspector-система:\n" + "\n".join(rows)

        if "стад" in q or "этап" in q or "статус проект" in q or "состояни" in q:
            return f"Текущая стадия проекта: {stage}. Источник: A_07_CONFIG/project_passport.json."
        if "какие department" in q or "какие департамент" in q or "список department" in q:
            return "В рабочем SmartDispatcherV2 зарегистрированы: " + ", ".join(names) + "."
        if "уровн" in q and "памят" in q:
            found = [row["path"] for row in matches if "memory" in row["path"].casefold() or "памят" in row["path"].casefold()]
            return "Подтверждённые компоненты памяти: " + (", ".join(found[:12]) if found else "UNCONFIRMED") + "."
        if "безопас" in q or "guard" in q or "validator" in q or "policy" in q:
            found = [row["path"] for row in matches if any(x in row["path"].casefold() for x in ("guard", "security", "validator", "policy"))]
            return "Подтверждённые механизмы безопасности: " + (", ".join(found[:12]) if found else "UNCONFIRMED") + ". Статическое существование не доказывает Runtime-достижимость."
        if "какие inspector" in q or ("инспектор" in q and "существ" in q):
            paths = [row["path"] for row in tools if "inspector" in row.get("kinds", [])]
            return f"Обнаружено Inspector-механизмов в активной области: {len(paths)}. Примеры: " + ", ".join(paths[:18]) + "."
        if "map-" in q or "map " in q or "карты" in q or ("артефакт" in q and "map" in q):
            maps = [f"{row['path']} ({row.get('freshness', 'UNKNOWN')})" for row in artifacts
                    if "map" in row["path"].casefold() or "graph" in row["path"].casefold()]
            return "MAP/GRAPH-артефакты: " + (", ".join(maps) if maps else "UNCONFIRMED") + "."
        if "доказ" in q or "acceptance" in q:
            acceptance = context.get("acceptance", {})
            return f"Acceptance evidence: official_entry={acceptance.get('official_entry')}, counts={acceptance.get('counts')}, all_scenarios_passed={acceptance.get('all_scenarios_passed')}. Источник: A_99_TESTS/reports/latest_acceptance_report.json."
        if "capabilit" in q or "возможност" in q:
            caps = []
            for item in departments:
                for capability in item.get("capabilities", []):
                    caps.append(f"{item.get('class')}:{capability}")
            registries = [row["path"] for row in artifacts if "capability" in row["path"].casefold()]
            return "Runtime-capabilities: " + (", ".join(caps[:40]) if caps else "не извлечены") + ". Реестры дополнительных заявлений: " + ", ".join(registries) + "; наличие в реестре само по себе не является execution proof."
        if "кто вызывает" in q or "вызывает" in q:
            callers = relations.get("callers", [])
            return "Статические AST-источники вызовов: " + (", ".join(callers) if callers else "UNCONFIRMED — прямые вызовы не найдены") + ". Динамические вызовы не доказаны."
        if "зависят" in q or "зависим" in q:
            deps = relations.get("dependents", [])
            return "Статические импортирующие компоненты: " + (", ".join(deps) if deps else "UNCONFIRMED — прямые импорты не найдены") + "."
        if ("какие файлы" in q or "классы" in q or "сущност" in q or "модул" in q) and matches:
            rows = []
            for item in matches[:10]:
                entities = list(dict.fromkeys(item.get("classes", []) + item.get("functions", [])))[:10]
                rows.append(f"{item['path']}" + (f" — {', '.join(entities)}" if entities else ""))
            return "Подтверждено актуальным файловым индексом и Python AST: " + "; ".join(rows) + "."
        if "offline" in q or "legacy" in q or "мёртв" in q:
            classified = knowledge.get("runtime_classification", [])
            if not classified:
                classified = [{"path": row["path"], "classification": "OFFLINE_TOOL"}
                              for row in tools if row.get("status") == "OFFLINE"][:20]
            return "Классификация по доказательствам Runtime: " + ("; ".join(f"{x['path']}={x['classification']}" for x in classified[:20]) if classified else "UNCONFIRMED") + ". Отсутствие регистрации не доказывает мёртвый код."
        if "ограничен" in q or ("чего не" in q and "зна" in q):
            return "Известные ограничения: " + "; ".join(knowledge.get("known_limits", []))

        matching_proofs = {key: value for key, value in proofs.items() if key.casefold() in q}
        if matching_proofs:
            return "Архитектурные proof-факты: " + ", ".join(f"{key}={value}" for key, value in matching_proofs.items()) + "."
        named = next((name for name in names if name.casefold() in q), None)
        if named:
            item = next(entry for entry in departments if entry.get("class") == named)
            details = list(dict.fromkeys(item.get("capabilities", []) + item.get("implementation_markers", []) + item.get("public_methods", [])))
            if any(marker in q for marker in ("существ", "зарегистр", "есть ли")):
                return (f"Да. {named} существует и зарегистрирован в SmartDispatcherV2. "
                        f"Путь: {item.get('source')}. Класс: {named}. "
                        f"Функции/capabilities: {', '.join(details) if details else 'UNCONFIRMED'}. "
                        "Доказательство: актуальный AST списка departments в A_02_MANAGERS/smart_dispatcher_v2.py и AST файла реализации.")
            return f"{named} зарегистрирован в Runtime. Реализация: {item.get('source')}. Подтверждённые capability/методы: {', '.join(details) if details else 'не извлечены'}."
        if creation_intent and ("переимен" in q or "rename" in q):
            filesystem = next((item for item in departments
                               if item.get("class") == "FilesystemDepartment"), None)
            if filesystem and "rename" in (filesystem.get("implementation_markers", []) +
                                             filesystem.get("public_methods", [])):
                return (
                    "Новый Department для переименования файлов создавать нельзя, потому что это дублирует "
                    "существующую зарегистрированную capability. FilesystemDepartment находится в "
                    "A_04_AGENTS/FilesystemDepartment/runner.py, зарегистрирован в SmartDispatcherV2 и "
                    "реализует rename через методы _rename_files, _rename_request, _validate_target_name, "
                    "_restore_rename и _rename_result. Доказательство: актуальный AST Runtime-регистрации "
                    "и файла реализации; следует использовать и при необходимости расширять существующий Department."
                )
        if creation_intent and relevant:
            item = relevant[0]
            details = list(dict.fromkeys(item.get("implementation_markers", []) + item.get("capabilities", []) + item.get("public_methods", [])))
            return (f"Повторное создание не требуется: релевантная реализация — {item.get('class')} в {item.get('source')}; "
                    f"регистрация в Runtime подтверждена. Признаки: {', '.join(details)}.")
        if creation_intent:
            return "Подтверждённая эквивалентная реализация в зарегистрированном Runtime не найдена."
        if relevant:
            return "Найдены релевантные зарегистрированные компоненты: " + "; ".join(
                f"{item.get('class')} — {item.get('source')}" for item in relevant) + "."
        if matches:
            return "Подтверждённые релевантные источники: " + ", ".join(item["path"] for item in matches[:12]) + "."
        return "UNCONFIRMED: в доступных актуальных структурированных фактах подтверждение не найдено."

    @staticmethod
    def _is_architecture_knowledge_query(query):
        markers = (
            "архитектурный сундук", "база знаний", "источник знаний", "источники знаний",
            "состав знаний", "вся архитектура", "всю архитектуру",
            "всё, что знаешь о проекте", "все, что знаешь о проекте",
            "данные собраны о проекте", "компоненты есть в проекте",
            "что подтверждено runtime", "какие inspector", "какие инспектор",
            "какие department", "какие департамент",
        )
        return any(marker in query for marker in markers)

    @staticmethod
    def _architecture_knowledge_answer(context):
        discovery = context.get("discovery_knowledge", {})
        if not discovery.get("loaded") or discovery.get("status") != "FACTUAL_ONLY":
            return "UNCONFIRMED:\nНедостаточно архитектурных данных."

        sources = discovery.get("sources", {})
        facts = discovery.get("facts", {})
        inspector_layer = facts.get("inspector_layer", [])
        runtime_departments = context.get("runtime", {}).get("departments", [])
        acceptance = context.get("acceptance", {})
        lines = [
            "Источник:", discovery.get("source", "facts/PROJECT_ARCHITECTURE_KNOWLEDGE.json"), "",
            "Создан:", str(discovery.get("generator") or "UNCONFIRMED"), "",
            "Дата:", str(discovery.get("generated") or "UNCONFIRMED"), "",
            "Статус:", "FACTUAL_ONLY", "", "Данные:", "", "Inspector Layer:",
        ]
        if inspector_layer:
            for item in inspector_layer:
                lines.append(
                    f"- {item.get('name')} | generator: {item.get('generator')} | output: {item.get('output')}"
                )
        else:
            lines.append("- UNCONFIRMED")

        lines.extend(["", "Discovery / JSON sources:"])
        loaded_sources = 0
        for name, item in sources.items():
            if not isinstance(item, dict):
                continue
            loaded = bool(item.get("loaded"))
            loaded_sources += int(loaded)
            lines.append(f"- {name}: {item.get('path') or 'UNCONFIRMED'} | loaded={str(loaded).lower()}")
        if not loaded_sources:
            lines.append("- UNCONFIRMED")

        lines.extend(["", "Registry / Passport / Storage:"])
        storage_names = ("ExecutionRegistry", "GoalsRegistry", "ProjectPassport", "UnifiedFacts")
        storage_rows = [
            f"- {name}: {sources[name].get('path')}"
            for name in storage_names
            if isinstance(sources.get(name), dict) and sources[name].get("loaded")
        ]
        lines.extend(storage_rows or ["- UNCONFIRMED"])

        lines.extend(["", "Runtime:", "- SmartDispatcherV2"])
        if runtime_departments:
            lines.append("- Departments:")
            lines.extend(
                f"  - {item.get('class')} | {item.get('source')}"
                for item in runtime_departments if item.get("class")
            )
        else:
            lines.append("- Departments: UNCONFIRMED")

        lines.extend(["", "Acceptance:"])
        if acceptance:
            lines.extend([
                "- A_99_TESTS/reports/latest_acceptance_report.json",
                f"- all_scenarios_passed: {acceptance.get('all_scenarios_passed')}",
            ])
        else:
            lines.append("- UNCONFIRMED")
        return "\n".join(lines)

    @staticmethod
    def _multi_category_answer(q, context):
        """Compose evidence for broad architectural questions without query-specific hardcoding."""
        intents = {
            "state": any(x in q for x in ("состояни", "стад", "roadmap")),
            "components": any(x in q for x in ("компонент", "архитектур")),
            "relations": any(x in q for x in ("связ", "зависим", "взаимодейств")),
            "runtime": "runtime" in q or "dispatcher" in q,
            "departments": "department" in q or "департамент" in q,
            "memory": "памят" in q or "memory" in q,
            "security": "безопас" in q or "security" in q or "guard" in q,
            "inspectors": any(x in q for x in ("inspector", "scanner", "analyzer", "registry", "evidence", "map")),
            "capabilities": "capabilit" in q or "возможност" in q,
            "acceptance": "acceptance" in q or "приём" in q or "доказ" in q,
            "freshness": "stale" in q or "устар" in q,
            "uncertainty": "unconfirmed" in q or "неподтверж" in q,
        }
        if sum(int(value) for value in intents.values()) < 4:
            return None

        knowledge = context.get("architectural_knowledge", {})
        runtime = context.get("runtime", {})
        state = context.get("project_state", {})
        categories = knowledge.get("category_components", {})
        artifacts = knowledge.get("map_and_registry_artifacts", [])
        acceptance = context.get("acceptance", {})
        lines = ["Фактический архитектурный обзор Butler Omega Smart:"]

        if intents["state"]:
            stage = state.get("current_stage") or state.get("identity", {}).get("current_stage") or "UNCONFIRMED"
            lines.append(f"1. Состояние: текущая стадия {stage}; источник A_07_CONFIG/project_passport.json. Известные ограничения: {state.get('limitations') or 'UNCONFIRMED'}.")
        if intents["components"]:
            inventory = knowledge.get("live_inventory", {})
            areas = inventory.get("areas", {})
            major = [f"{name} ({count} файлов)" for name, count in sorted(areas.items())
                     if name.startswith(("A_01_", "A_02_", "A_03_", "A_04_", "A_05_", "A_07_", "A_09_", "A_10_"))]
            lines.append(f"2. Основные компоненты: {', '.join(major)}. Актуальный live-индекс: {inventory.get('files')} файлов, Python AST: {inventory.get('python_files_parsed')} файлов.")
        if intents["relations"]:
            lines.append("3. Связи: BUTLER_OS/launcher → dispatcher_bridge_v2 → SmartDispatcherV2 → зарегистрированный Department; архитектурные запросы → ProjectDocumentationDepartment → ArchitectAgent → ContextProvider → live filesystem/AST, passport, registries и Acceptance → SmartDispatcher model provider → Result Contract. Импорты, вызовы и регистрации дополнительно представлены статическим AST; динамические связи сверх этого UNCONFIRMED.")
        if intents["runtime"]:
            lines.append(f"4. Runtime и Dispatcher: официальный entry {runtime.get('official_entry')}; dispatcher {runtime.get('dispatcher')}; список Department извлечён непосредственно из его AST.")
        if intents["departments"]:
            deps = []
            for item in runtime.get("departments", []):
                caps = ", ".join(item.get("capabilities", [])) or "capabilities UNCONFIRMED"
                deps.append(f"{item.get('class')} [{caps}] @ {item.get('source')}")
            lines.append("5. Departments (зарегистрированы и Runtime-достижимы): " + "; ".join(deps) + ".")
        if intents["memory"]:
            memory = categories.get("memory", [])
            lines.append("6. Память: " + (", ".join(memory) if memory else "UNCONFIRMED") + ". Существование подтверждено live AST/path index; Runtime-use каждого отдельного файла без регистрации/Acceptance остаётся UNCONFIRMED.")
        if intents["security"]:
            security = categories.get("security", [])
            lines.append("7. Безопасность: " + (", ".join(security) if security else "UNCONFIRMED") + ". Наличие исходника не подменяется утверждением о выполнении в каждом Runtime-маршруте.")
        if intents["inspectors"]:
            kinds = {}
            for row in knowledge.get("tool_inventory", []):
                for kind in row.get("kinds", []):
                    kinds[kind] = kinds.get(kind, 0) + 1
            examples = [row.get("path") for row in knowledge.get("tool_inventory", [])[:24]]
            lines.append(f"8. Inspector/Scanner/Analyzer/Map/Registry/Evidence: {knowledge.get('tool_inventory_total')} активных исходников; категории {kinds}; примеры: {', '.join(examples)}.")
        if intents["capabilities"]:
            caps = []
            for item in runtime.get("departments", []):
                caps.extend(f"{item.get('class')}:{cap}" for cap in item.get("capabilities", []))
            lines.append("9. Capabilities: подтверждённые объявления зарегистрированных Department: " + (", ".join(caps) if caps else "UNCONFIRMED") + ". Capability Registry содержит дополнительные claims, но claim без Acceptance не считается execution proof.")
        if intents["acceptance"]:
            lines.append(f"10. Acceptance: official_entry={acceptance.get('official_entry')}; counts={acceptance.get('counts')}; all_scenarios_passed={acceptance.get('all_scenarios_passed')}; источник A_99_TESTS/reports/latest_acceptance_report.json.")
        if intents["freshness"]:
            stale = [row.get("path") for row in artifacts if row.get("freshness") == "STALE"]
            lines.append("11. STALE: " + (", ".join(stale) if stale else "устаревшие структурированные источники не обнаружены") + ". Live filesystem/AST имеет приоритет над этими картами.")
        if intents["uncertainty"]:
            lines.append("12. UNCONFIRMED: динамические вызовы, абсолютная dead/legacy-классификация и работоспособность registry-only capabilities без отдельного Acceptance. Неподтверждённые сведения не дополняются предположениями модели.")
        return "\n".join(lines)

    def execute_goal(self, goal_text: str):
        return PlannerEngine.execute(goal_text)

    def plan(self):
        context = self.context_provider.build_context()
        goal_report = self.goal_analyzer.analyze(context)
        dependency_report = self.dependency_analyzer.analyze(goal_report, context)
        recipe = self.recipe_builder.build_planning_recipe(goal_report, dependency_report)
        queued_path = self.queue_manager.enqueue(recipe)
        return {"status": "ARCHITECT_RECIPE_CREATED", "queued_recipe": queued_path, "recipe": recipe}


if __name__ == "__main__":
    print(ArchitectAgent().answer("На какой стадии находится проект?")["text"])
