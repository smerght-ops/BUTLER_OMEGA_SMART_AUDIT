# -*- coding: utf-8 -*-
import time
import json
import sys
import os
import uuid
import hashlib
import shutil
import subprocess
import traceback
from urllib.parse import urlparse
from pathlib import Path

import requests

from A_04_AGENTS.base_department import BaseDepartment
from A_03_ORCHESTRATION.ConversationContext.ImageSession.image_session import ImageSession
from A_03_ORCHESTRATION.hybrid_resolver import HybridResolver


ROOT = Path(__file__).resolve().parents[2]
UTILS_DIR = ROOT / "A_00_UTILS"
if str(UTILS_DIR) not in sys.path:
    sys.path.insert(0, str(UTILS_DIR))

from document_writer import write_document


class ImageDepartment(BaseDepartment):
    NAME = "IMAGE"
    name = "IMAGE"
    VERSION = "1.0"
    CAPABILITIES = ("prompt_building", "comfyui_image_generation", "png_export")
    DEPENDENCIES = ("requests", "Ollama", "ComfyUI", "document_writer")
    DATA_READS = ("ComfyUI object_info", "ComfyUI output PNG", "ImageSession context")
    DATA_WRITES = (
        "A_06_WORKSPACE/exports/last_comfy_prompt.txt",
        "A_06_WORKSPACE/GENERATED_IMAGES/*.png",
    )

    def __init__(self):
        self.comfy_api = os.environ.get(
            "BUTLER_COMFYUI_BASE", "http://127.0.0.1:8188"
        ).rstrip("/")
        self.out_dir = ROOT / "A_06_WORKSPACE" / "GENERATED_IMAGES"
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.comfy_output = Path("D:/AI_Studio/ComfyUI_windows_portable/ComfyUI/output")

        # === МИКРО-ШАГ: ИНИЦИАЛИЗАЦИЯ ДАННЫХ ХУДОЖНИКОВ ===
        self.ollama_generate = "http://127.0.0.1:11434/api/generate"
        self.artists = {
            "1": ("Художник Хоррор", "DeepSeek-GPU:latest"),
            "2": ("Выдумщик", "gemma-4:latest"),
            "3": ("Художник Технарь", "ibm-granite_granite-4.1-30b-Q5_K_S:latest"),
        }
        self.last_artist_key = "1"
        self.wait_timeout = 300
        self.poll_interval = 2

    def can_handle(self, query: str, context: dict = None) -> bool:
        q = (query or "").lower()
        if "создай pdf" in q and ("из изображения" in q or "из изображений" in q):
            return False
        vision_analysis = any(k in q for k in (
            "что на картинке",
            "опиши изображение",
            "проанализируй изображение",
            "проанализируй фото",
            "что на фото",
            "что изображено",
            "анализ изображения",
            "ocr",
            "прочитай текст",
        ))
        if vision_analysis:
            return False
        hybrid_query = q.replace("кастрюлечеловек", "кастрюля-человек")
        explicit_creation = any(k in q for k in [
            "нарисуй",
            "сгенерируй изображение",
            "создай картинку",
            "создай изображение",
            "сделай картинку",
            "сделай фото",
            "image",
            "picture"
        ])
        return explicit_creation or HybridResolver().resolve(hybrid_query).get("is_hybrid", False)

    def _clean_prompt(self, query: str) -> str:
        q = query or ""
        for k in [
            "нарисуй мне",
            "нарисуй",
            "сгенерируй изображение",
            "создай картинку",
            "создай изображение",
            "сделай картинку",
            "сделай фото"
        ]:
            q = q.replace(k, "")
        return q.strip()

    def _list_first(self, obj, fallback):
        try:
            if isinstance(obj, list) and len(obj) > 0:
                if isinstance(obj[0], list) and len(obj[0]) > 0:
                    return obj[0][0]
                return obj[0]
        except Exception:
            pass
        return fallback

    def _get_object_info(self):
        r = requests.get(self.comfy_api + "/object_info", timeout=10)
        r.raise_for_status()
        return r.json()

    def _check_comfyui_ready(self):
        try:
            response = requests.get(self.comfy_api, timeout=3)
            response.raise_for_status()
            return response
        except requests.exceptions.ConnectionError as initial_error:
            parsed = urlparse(self.comfy_api)
            if parsed.hostname not in {"127.0.0.1", "localhost"}:
                raise

            comfy_root = self.comfy_output.parent.parent
            launcher = comfy_root / "run_nvidia_gpu.bat"
            if not launcher.is_file():
                raise

            creation_flags = (
                getattr(subprocess, "CREATE_NO_WINDOW", 0)
                | getattr(subprocess, "DETACHED_PROCESS", 0)
            )
            subprocess.Popen(
                ["cmd.exe", "/c", str(launcher)],
                cwd=str(comfy_root),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=creation_flags,
            )

            deadline = time.time() + 90
            last_error = initial_error
            while time.time() < deadline:
                time.sleep(2)
                try:
                    response = requests.get(self.comfy_api, timeout=3)
                    response.raise_for_status()
                    return response
                except requests.exceptions.ConnectionError as exc:
                    last_error = exc
            raise last_error

    def _comfy_connection_metadata(self, endpoint, exc, started):
        parsed = urlparse(endpoint)
        return {
            "endpoint": endpoint,
            "host": parsed.hostname,
            "port": parsed.port,
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
            "elapsed_ms": max(0, int((time.time() - started) * 1000)),
            "traceback": self._traceback_tail(),
        }

    def _image_size_for_prompt(self, prompt: str) -> tuple:
        q = (prompt or "").lower()
        portrait_markers = [
            "в полный рост",
            "полный рост",
            "full body",
            "full-body",
            "head to toe",
            "standing",
            "portrait orientation",
        ]
        wide_markers = [
            "панорама",
            "широкий кадр",
            "wide shot",
            "landscape",
            "seascape",
        ]

        if any(x in q for x in portrait_markers):
            return 768, 1152
        if any(x in q for x in wide_markers):
            return 1152, 768
        return 1024, 1024

    def _build_checkpoint_graph(self, prompt: str) -> dict:
        info = self._get_object_info()

        ckpt_req = info["CheckpointLoaderSimple"]["input"]["required"]["ckpt_name"]
        sampler_req = info["KSampler"]["input"]["required"]["sampler_name"]
        scheduler_req = info["KSampler"]["input"]["required"]["scheduler"]

        ckpt_name = "RealVisXL_V5.0.safetensors"
        sampler_name = self._list_first(sampler_req, "euler")
        scheduler = self._list_first(scheduler_req, "normal")
        width, height = self._image_size_for_prompt(prompt)

        return {
            "4": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {
                    "ckpt_name": ckpt_name
                }
            },
            "5": {
                "class_type": "EmptyLatentImage",
                "inputs": {
                    "width": width,
                    "height": height,
                    "batch_size": 1
                }
            },
            "6": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "text": prompt,
                    "clip": ["4", 1]
                }
            },
            "7": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "text": "bad quality, low quality, blurry, cropped body, cut off feet, cut off head, distorted, deformed, extra limbs, watermark, text",
                    "clip": ["4", 1]
                }
            },
            "3": {
                "class_type": "KSampler",
                "inputs": {
                    "seed": int(time.time() * 1000) % 2147483647,
                    "steps": 30,
                    "cfg": 7,
                    "sampler_name": sampler_name,
                    "scheduler": scheduler,
                    "denoise": 1,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0]
                }
            },
            "8": {
                "class_type": "VAEDecode",
                "inputs": {
                    "samples": ["3", 0],
                    "vae": ["4", 2]
                }
            },
            "9": {
                "class_type": "SaveImage",
                "inputs": {
                    "filename_prefix": "BUTLER_OMEGA_SMART",
                    "images": ["8", 0]
                }
            }
        }

    def _latest_image(self, before_time: float):
        if not self.comfy_output.exists():
            return None
        files = list(self.comfy_output.rglob("BUTLER_OMEGA_SMART*.png"))
        files = [p for p in files if p.stat().st_mtime > before_time]
        return max(files, key=lambda p: p.stat().st_mtime) if files else None

    def _ask_artist(self, model_name: str, prompt: str, timeout=120) -> str:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }
        res = requests.post(
            self.ollama_generate,
            json=payload,
            timeout=timeout
        )
        if res.status_code == 200:
            return res.json().get("response", "").strip()
        raise RuntimeError(
            f"Ollama error {res.status_code}: {res.text}"
        )

    def _build_artist_prompt(self, user_prompt: str) -> str:
        sys_text = (
            'Ты профессиональный prompt-engineer для Stable Diffusion / ComfyUI.\n'
            'Твоя задача — перевести запрос пользователя на английский язык, детализировать его, '
            'добавить стили, освещение, проработать детали фасадов или окружения.\n'
            'Если пользователь просит девушку/женщину, формулируй как adult woman. '
            'Если пользователь просит полный рост, обязательно добавь full body, head to toe, standing pose, full figure visible, feet visible. '
            'Если пользователь просит качество, добавь high quality, detailed, sharp focus, professional composition. '
            'Выдавай СТРОГО финальный промпт на английском языке. Никаких вводных слов и объяснений!'
        )
        return f'{sys_text}\n\nЗапрос: {user_prompt}'

    def _resolve_hybrid_prompt(self, user_prompt: str):
        normalized_prompt = user_prompt.lower().replace("кастрюлечеловек", "кастрюля-человек")
        resolved = HybridResolver().resolve(normalized_prompt)
        if not resolved.get("is_hybrid"):
            return user_prompt, None

        entity_1 = resolved["entity_1"]
        entity_2 = resolved["entity_2"]
        constraints = (
            f"HYBRID OBJECT. ENTITY 1: {entity_1}. ENTITY 2: {entity_2}. "
            f"Show unmistakable, clearly visible physical traits of BOTH {entity_1} and {entity_2} "
            "with equal visual importance in one integrated subject. "
            "Do not omit, replace, hide, or merely imply either entity."
        )
        return constraints, resolved

    def _inject_constraints(self, prompt: str, user_prompt: str):
        constraint_map = (
            (
                "девушк",
                ("adult woman",),
            ),
            (
                "не лицо",
                ("back view", "rear view", "turned away from camera", "face hidden", "face not visible", "no visible face"),
            ),
            (
                "в полный рост",
                ("full body", "head to toe", "feet visible", "standing pose", "full figure visible"),
            ),
            (
                "под водопадом",
                ("under waterfall", "cascading waterfall", "waterfall background"),
            ),
            (
                "на море",
                ("ocean", "sea", "beach", "coastline"),
            ),
        )

        source = (user_prompt or "").lower()
        injected = []
        for marker, constraints in constraint_map:
            if marker in source:
                injected.extend(constraints)

        if not injected:
            return prompt, []

        return f"{prompt.rstrip().rstrip('.')}. {', '.join(injected)}.", injected

    def _inject_hybrid_constraints(self, prompt: str, hybrid: dict):
        if not hybrid:
            return prompt, []

        feature_map = {
            "тигрокрыса": (
                "one full-body single rat-shaped tiger-rat hybrid creature, no separate animals",
                "(unmistakable rat anatomy, large round rat ears, rat muzzle, incisors and whiskers:1.7)",
                "(long hairless pink rat tail and rat paws fully visible:1.7)",
                "(the same rat body covered in bright orange-and-black tiger fur and tiger stripes:1.5)",
            ),
            "тигрокрысу": (
                "one full-body single rat-shaped tiger-rat hybrid creature, no separate animals",
                "(unmistakable rat anatomy, large round rat ears, rat muzzle, incisors and whiskers:1.7)",
                "(long hairless pink rat tail and rat paws fully visible:1.7)",
                "(the same rat body covered in bright orange-and-black tiger fur and tiger stripes:1.5)",
            ),
            "бетонолошадь": (
                "full body horse-shaped concrete sculpture isolated on a plain studio background",
                "(unmistakable horse head, mane, four legs and hooves:1.5)",
                "(the horse itself is entirely made from rough gray concrete:1.6)",
                "(concrete aggregate, cement pores and deep cracks visible across the horse body:1.5)",
            ),
            "кастрюля-человек": (
                "one single integrated human-pot hybrid subject, no extra people, no separate cookware",
                "(clearly visible human head, face, bare arms, hands, legs and feet:1.6)",
                "(huge unmistakable stainless-steel cooking pot forms the human torso:1.7)",
                "(open pot bowl, circular pot rim and two large side handles clearly visible:1.7)",
                "(separate cooking-pot lid held in one human hand:1.5)",
            ),
            "акула-человек": (
                "one single full-body anthropomorphic shark man standing upright on dry land in a plain studio, no extra person",
                "(two muscular human arms with elbows, five-fingered human hands:1.7)",
                "(human chest, waist, two long human legs and two human feet:1.7)",
                "(shark head, shark teeth, dorsal fin, gills, gray shark skin and shark tail:1.6)",
                "bipedal humanoid pose, not swimming, no underwater scene",
            ),
            "монетокамень": (
                "one single integrated coin-stone hybrid object",
                "(shiny gold metal coin with raised gold rim, embossed currency numerals and engraved coin face:1.7)",
                "(half of the same coin made from rough natural stone with cracks and mineral texture:1.7)",
            ),
        }

        source = {
            "акулачеловек": "акула-человек",
            "монетакамень": "монетокамень",
        }.get(hybrid.get("source"), hybrid.get("source"))
        features = feature_map.get(source, ())
        if not features:
            return prompt, []

        final_prompt = (
            f"{', '.join(features)}. "
            f"Both {hybrid['entity_1']} and {hybrid['entity_2']} traits must be unmistakable "
            "and equally prominent in the same integrated subject. "
            "Photorealistic, professional studio composition, sharp focus, highly detailed."
        )
        return final_prompt, list(features)

    def _select_artist(self, context: dict = None) -> tuple:
        context = dict(context or {})
        if context.get("image_followup") and self.last_artist_key in self.artists:
            return self.artists[self.last_artist_key]

        choice = str(context.get("artist_key", self.last_artist_key or "1")).strip()
        if choice in self.artists:
            self.last_artist_key = choice
            return self.artists[choice]
        self.last_artist_key = '1'
        return self.artists['1']

    def _success_text(self, target: Path, prompt: str) -> str:
        width, height = self._image_size_for_prompt(prompt)
        return (
            "Изображение готово.\n"
            f"Файл: {target}\n"
            f"Формат: {width}x{height}\n"
            "Промпт сохранён: A_06_WORKSPACE\\exports\\last_comfy_prompt.txt"
        )

    def execute(self, query: str, context: dict = None, **kwargs) -> dict:
        start = time.time()
        context = dict(context or {})
        last_pipeline_step = "prepare_prompt"
        diagnostic_prompt = None
        http_status = None
        http_response = None

        if context.get("image_followup"):
            clean_prompt = ImageSession.current() or self._clean_prompt(query)
        else:
            clean_prompt = self._clean_prompt(query)

        if not clean_prompt:
            return self._error_result(
                start, "EMPTY_PROMPT",
                "Не указан prompt для генерации изображения."
            )

        try:
            last_pipeline_step = "check_comfyui_readiness"
            readiness_started = time.time()
            try:
                self._check_comfyui_ready()
            except requests.exceptions.ConnectionError as exc:
                return self._error_result(
                    start, "COMFYUI_CONNECTION_ERROR",
                    "ComfyUI недоступен до построения workflow.",
                    model="ComfyUI",
                    metadata=self._comfy_connection_metadata(
                        self.comfy_api, exc, readiness_started
                    ),
                )
            except requests.exceptions.RequestException as exc:
                return self._error_result(
                    start, "COMFYUI_NOT_READY",
                    "ComfyUI не подтвердил готовность до построения workflow.",
                    model="ComfyUI",
                    metadata=self._comfy_connection_metadata(
                        self.comfy_api, exc, readiness_started
                    ),
                )

            last_pipeline_step = "select_artist"
            role_name, selected_model = self._select_artist(context=context)
            prepared_prompt, hybrid = self._resolve_hybrid_prompt(clean_prompt)
            artist_prompt = self._build_artist_prompt(prepared_prompt)
            last_pipeline_step = "artist_prompt_request"
            draft_prompt = self._ask_artist(selected_model, artist_prompt)
            if not draft_prompt:
                return self._error_result(
                    start, "EMPTY_DRAFT_PROMPT",
                    "Prompt-модель вернула пустой черновик.",
                    model=selected_model,
                )

            review_prompt = (
                "You are a senior Stable Diffusion prompt reviewer. "
                "Improve the following prompt without changing its meaning. "
                "Preserve every explicitly named hybrid entity and all mandatory constraints. "
                "Return ONLY the final prompt.\n\n"
                + draft_prompt
            )
            last_pipeline_step = "review_prompt_request"
            prompt = self._ask_artist("gemma-4:latest", review_prompt)
            diagnostic_prompt = prompt
            if not prompt:
                return self._error_result(
                    start, "EMPTY_REVIEWED_PROMPT",
                    "Prompt reviewer вернул пустой результат.",
                    model="gemma-4:latest",
                )

            if hybrid:
                prompt = (
                    f"{prompt}. MANDATORY HYBRID PRESERVATION: "
                    f"clearly visible {hybrid['entity_1']} traits AND clearly visible {hybrid['entity_2']} traits, "
                    "both equally prominent, neither entity omitted or substituted."
                )

            prompt, hybrid_constraints = self._inject_hybrid_constraints(prompt, hybrid)

            prompt, injected_constraints = self._inject_constraints(prompt, clean_prompt)

            model_name = f"{selected_model} -> gemma-4:latest"
            exports_dir = ROOT / "A_06_WORKSPACE" / "exports"
            exports_dir.mkdir(parents=True, exist_ok=True)
            try:
                last_pipeline_step = "save_prompt"
                write_document(exports_dir / "last_comfy_prompt.txt", prompt)
            except Exception as exc:
                return self._error_result(
                    start, "PROMPT_SAVE_ERROR",
                    "Не удалось сохранить итоговый prompt.",
                    model=model_name,
                    metadata={"exception_type": type(exc).__name__},
                )

            before_time = time.time()
            last_pipeline_step = "build_checkpoint_graph"
            api_prompt = self._build_checkpoint_graph(prompt)

            payload = {
                "prompt": api_prompt,
                "client_id": str(uuid.uuid4())
            }

            last_pipeline_step = "submit_comfy_prompt"
            r = requests.post(self.comfy_api + "/prompt", json=payload, timeout=30)
            http_status = r.status_code
            http_response = r.text

            if r.status_code >= 400:
                return self._error_result(
                    start, "IMAGE_ENGINE_ERROR",
                    "Ошибка отправки графа в ComfyUI.",
                    model="ComfyUI",
                    metadata={"status_code": r.status_code},
                )

            prompt_id = r.json().get("prompt_id", "")
            if not prompt_id:
                return self._error_result(
                    start, "EMPTY_IMAGE_ENGINE_RESPONSE",
                    "ComfyUI не вернул prompt_id.",
                    model="ComfyUI",
                )

            deadline = time.time() + self.wait_timeout
            final_img = None

            while time.time() < deadline:
                last_pipeline_step = "wait_for_comfy_output"
                time.sleep(self.poll_interval)
                final_img = self._latest_image(before_time)
                if final_img:
                    break

            if not final_img:
                return self._error_result(
                    start, "IMAGE_WAIT_TIMEOUT",
                    "Задача отправлена, но новый PNG не найден.",
                    model="ComfyUI",
                    metadata={"prompt_id": prompt_id},
                )

            target = self.out_dir / final_img.name
            try:
                self.out_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(final_img, target)
            except Exception as exc:
                return self._error_result(
                    start, "IMAGE_SAVE_ERROR",
                    "Не удалось сохранить сгенерированное изображение.",
                    model="ComfyUI",
                    metadata={"prompt_id": prompt_id, "exception_type": type(exc).__name__},
                )

            image_hash = hashlib.sha256(target.read_bytes()).hexdigest()
            presented = False
            presentation_error = None
            try:
                os.startfile(str(target))
                presented = True
            except Exception as exc:
                presentation_error = type(exc).__name__

            return {
                "ok": True,
                "department": self.NAME,
                "model": "ComfyUI",
                "artist": role_name,
                "artist_model": model_name,
                "sd_prompt": prompt,
                "latency_ms": int((time.time() - start) * 1000),
                "image_path": str(target),
                "text": self._success_text(target, prompt),
                "metadata": {
                    "prompt_id": prompt_id,
                    "prompt": prompt,
                    "hybrid": hybrid,
                    "hybrid_constraints": hybrid_constraints,
                    "injected_constraints": injected_constraints,
                    "image_path": str(target),
                    "image_size": target.stat().st_size,
                    "image_sha256": image_hash,
                    "presented": presented,
                    "presentation_method": "WindowsShell" if presented else None,
                    "presentation_error": presentation_error,
                    "prompt_writes": 1,
                    "comfy_tasks": 1,
                },
                "error": None
            }
        except Exception as exc:
            return self._error_result(
                start, "IMAGE_PIPELINE_ERROR",
                "Ошибка генерации изображения через Image pipeline.",
                model="ComfyUI",
                metadata={
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                    "traceback": self._traceback_tail(),
                    "prompt": diagnostic_prompt or clean_prompt,
                    "workflow": "checkpoint_graph",
                    "checkpoint": "RealVisXL_V5.0.safetensors",
                    "output_directory": str(self.out_dir),
                    "http_status": http_status,
                    "http_response": http_response,
                    "last_pipeline_step": last_pipeline_step,
                    "endpoint": self.comfy_api + "/object_info",
                    "host": urlparse(self.comfy_api).hostname,
                    "port": urlparse(self.comfy_api).port,
                    "elapsed_ms": max(0, int((time.time() - start) * 1000)),
                },
            )

    @staticmethod
    def _traceback_tail():
        return "\n".join(traceback.format_exc().strip().splitlines()[-10:])

    def _error_result(self, start, error, text, model=None, metadata=None):
        return {
            "ok": False,
            "department": self.NAME,
            "model": model,
            "latency_ms": max(0, int((time.time() - start) * 1000)),
            "text": text,
            "error": str(error),
            "metadata": dict(metadata or {}),
        }




