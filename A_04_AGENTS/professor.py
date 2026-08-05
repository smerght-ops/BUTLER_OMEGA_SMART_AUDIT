import re
import json
import requests
import base64
import shutil
from pathlib import Path

from A_02_MANAGERS.catalog_manager import CatalogManager
from A_03_HANDLERS.registry import registry
from A_03_HANDLERS.vision_engine import VisionEngine
from A_07_MEMORY.semantic_memory import SemanticMemory


class DispatcherAgent:
    def __init__(self):
        self.workspace_dir = Path("A_06_WORKSPACE/incoming")
        self.done_dir = Path("A_06_WORKSPACE/ARCHIVE_DONE")
        self.done_dir.mkdir(parents=True, exist_ok=True)

        self.memory_dir = Path("A_07_MEMORY")
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.memory_file = self.memory_dir / "MEMORY.txt"
        self.memory_index = self.memory_dir / "MEMORY_INDEX.jsonl"
        self.vision = VisionEngine()
        self.semantic_memory = SemanticMemory()

        self.ollama_url = "http://127.0.0.1:11434/api/generate"

        self.models = {
            "text": "qwen35-ru:latest",
            "vision": "qwen2.5-vl:latest",
        }

        self.catalog = CatalogManager()
        self.vision = VisionEngine()
        self.semantic_memory = SemanticMemory()

    def execute_employee(self, employee="AUTO", system_prompt="", user_content=""):
        """
        Совместимый интерфейс для dream_manager.py.
        Возвращает только текст ответа модели.
        """

        model = self.models.get("text", "qwen35-ru:latest")

        prompt = f"{system_prompt}\n\n{user_content}"

        response = requests.post(
            self.ollama_url,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=600
        )

        response.raise_for_status()

        data = response.json()

        result = data.get("response", "") or ""

        # Удаляем внутренние рассуждения модели
        result = re.sub(
            r"<think>.*?</think>",
            "",
            result,
            flags=re.DOTALL | re.IGNORECASE
        ).strip()

        return result

    def resolve_file_path(self, doc_id):
        file_path = Path(doc_id)

        if file_path.exists():
            return file_path

        candidate = self.workspace_dir / Path(doc_id).name
        if candidate.exists():
            return candidate

        return file_path

    def normalize_tags(self, raw_tags):
        if isinstance(raw_tags, list):
            return ",".join(
                str(item.get("name", item)) if isinstance(item, dict) else str(item)
                for item in raw_tags
            )

        if isinstance(raw_tags, dict):
            return str(raw_tags.get("name", raw_tags))

        return str(raw_tags or "")

    def parse_model_response(self, response_text):
        raw = (response_text or "").strip()

        if not raw:
            return {
                "summary": "Пустой ответ модели.",
                "tags": []
            }

        try:
            return json.loads(raw)
        except Exception:
            return {
                "summary": raw[:1000],
                "tags": ["raw_model_response"]
            }

    def build_prompt(self, file_path, extracted_text, handler_name, metadata):
        safe_text = extracted_text or ""

        if len(safe_text) > 6000:
            safe_text = safe_text[:6000] + "\n\n[TRUNCATED]"

        return (
            "Ты экспертный модуль BUTLER OMEGA.\n"
            "Проанализируй файл и верни строго JSON без лишнего текста.\n\n"
            "Формат ответа:\n"
            "{\n"
            '  "summary": "краткое содержание файла",\n'
            '  "tags": ["tag1", "tag2", "tag3"]\n'
            "}\n\n"
            f"Р В¤Р В°Р в„–Р В»: {file_path.name}\n"
            f"Обработчик: {handler_name}\n"
            f"Метаданные: {json.dumps(metadata, ensure_ascii=False)}\n\n"
            f"Контент:\n{safe_text}"
        )

    def get_model_payload(self, file_path, handler_name, extracted_text, metadata):
        is_image_handler = handler_name == "ImageHandler"

        if is_image_handler:
            prompt = (
                "Ты vision-модуль BUTLER OMEGA.\n"
                "Проанализируй изображение и верни строго JSON без лишнего текста.\n\n"
                "Формат ответа:\n"
                "{\n"
                '  "summary": "что изображено на картинке",\n'
                '  "tags": ["tag1", "tag2", "tag3"]\n'
                "}\n\n"
                f"Р В¤Р В°Р в„–Р В»: {file_path.name}\n"
                f"Метаданные изображения: {json.dumps(metadata, ensure_ascii=False)}"
            )

            return self.models["vision"], {
                "prompt": prompt
            }

        prompt = self.build_prompt(
            file_path=file_path,
            extracted_text=extracted_text,
            handler_name=handler_name,
            metadata=metadata
        )

        return self.models["text"], {
            "prompt": prompt
        }

    def append_memory(self, doc_id, file_path, handler_name, summary, tags):
        with open(self.memory_file, "a", encoding="utf-8") as f:
            f.write(
                f"FILE: {doc_id}\n"
                f"PATH: {file_path}\n"
                f"HANDLER: {handler_name}\n"
                f"SUMMARY: {summary}\n"
                f"TAGS: {tags}\n"
                f"{'-' * 30}\n"
            )

    def process_agent_task(self, doc_id, agent_type):
        file_path = self.resolve_file_path(doc_id)

        if not file_path.exists():
            print(f"[!] Р В¤Р В°Р в„–Р В» Р Р…Р Вµ Р Р…Р В°Р в„–Р Т‘Р ВµР Р…: {doc_id}")
            return False

        handler = registry.get_handler(file_path)

        if handler is None:
            print(f"[!] Нет обработчика для файла: {file_path}")
            return False

        handler_name = type(handler).__name__
        print(f"[PROFESSOR] Handler selected: {handler_name} -> {file_path.name}")

        extracted = handler.extract(file_path)

        if not extracted.get("success"):
            print(f"[!] Ошибка извлечения данных через {handler_name}: {extracted.get('metadata')}")
            return False

        extracted_text = extracted.get("text", "") or ""
        metadata = extracted.get("metadata", {}) or {}

        model_name, payload = self.get_model_payload(
            file_path=file_path,
            handler_name=handler_name,
            extracted_text=extracted_text,
            metadata=metadata
        )

        payload.update({
            "stream": False,
            "format": "json",
            "model": model_name
        })

        if handler_name == "ImageHandler":
            try:
                with open(file_path, "rb") as f:
                    payload["images"] = [base64.b64encode(f.read()).decode("utf-8")]
            except Exception as e:
                print(f"[!] Ошибка чтения изображения: {e}")
                return False

        try:
            resp = requests.post(
                self.ollama_url,
                json=payload,
                timeout=300
            )
        except Exception as e:
            print(f"[!] Ошибка подключения к Ollama: {e}")
            return False

        if resp.status_code != 200:
            print(f"[!] Ошибка модели {model_name}. HTTP {resp.status_code}")
            return False

        try:
            model_response = resp.json().get("response", "")
        except Exception as e:
            print(f"[!] Ошибка разбора ответа Ollama: {e}")
            return False

        res = self.parse_model_response(model_response)

        summary = res.get("summary", "Нет анализа.")
        tags = self.normalize_tags(res.get("tags", []))

        self.append_memory(
            doc_id=doc_id,
            file_path=file_path,
            handler_name=handler_name,
            summary=summary,
            tags=tags
        )

        # ВАЖНО:
        # file_hash передаём пустым, чтобы CatalogManager сохранил уже рассчитанный хэш Оркестратора.
        self.catalog.register_document(
            filepath=str(file_path),
            file_bytes=b"",
            summary=summary,
            tags=tags,
            file_hash="",
            status="completed"
        )

        try:
            target = self.done_dir / file_path.name
            if target.exists():
                target = self.done_dir / f"{file_path.stem}_done{file_path.suffix}"

            shutil.move(str(file_path), str(target))
            print(f"[PROFESSOR] Файл перемещён в архив: {target}")

        except Exception as e:
            print(f"[!] Ошибка перемещения файла в архив: {e}")
            return False

        try:
            self.semantic_memory.append(
                path=file_path,
                handler=handler_name,
                summary=summary,
                entities=[],
                tags=tags.split(",") if tags else [],
                engine="VisionEngine-v3-Hybrid",
                doc_type="document"
            )
        except Exception as e:
            print(f"[SemanticMemory] {e}")

        return True

    def _process_image_with_vision(self, file_path):
        """
        Централизованная обработка изображений через VisionEngine.
        """
        result = self.vision.analyze(file_path)

        metadata = result.get("metadata", {})

        return {
            "content": result.get("text", ""),
            "summary": metadata.get("summary", ""),
            "image_type": metadata.get("type", "other"),
            "entities": metadata.get("entities", []),
            "engine": metadata.get("engine", "VisionEngine"),
            "needs_review": metadata.get("needs_review", False)
        }
