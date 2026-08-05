# -*- coding: utf-8 -*-

import json
import re
import subprocess
import time
from datetime import date, datetime, timedelta
from pathlib import Path

from A_04_AGENTS.base_department import BaseDepartment


class HomeDepartment(BaseDepartment):
    NAME = "HOME"
    VERSION = "1.0"
    CAPABILITIES = (
        "reminder_lifecycle", "document_watch", "inventory",
        "program_registry", "confirmed_program_launch", "home_status",
        "butler_identity",
    )
    DEPENDENCIES = ("A_04_AGENTS.base_department.BaseDepartment",)
    DATA_READS = ("A_05_STORAGE/home_assistant.json",)
    DATA_WRITES = ("A_05_STORAGE/home_assistant.json",)

    def __init__(self):
        self.root = Path(__file__).resolve().parents[2]
        self.storage_path = self.root / "A_05_STORAGE" / "home_assistant.json"
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def can_handle(self, query: str, context: dict = None) -> bool:
        context = context or {}
        if context.get("image_followup"):
            return False

        q = (query or "").lower()
        if any(token in q for token in (
            "нарисуй", "создай картинку", "создай изображение",
            "озвучь", "скажи голосом", ".mp4", "видео",
        )):
            return False
        return (
            q.rstrip("?.!") == "кто ты"
            or self._is_status_query(q)
            or self._is_reminder_close(q)
            or self._is_reminder_update(q)
            or self._is_reminder_create(q)
            or self._is_program_register(q)
            or self._is_program_launch(q)
            or self._is_inventory_query(q)
            or self._is_document_query(q)
        )

    def execute(self, query: str, context: dict = None, **kwargs) -> dict:
        start = time.time()
        text = (query or "").strip()
        q = text.lower()
        context = dict(context or {})

        try:
            data = self._load()
            should_save = False

            if q.rstrip("?.!") == "кто ты":
                from A_07_CONFIG.project_passport_loader import ProjectPassportLoader
                identity = ProjectPassportLoader().get_identity()
                answer = (
                    f"Я Butler Omega Smart — локальный цифровой помощник. "
                    f"Версия: {identity.get('version', 'UNKNOWN')}."
                )
            elif self._is_status_query(q):
                answer = self._build_status(data)
            elif self._is_reminder_close(q):
                answer = self._close_reminder(data, text)
                should_save = True
            elif self._is_reminder_update(q):
                answer = self._update_reminder(data, text)
                should_save = True
            elif self._is_program_register(q):
                if not self._program_registration_parts(text):
                    raise ValueError("HOME_INVALID_PROGRAM_REGISTRATION")
                answer = self._register_program(data, text)
                should_save = True
            elif self._is_program_launch(q):
                if not context.get("confirmed"):
                    raise PermissionError("HOME_PROGRAM_LAUNCH_REQUIRES_CONFIRMATION")
                answer = self._launch_program(data, text)
            elif self._is_inventory_query(q):
                answer = self._add_inventory_item(data, text)
                should_save = True
            elif self._is_document_query(q):
                answer = self._add_document_watch(data, text)
                should_save = True
            elif self._is_reminder_create(q):
                if self._has_invalid_explicit_date(q):
                    raise ValueError("HOME_INVALID_DATE")
                answer = self._add_reminder(data, text)
                should_save = True
            else:
                raise ValueError("HOME_INTENT_UNCONFIRMED")

            if should_save:
                self._save(data)
            ok = True
            error = None
        except Exception as exc:
            answer = f"HOME: не удалось выполнить команду: {exc}"
            ok = False
            error = str(exc)

        return {
            "ok": ok,
            "department": self.NAME,
            "model": "HomeDepartment",
            "latency_ms": int((time.time() - start) * 1000),
            "text": answer,
            "error": error,
            "metadata": {
                "storage": self.storage_path.relative_to(self.root).as_posix(),
                "mode": "read_write",
            },
        }

    def _empty(self):
        return {
            "schema_version": 1,
            "reminders": [],
            "documents": [],
            "inventory": [],
            "programs": [],
            "updated_at": None
        }

    def _load(self):
        if not self.storage_path.exists():
            return self._empty()

        try:
            data = json.loads(self.storage_path.read_text(encoding="utf-8-sig"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ValueError("HOME_STORAGE_READ_ERROR") from exc

        if not isinstance(data, dict):
            raise ValueError("HOME_STORAGE_INVALID_ROOT")

        base = self._empty()
        base.update(data)
        for key in ["reminders", "documents", "inventory", "programs"]:
            if not isinstance(base.get(key), list):
                base[key] = []
        return base

    def _save(self, data):
        data["updated_at"] = datetime.now().isoformat(timespec="seconds")
        self.storage_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def _is_status_query(self, q):
        return any(x in q for x in [
            "что по дому", "статус дома", "домашний статус", "сводка",
            "что срочно", "какие сроки", "что нужно сделать", "список дел"
        ])

    def _is_inventory_query(self, q):
        return any(x in q for x in ["купить", "продукт", "заканчивается", "запас", "холодильник", "лекарств"])

    def _is_document_query(self, q):
        return any(x in q for x in ["страхов", "осаго", "каско", "медкарт", "медицинск", "паспорт", "карта"]) and self._extract_date(q)

    def _is_program_register(self, q):
        return any(x in q for x in ["добавь программу", "зарегистрируй программу", "запомни программу"])

    def _is_program_launch(self, q):
        return any(x in q for x in ["запусти", "открой приложение", "запуск программы"])

    def _is_reminder_close(self, q):
        return bool(re.search(r"(?:закрой|заверши|выполнено)\s+(rem-\d+)", q))

    def _is_reminder_update(self, q):
        return bool(re.search(r"(?:обнови|измени)\s+(rem-\d+)\s*:", q))

    @staticmethod
    def _is_reminder_create(q):
        return bool(re.match(
            r"^\s*(?:напомни(?:\s+мне)?|(?:создай|добавь|поставь)\s+напоминание)"
            r"(?:\s|:|$)",
            str(q or ""),
        ))

    def _has_invalid_explicit_date(self, text):
        candidate = re.search(r"\b(20\d{2}-\d{1,2}-\d{1,2}|\d{1,2}[.\/]\d{1,2}[.\/]20\d{2})\b", text)
        return bool(candidate and self._extract_date(candidate.group(1)) is None)

    def _extract_date(self, text):
        text = text or ""

        iso = re.search(r"\b(20\d{2}-\d{1,2}-\d{1,2})\b", text)
        if iso:
            try:
                return datetime.strptime(iso.group(1), "%Y-%m-%d").date().isoformat()
            except ValueError:
                pass

        ru = re.search(r"\b(\d{1,2})[.\/](\d{1,2})[.\/](20\d{2})\b", text)
        if ru:
            try:
                d, m, y = [int(x) for x in ru.groups()]
                return date(y, m, d).isoformat()
            except ValueError:
                pass

        today = date.today()
        if "сегодня" in text:
            return today.isoformat()
        if "завтра" in text:
            return (today + timedelta(days=1)).isoformat()

        rel = re.search(r"через\s+(\d+)\s+(день|дня|дней|неделю|недели|недель|месяц|месяца|месяцев)", text)
        if rel:
            num = int(rel.group(1))
            unit = rel.group(2)
            if unit.startswith("недел"):
                num *= 7
            elif unit.startswith("месяц"):
                num *= 30
            return (today + timedelta(days=num)).isoformat()

        return None

    def _next_id(self, items, prefix):
        numbers = []
        for item in items:
            raw = str(item.get("id", ""))
            if raw.startswith(prefix + "-"):
                try:
                    numbers.append(int(raw.split("-", 1)[1]))
                except ValueError:
                    pass
        return f"{prefix}-{max(numbers, default=0) + 1:04d}"

    def _clean_title(self, text):
        title = re.sub(
            r"^(напомни|напоминание|добавь|запомни|нужно|надо|поставь|создай)\s*",
            "",
            text.strip(),
            flags=re.IGNORECASE
        )
        title = re.sub(r"\b(20\d{2}-\d{1,2}-\d{1,2}|\d{1,2}[.\/]\d{1,2}[.\/]20\d{2})\b", "", title)
        title = re.sub(r"\s+", " ", title).strip(" .,:;-")
        return title or text.strip()

    def _add_reminder(self, data, text):
        due = self._extract_date(text)
        item = {
            "id": self._next_id(data["reminders"], "REM"),
            "title": self._clean_title(text),
            "due": due,
            "status": "open",
            "created_at": datetime.now().isoformat(timespec="seconds")
        }
        data["reminders"].append(item)

        if due:
            return f"HOME: напоминание добавлено: {item['title']} | срок {due} | {item['id']}"
        return f"HOME: задача добавлена без даты: {item['title']} | {item['id']}"

    def _add_document_watch(self, data, text):
        due = self._extract_date(text)
        doc_type = "document"
        q = text.lower()
        if "страх" in q or "осаго" in q or "каско" in q:
            doc_type = "car_insurance"
        elif "мед" in q:
            doc_type = "medical"
        elif "паспорт" in q:
            doc_type = "passport"

        item = {
            "id": self._next_id(data["documents"], "DOC"),
            "type": doc_type,
            "title": self._clean_title(text),
            "due": due,
            "status": "watch",
            "created_at": datetime.now().isoformat(timespec="seconds")
        }
        data["documents"].append(item)
        return f"HOME: срок документа взят под контроль: {item['title']} | {due} | {item['id']}"

    def _add_inventory_item(self, data, text):
        item = {
            "id": self._next_id(data["inventory"], "INV"),
            "title": self._clean_title(text),
            "status": "needed",
            "created_at": datetime.now().isoformat(timespec="seconds")
        }
        data["inventory"].append(item)
        return f"HOME: добавлено в домашние запасы/покупки: {item['title']} | {item['id']}"

    def _register_program(self, data, text):
        alias, command = self._program_registration_parts(text)
        existing = next((p for p in data["programs"] if p.get("alias") == alias), None)
        record = {
            "alias": alias,
            "command": command,
            "created_at": datetime.now().isoformat(timespec="seconds")
        }
        if existing:
            existing.update(record)
        else:
            data["programs"].append(record)
        return f"HOME: программа зарегистрирована: {alias} -> {command}"

    def _program_registration_parts(self, text):
        match = re.search(r"(?:программу|приложение)\s+([A-Za-zА-Яа-я0-9_-]+)\s*[:=]\s*(.+)$", text, re.IGNORECASE)
        if not match:
            return None
        alias = match.group(1).strip().lower()
        command = match.group(2).strip().strip('"')
        if not alias or not command:
            return None
        return alias, command

    def _close_reminder(self, data, text):
        match = re.search(r"(?:закрой|заверши|выполнено)\s+(REM-\d+)", text, re.IGNORECASE)
        reminder_id = match.group(1).upper()
        item = next((x for x in data["reminders"] if x.get("id") == reminder_id), None)
        if not item:
            raise ValueError("HOME_REMINDER_NOT_FOUND")
        item["status"] = "closed"
        item["closed_at"] = datetime.now().isoformat(timespec="seconds")
        return f"HOME: напоминание закрыто: {reminder_id}"

    def _update_reminder(self, data, text):
        match = re.search(r"(?:обнови|измени)\s+(REM-\d+)\s*:\s*(.+)$", text, re.IGNORECASE)
        reminder_id = match.group(1).upper()
        update_text = match.group(2).strip()
        item = next((x for x in data["reminders"] if x.get("id") == reminder_id), None)
        if not item:
            raise ValueError("HOME_REMINDER_NOT_FOUND")
        if self._has_invalid_explicit_date(update_text):
            raise ValueError("HOME_INVALID_DATE")
        item["title"] = self._clean_title(update_text)
        due = self._extract_date(update_text)
        if due:
            item["due"] = due
        item["updated_at"] = datetime.now().isoformat(timespec="seconds")
        return f"HOME: напоминание обновлено: {reminder_id}"

    def _launch_program(self, data, text):
        q = text.lower()
        alias = q
        for prefix in ["запусти", "открой приложение", "запуск программы", "программу"]:
            alias = alias.replace(prefix, "")
        alias = alias.strip(" .,:;-\"'")

        if not alias:
            names = ", ".join(p.get("alias", "?") for p in data["programs"]) or "пока нет"
            return f"HOME: какую программу запустить? Зарегистрированы: {names}"

        program = next((p for p in data["programs"] if p.get("alias") == alias), None)
        if not program:
            return f"HOME: программа '{alias}' не зарегистрирована. Сначала: добавь программу {alias}: C:\\path\\app.exe"

        command = Path(program.get("command", ""))
        allowed = {".exe", ".bat", ".cmd", ".ps1", ".lnk"}
        if not command.exists() or command.suffix.lower() not in allowed:
            return f"HOME: запуск заблокирован, путь не найден или тип файла не разрешён: {command}"

        subprocess.Popen([str(command)], cwd=str(command.parent))
        return f"HOME: запускаю программу: {program['alias']}"

    def _due_items(self, items, days=14):
        today = date.today()
        horizon = today + timedelta(days=days)
        due = []
        for item in items:
            raw = item.get("due")
            if not raw:
                continue
            try:
                item_date = datetime.strptime(raw, "%Y-%m-%d").date()
            except ValueError:
                continue
            if item_date <= horizon and item.get("status") not in {"done", "closed"}:
                due.append((item_date, item))
        return [item for _, item in sorted(due, key=lambda x: x[0])]

    def _build_status(self, data):
        due = self._due_items(data["reminders"]) + self._due_items(data["documents"], days=30)
        inventory = [x for x in data["inventory"] if x.get("status") == "needed"]

        lines = ["HOME: домашняя сводка"]
        lines.append(f"- открытых напоминаний: {len([x for x in data['reminders'] if x.get('status') == 'open'])}")
        lines.append(f"- документов под контролем: {len(data['documents'])}")
        lines.append(f"- покупок/запасов: {len(inventory)}")
        lines.append(f"- программ в реестре: {len(data['programs'])}")

        if due:
            lines.append("")
            lines.append("Ближайшие сроки:")
            for item in due[:8]:
                lines.append(f"- {item.get('due')}: {item.get('title')} ({item.get('id')})")

        if inventory:
            lines.append("")
            lines.append("Нужно купить/пополнить:")
            for item in inventory[:8]:
                lines.append(f"- {item.get('title')} ({item.get('id')})")

        return "\n".join(lines)

