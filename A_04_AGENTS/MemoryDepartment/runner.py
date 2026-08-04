from A_04_AGENTS.base_department import BaseDepartment

# -*- coding: utf-8 -*-

from pathlib import Path
from time import perf_counter
import json
import re

from A_07_MEMORY import memory_router
from A_07_MEMORY.memory_orchestrator_v2 import MemoryOrchestratorV2
from A_07_MEMORY.profile_manager import get_fact, get_memory_summary, load_profile

class MemoryDepartment(BaseDepartment):

    NAME = "MEMORY"
    name = "MEMORY"
    VERSION = "1.0"
    CAPABILITIES = ("read_memory_sources", "write_profile_fact")
    DEPENDENCIES = (
        "A_04_AGENTS.base_department.BaseDepartment",
        "A_07_MEMORY.memory_router",
        "A_07_MEMORY.profile_manager",
    )
    DATA_READS = (
        "A_05_STORAGE/USER_MEMORY.md",
        "A_07_CONFIG/project_state.json",
        "A_05_STORAGE/session_history.jsonl",
    )
    DATA_WRITES = (
        "A_05_STORAGE/user_profile.json",
        "A_05_STORAGE/USER_MEMORY.md",
    )

    def __init__(self):
        self.root = Path(__file__).resolve().parents[2]

        self.permanent = self.root / "A_05_STORAGE" / "USER_MEMORY.md"
        self.project   = self.root / "A_07_CONFIG" / "project_state.json"
        self.session   = self.root / "A_05_STORAGE" / "session_history.jsonl"
        self.memory = MemoryOrchestratorV2()

    def can_handle(self, query: str, context: dict = None) -> bool:
        q = (query or "").lower()

        if "не обращайся" in q and "memorydepartment" in q:
            return False

        # Advisory questions are synthesized by CHAT with the selected memory
        # packet; MEMORY owns storage and focused retrieval, not final advice.
        if any(stem in q for stem in ("предпоч", "лучше", "следует")) and any(
            stem in q for stem in ("формат", "язык", "команд", "использ")
        ):
            return False

        personal_reference = bool(
            re.search(r"\bмо(?:й|я|ё|е|и|ю)\b", q, re.I)
            or "обо мне" in q or "своих" in q
        )
        personal_memory = (
            any(stem in q for stem in ("помн", "памят", "сохраненн", "сохранённ", "знан"))
            and (personal_reference or "активн" in q)
        )
        media_knowledge = (
            any(stem in q for stem in ("изображ", "аудио", "видео", "медиа"))
            and any(stem in q for stem in ("знан", "проект", "сохран", "связан"))
        )

        keys = [
            "департамент памяти", "что ты помнишь",
            "что помнишь обо мне", "кто я", "мой любимый", "контекст",
            "запомни", "найди", "что ты знаешь обо мне", "как меня зовут",
            "департамент памяти", "что ты помнишь", 
            "что помнишь обо мне", "кто я", "мой любимый", "контекст",
            "бюджет сессии", "контекстный бюджет", "наблюдения", 
            "системные наблюдения", "memory", "паспорт", "реестр задач",
            "запомни", "что ты знаешь обо мне", "как меня зовут",
            "какой мой", "что знаешь обо мне"
            , "что ты умеешь", "какие department", "что находится внутри",
            "что уже сделано", "что уже завершено", "что осталось",
            "что ещё не реализовано", "что еще не реализовано",
            "что изменилось после последнего обновления", "расскажи о себе",
            "что ты знаешь о своём проекте", "что ты знаешь о своем проекте"
            , "какая у тебя память", "как устроена твоя память",
            "откати знание", "откатить знание", "свяжи знание"
        ]

        return personal_memory or media_knowledge or any(k in q for k in keys)

    def execute(self, query: str, context: dict = None, **kwargs) -> dict:

        started = perf_counter()
        query = (query or "").strip()

        rollback = re.search(r"откат\w*\s+знан\w*\s+(.+?)\s+(?:к|до)\s+верс\w*\s+(\d+)", query, re.I)
        if rollback:
            key = rollback.group(1).strip()
            if "/" not in key:
                key = f"profile/facts/{key.casefold()}"
            outcome = self.memory.rollback_knowledge(key, int(rollback.group(2)))
            return {
                "ok": bool(outcome.get("ok")), "department": self.NAME,
                "model": "SemanticMemory", "latency_ms": max(0, int((perf_counter() - started) * 1000)),
                "text": (f"Активная версия знания переключена на v{rollback.group(2)}."
                         if outcome.get("ok") else "Версия знания не найдена."),
                "error": outcome.get("error"),
                "metadata": {"mode": "controlled_evolution", "action": "rollback", "result": outcome},
            }

        media_link = re.search(
            r"свяж\w*\s+знан\w*\s+(.+?)\s+с\s+(документ\w*|изображен\w*|аудио|видео)\s+(.+)$",
            query, re.I,
        )
        if media_link:
            key = media_link.group(1).strip()
            if "/" not in key:
                key = f"profile/facts/{key.casefold()}"
            kind_word = media_link.group(2).casefold()
            kind = "document" if kind_word.startswith("документ") else (
                "image" if kind_word.startswith("изображ") else kind_word
            )
            outcome = self.memory.link_knowledge_media(
                key, kind, media_link.group(3).strip(), source="MemoryDepartment:user_request",
            )
            return {
                "ok": bool(outcome.get("ok")), "department": self.NAME,
                "model": "SemanticMemory", "latency_ms": max(0, int((perf_counter() - started) * 1000)),
                "text": "Связь знания с медиа сохранена." if outcome.get("ok") else "Знание не найдено.",
                "error": outcome.get("error"),
                "metadata": {"mode": "knowledge_linking", "action": "link_media", "result": outcome},
            }

        try:
            self.memory.add_session_event("user", query)
        except Exception as exc:
            return self._error_result(
                started,
                "DK02_SESSION_WRITE_ERROR",
                "Не удалось записать запрос в память сессии.",
                metadata={"exception_type": type(exc).__name__},
            )

        if query.lower().startswith("запомни"):
            return self._write_memory(query, started)

        if self._is_self_knowledge_query(query):
            return self._self_knowledge_result(query, started)

        result = {
            "ok": True,
            "department": self.NAME,
            "model": None,
            "latency_ms": 0,
            "text": "",
            "error": None,
            "metadata": {
                "mode": "read_only",
                "sources": {},
            },
            "permanent":"",
            "project":"",
            "session":""
        }

        sources = (
            ("permanent", self.permanent, "ProfileManager/ProfileSync", True, None),
            ("project", self.project, "ProjectState", False, None),
        )

        for source_name, path, owner, required, tail_lines in sources:
            source_info = {
                "path": path.relative_to(self.root).as_posix(),
                "owner": owner,
                "required": required,
                "status": "missing",
            }
            result["metadata"]["sources"][source_name] = source_info

            if not path.exists():
                if required:
                    result["ok"] = False
                    result["error"] = "MEMORY_REQUIRED_SOURCE_MISSING"
                continue

            try:
                content = path.read_text(encoding="utf-8-sig")
                if tail_lines is not None:
                    content = "\n".join(content.splitlines()[-tail_lines:])
                result[source_name] = content
                source_info["status"] = "read"
            except (OSError, UnicodeError) as exc:
                source_info["status"] = "error"
                source_info["error_type"] = type(exc).__name__
                result["ok"] = False
                result["error"] = "MEMORY_SOURCE_READ_ERROR"

        try:
            result["permanent"] = get_memory_summary()
            result["metadata"]["sources"]["permanent"]["projection"] = "ProfileManager.get_memory_summary"
        except Exception as exc:
            result["ok"] = False
            result["error"] = "MEMORY_SOURCE_READ_ERROR"
            result["metadata"]["sources"]["permanent"]["error_type"] = type(exc).__name__

        result["text"] = self._answer_memory_query(query, result["permanent"])
        result["metadata"]["response_mode"] = "relevant_profile_answer"
        try:
            result["metadata"]["dk02"] = self.memory.build_context(semantic_query=query)
            self.memory.add_session_event("assistant", result["text"])
        except Exception as exc:
            result["ok"] = False
            result["error"] = "DK02_CONTEXT_ERROR"
            result["metadata"]["dk02_error_type"] = type(exc).__name__
        result["latency_ms"] = max(0, int((perf_counter() - started) * 1000))

        return result

    def _answer_memory_query(self, query: str, summary: str) -> str:
        q = query.lower().strip().rstrip("?.!")

        if any(word in q for word in ("изображ", "аудио", "видео", "медиа")) and "связ" in q:
            links = self.memory.get_media_links()
            if not links:
                return "Связанные изображения, аудио или видео не найдены."
            return "Связанные медиа: " + "; ".join(
                f"{entry['media'].get('type')}: {entry['media'].get('path')} "
                f"(знание: {entry['knowledge'].get('key')})" for entry in links[:10]
            )

        # Controlled knowledge is queried by meaning; do not reinterpret the
        # whole natural-language question as a literal profile key.
        knowledge = self.memory.search_knowledge(query)
        if knowledge:
            item = knowledge[0]
            active = item.get("knowledge", {})
            media = item.get("related_media", [])
            value = active.get("value")
            if any(word in q for word in ("изображ", "аудио", "видео", "медиа")):
                if not media:
                    return "Связанные изображения, аудио или видео не найдены."
                return "Связанные медиа: " + "; ".join(
                    f"{entry.get('type')}: {entry.get('path')}" for entry in media
                )
            if value is not None:
                return f"Активное значение: {value}."

        if q in {"кто я", "как меня зовут"}:
            name = get_fact("user_name", "name")
            return f"Вас зовут {name}." if name else "Имя пользователя не сохранено."

        if "любимый цвет" in q:
            color = get_fact("preferences", "favorite_color")
            return f"Ваш любимый цвет — {color}." if color else "Любимый цвет не сохранён."

        match = re.search(r"какой мой\s+(.+)$", q)
        if match:
            key = match.group(1).strip()
            value = get_fact("facts", key)
            return f"Ваш {key} — {value}." if value else f"Факт «{key}» не найден в памяти."

        profile = load_profile()
        words = {word for word in re.findall(r"[a-zа-я0-9_-]+", q, re.I) if len(word) >= 3}
        matches = []
        for section, values in profile.items():
            if not isinstance(values, dict):
                continue
            for key, payload in values.items():
                value = payload.get("value") if isinstance(payload, dict) else payload
                searchable = set(re.findall(r"[a-zа-я0-9_-]+", f"{key} {value}".lower(), re.I))
                if words & searchable:
                    matches.append((key, value))
        if matches:
            return "; ".join(f"{key} = {value}" for key, value in matches[:5])

        if any(marker in q for marker in ("что ты знаешь обо мне", "что знаешь обо мне", "что ты помнишь обо мне")):
            return summary or "Сохранённых персональных фактов нет."

        if "проект" in q:
            return summary or "Сохранённых сведений о проекте нет."

        return summary or "Сохранённых фактов нет."

    def _is_self_knowledge_query(self, query: str) -> bool:
        q = query.casefold()
        markers = (
            "что ты умеешь", "какие department", "что находится внутри",
            "что уже сделано", "что уже завершено", "что осталось",
            "что ещё не реализовано", "что еще не реализовано",
            "что изменилось после последнего обновления", "расскажи о себе",
            "что ты знаешь о своём проекте", "что ты знаешь о своем проекте",
            "какая у тебя память", "как устроена твоя память",
        )
        return any(marker in q for marker in markers)

    def _read_json_artifact(self, relative_path, sources):
        path = self.root / relative_path
        info = {"path": relative_path.as_posix(), "status": "missing"}
        sources.append(info)
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
            info["status"] = "read"
            return data
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            info.update({"status": "error", "error_type": type(exc).__name__})
            return None

    def _read_text_artifact(self, relative_path, sources):
        path = self.root / relative_path
        info = {"path": relative_path.as_posix(), "status": "missing"}
        sources.append(info)
        if not path.exists():
            return ""
        try:
            raw = path.read_bytes()
            try:
                text = raw.decode("utf-8-sig")
            except UnicodeDecodeError:
                text = raw.decode("utf-16")
            info["status"] = "read"
            return text
        except (OSError, UnicodeError) as exc:
            info.update({"status": "error", "error_type": type(exc).__name__})
            return ""

    def _load_project_knowledge(self):
        sources = []
        artifacts = {
            "capability": self._read_json_artifact(Path("A_00_ARCHITECTURE/BUTLER_CAPABILITY_AUDIT.json"), sources),
            "project_state": self._read_json_artifact(Path("A_00_ARCHITECTURE/PROJECT_STATE.json"), sources),
            "memory_index": self._read_json_artifact(Path("A_00_ARCHITECTURE/PROJECT_MEMORY_INDEX.json"), sources),
            "acceptance": self._read_json_artifact(Path("A_99_TESTS/reports/latest_acceptance_report.json"), sources),
            "passport": self._read_text_artifact(Path("PASSPORT_SUMMARY.md"), sources),
        }
        roadmap = Path("ROADMAP_6_0_BUTLER_OMEGA_SMART_UPDATED.md")
        if not (self.root / roadmap).exists():
            roadmap = Path("ROADMAP_6_0_BUTLER_OMEGA_SMART.md")
        artifacts["roadmap"] = self._read_text_artifact(roadmap, sources)
        inspector_names = (
            "Inspector0_PhysicalMap.json", "Inspector1_EntityMap.json",
            "Inspector2_ImportMap.json", "Inspector3_RegistrationAST.json",
            "Inspector3_RegistrationMap.json", "Inspector4_CallGraph.json",
            "Inspector5_DependencyGraph.json",
        )
        artifacts["inspectors"] = {
            name: self._read_json_artifact(Path(name), sources) for name in inspector_names
        }
        return artifacts, sources

    @staticmethod
    def _markdown_section(text, heading):
        match = re.search(
            rf"(?ms)^##[ \t]+{re.escape(heading)}[ \t]*\r?$\n(.*?)(?=^##[ \t]+|\Z)", text or ""
        )
        if not match:
            return []
        return [line[2:].strip() for line in match.group(1).splitlines() if line.startswith("- ")]

    @staticmethod
    def _unique(values):
        return list(dict.fromkeys(str(value).strip() for value in values if str(value).strip()))

    def _capabilities_answer(self, data):
        audit = data.get("capability") or {}
        groups = audit.get("capabilities") if isinstance(audit, dict) else None
        values = []
        user_groups = {"document_processing", "vision_ocr", "memory", "search"}
        if isinstance(groups, dict):
            for name, items in groups.items():
                if name not in user_groups or not isinstance(items, list):
                    continue
                values.extend(items)
        values = self._unique(values)
        return "Возможности по Capability Audit: " + ("; ".join(values) if values else "информация отсутствует в артефактах.")

    def _departments(self, data):
        acceptance = data.get("acceptance") or {}
        values = []
        for item in acceptance.get("results", []) if isinstance(acceptance, dict) else []:
            department = item.get("actual_department")
            if department and department not in {"INFRASTRUCTURE", "NONE"}:
                values.append(department)
        if not values:
            values = self._markdown_section(data.get("passport", ""), "DEPARTMENTS")
        return self._unique(values)

    def _departments_answer(self, data):
        departments = self._departments(data)
        return "Активные Department: " + (", ".join(departments) if departments else "информация отсутствует в артефактах.")

    def _memory_answer(self, data):
        components = self._markdown_section(data.get("passport", ""), "MEMORY")
        index = data.get("memory_index") or {}
        built = index.get("built", []) if isinstance(index, dict) else []
        components.extend(item for item in built if "MEMORY" in str(item).upper())
        components = self._unique(components)
        if not components:
            return "Архитектура памяти: описание отсутствует в существующих артефактах."
        return (
            "Архитектура памяти представлена найденными компонентами: "
            + ", ".join(components)
            + ". Формальная схема уровней в источниках не обозначена, поэтому дополнительные уровни не предполагаются."
        )

    def _department_answer(self, query, data):
        match = re.search(r"внутри\s+([A-Za-z0-9_]+Department)", query, re.IGNORECASE)
        target = match.group(1) if match else "MemoryDepartment"
        physical = (data.get("inspectors") or {}).get("Inspector0_PhysicalMap.json") or {}
        entities = (data.get("inspectors") or {}).get("Inspector1_EntityMap.json") or {}
        paths = {item.get("id"): item.get("relative_path") for item in physical.get("payload", [])}
        found = None
        found_item = None
        found_path = None
        for item in entities.get("payload", []):
            for cls in item.get("classes", []):
                if str(cls.get("name", "")).casefold() == target.casefold():
                    found, found_item, found_path = cls, item, paths.get(item.get("id")); break
            if found:
                break
        if not found:
            return f"Department {target}: информация отсутствует в Inspector v3.1."
        methods = [method.get("name") for method in found.get("methods", []) if method.get("name") and not method.get("name").startswith("_")]
        imports = self._unique(
            entry.get("module") for entry in (found_item or {}).get("imports", []) if entry.get("module")
        )
        return (
            f"Назначение Department {target}: зарегистрированный компонент {found_path or 'путь не указан'}. "
            f"Возможности по Inspector: {', '.join(methods) if methods else 'публичные методы не указаны'}. "
            f"Используемые данные/зависимости по Inspector: {', '.join(imports) if imports else 'не указаны'}. "
            "Ограничения: для этого Department в использованных артефактах не указаны."
        )

    def _roadmap_status(self, data, completed):
        roadmap = data.get("roadmap", "")
        index = data.get("memory_index") or {}
        values = list(index.get("built" if completed else "next_work", [])) if isinstance(index, dict) else []
        if completed:
            values.extend(re.findall(r"(?m)^##\s+(.+?)\s*$\n\s*Статус:\s*COMPLETED[^\n]*", roadmap))
            label = "Завершённые статусы"
        else:
            values.extend(re.findall(r"(?im)^.*(?:PENDING|TODO|IN PROGRESS|не реализовано).*$", roadmap))
            label = "Незавершённые пункты"
        values = self._unique(values)
        return f"{label}: " + ("; ".join(values) if values else "информация отсутствует в текущих артефактах.")

    def _project_answer(self, data):
        state = data.get("project_state") or {}
        acceptance = data.get("acceptance") or {}
        counts = acceptance.get("counts", {}) if isinstance(acceptance, dict) else {}
        index = data.get("memory_index") or {}
        return (
            f"Проект: {state.get('project') or index.get('project') or 'информация отсутствует'}. "
            f"Версия архитектуры: {state.get('architecture_version', 'не указана')}; approved: {state.get('approved', 'не указано')}. "
            f"Acceptance: PASS {counts.get('PASS', 'None')}, FAIL {counts.get('FAIL', 'None')}, SKIP {counts.get('SKIP', 'None')}. "
            f"Текущая работа: {', '.join(index.get('current_work', [])) if isinstance(index, dict) and index.get('current_work') else 'не указана'}. "
            f"Последнее обновление отчёта: {acceptance.get('timestamp', state.get('generated_at', 'не указано'))}."
        )

    def _build_self_knowledge_answer(self, query, data):
        q = query.casefold()
        if "что ты умеешь" in q:
            return self._capabilities_answer(data)
        if "какие department" in q:
            return self._departments_answer(data)
        if "какая у тебя память" in q or "как устроена твоя память" in q:
            return self._memory_answer(data)
        if "что находится внутри" in q:
            return self._department_answer(query, data)
        if "что уже" in q:
            return self._roadmap_status(data, True)
        if "что осталось" in q or "не реализовано" in q:
            return self._roadmap_status(data, False)
        if "что изменилось" in q:
            return self._project_answer(data)
        if "расскажи о себе" in q:
            return "Я — " + self._project_answer(data) + " " + self._capabilities_answer(data) + " " + self._departments_answer(data) + " " + self._memory_answer(data)
        return self._project_answer(data)

    def _self_knowledge_result(self, query, started):
        artifacts, sources = self._load_project_knowledge()
        text = self._build_self_knowledge_answer(query, artifacts)
        try:
            self.memory.add_session_event("assistant", text)
        except Exception:
            pass
        return {
            "ok": True,
            "department": self.NAME,
            "model": "ProjectArtifacts",
            "latency_ms": max(0, int((perf_counter() - started) * 1000)),
            "text": text,
            "error": None,
            "metadata": {"mode": "read_only", "response_mode": "project_self_knowledge", "sources": sources},
        }

    def _write_memory(self, query: str, started: float) -> dict:
        parsed = memory_router.parse_memory_command(query)
        if not parsed:
            return self._error_result(
                started,
                "INVALID_MEMORY_COMMAND",
                "Команда записи памяти должна содержать непустые ключ и значение.",
            )

        section, key, value = parsed
        previous_value = get_fact(section, key)

        try:
            evolution = self.memory.evolve_knowledge(
                f"profile/{section}/{key}", value,
                provenance="MemoryDepartment:user_request",
            )
        except Exception as exc:
            return self._error_result(
                started, "KNOWLEDGE_EVOLUTION_ERROR",
                "Не удалось зафиксировать версию знания.",
                metadata={"exception_type": type(exc).__name__},
            )

        if evolution.get("relation") == "CONFLICTS_WITH_EXISTING":
            try:
                self.memory.rollback_knowledge(
                    f"profile/{section}/{key}", evolution["version"]
                )
                evolution["active_version"] = evolution["version"]
            except Exception as exc:
                return self._error_result(
                    started, "KNOWLEDGE_ACTIVATION_ERROR",
                    "Новая версия знания сохранена, но не активирована.",
                    metadata={"exception_type": type(exc).__name__},
                )

        try:
            written = memory_router.remember(query)
        except Exception as exc:
            return self._error_result(
                started,
                "MEMORY_WRITE_ERROR",
                "Не удалось сохранить факт в долговременной памяти.",
                metadata={"exception_type": type(exc).__name__},
            )

        if not written:
            return self._error_result(
                started,
                "MEMORY_WRITE_REJECTED",
                "Команда записи памяти отклонена.",
            )

        try:
            self.memory.index_semantic(
                f"{key} = {value}",
                path=f"memory://profile/{section}/{key}",
                tags=["profile", section, key],
                entities=[key, value],
            )
            self.memory.add_session_event("assistant", f"Факт сохранён: {key} = {value}")
        except Exception as exc:
            return self._error_result(
                started,
                "DK02_INDEX_WRITE_ERROR",
                "Факт сохранён в профиле, но не проиндексирован DK02.",
                metadata={"exception_type": type(exc).__name__},
            )

        return {
            "ok": True,
            "department": self.NAME,
            "model": "ProfileManager",
            "latency_ms": max(0, int((perf_counter() - started) * 1000)),
            "text": f"Факт сохранён: {key} = {value}",
            "error": None,
            "metadata": {
                "mode": "read_write",
                "action": "write",
                "dk02_bridge": "MemoryOrchestratorV2",
                "section": section,
                "key": key,
                "value": value,
                "replaced": previous_value is not None,
                "knowledge_evolution": evolution,
            },
        }

    def _error_result(self, started, error, text, metadata=None):
        return {
            "ok": False,
            "department": self.NAME,
            "model": "ProfileManager",
            "latency_ms": max(0, int((perf_counter() - started) * 1000)),
            "text": text,
            "error": error,
            "metadata": dict(metadata or {}, mode="read_write"),
        }

