# -*- coding: utf-8 -*-
import sys
import types
import tempfile
from pathlib import Path

# The routing tests are offline and never call HTTP. Keep them runnable in the
# project's minimal verification interpreter where requests may be absent.
sys.modules.setdefault("requests", types.ModuleType("requests"))

from A_02_MANAGERS.smart_dispatcher import SmartDispatcher
from A_04_AGENTS.AudioDepartment.runner import AudioDepartment
from A_04_AGENTS.VideoDepartment.runner import VideoDepartment
from A_04_AGENTS.MemoryDepartment.runner import MemoryDepartment
from A_04_AGENTS.ImageDepartment.runner import ImageDepartment
from A_04_AGENTS.HomeDepartment.runner import HomeDepartment
from A_04_AGENTS.DocumentsDepartment.runner import DocumentsDepartment
from A_04_AGENTS.TextDepartment.runner import TextDepartment
from A_04_AGENTS.CodingDepartment.runner import CodingDepartment
from A_04_AGENTS.ArchiveDepartment.runner import ArchiveDepartment
from A_00_UTILS.llm_output_sanitizer import sanitize_llm_output
from A_03_ORCHESTRATION.ConversationContext.context_engine import ConversationContextEngine


def test_chat_reasoning_is_removed():
    raw = "<think>секретный план</think>\nГотовый ответ"
    assert SmartDispatcher.clean_model_output(raw) == "Готовый ответ"
    raw = "Thinking Process:\n1. internal\n\nПользовательский ответ"
    assert SmartDispatcher.clean_model_output(raw) == "Пользовательский ответ"
    raw = "Thinking Process:\nAnalyze the Request: secret\nConfidence Score: 99%\n\nИтог"
    assert sanitize_llm_output(raw) == "Итог"
    assert sanitize_llm_output("ответ\nConfidence Score: 80%") == "ответ"


def test_chat_continue_uses_previous_user_scenario():
    ConversationContextEngine.last_department = "CHAT"
    ConversationContextEngine.last_user_query = "Составь план поездки"
    resolved = ConversationContextEngine.resolve("Продолжай")
    assert "Составь план поездки" in resolved
    assert "Продолжай" in resolved


def test_attested_routing_markers():
    assert AudioDepartment().can_handle('озвучь текст "Привет"')
    assert AudioDepartment().can_handle("скажи голосом привет")
    assert VideoDepartment().can_handle("проанализируй видео movie.mp4")
    assert MemoryDepartment().can_handle("что ты помнишь обо мне")
    assert MemoryDepartment().can_handle("найди в памяти паспорт")
    assert MemoryDepartment().can_handle("какой мой любимый цвет")
    assert ImageDepartment().can_handle("нарисуй девушку под водопадом")
    assert ImageDepartment().can_handle("create image of a waterfall")
    assert ImageDepartment().can_handle("make a picture of a waterfall")


def test_dispatcher_priority_is_image_video_audio_then_home():
    source = Path("A_02_MANAGERS/smart_dispatcher_v2.py").read_text(encoding="utf-8")
    start = source.index("self.departments = [")
    end = source.index("]", start)
    order = source[start:end]
    assert order.index("ImageDepartment()") < order.index("VideoDepartment()")
    assert order.index("VideoDepartment()") < order.index("AudioDepartment()")
    assert order.index("SearchDepartment()") < order.index("MemoryDepartment()")
    assert order.index("AudioDepartment()") < order.index("HomeDepartment()")


def test_broad_departments_do_not_capture_media():
    assert not HomeDepartment().can_handle("нарисуй девушку")
    assert not DocumentsDepartment().can_handle("проанализируй видео movie.mp4")
    assert not DocumentsDepartment().can_handle(
        "проанализируй файл", context={"attachments": ["movie.mp4"]}
    )


def test_text_handles_transformations():
    department = TextDepartment.__new__(TextDepartment)
    assert department.can_handle("переведи этот текст")
    assert department.can_handle("перефразируй предложение")


def test_text_prompt_contains_only_user_task_not_project_memory():
    department = TextDepartment.__new__(TextDepartment)
    department.model = "text-test"
    department.generate_url = "http://local/api/generate"
    department.available_models = lambda: ["text-test"]
    captured = {}

    class Response:
        def raise_for_status(self): pass
        def json(self): return {"response": "Hello"}

    old_post = sys.modules["requests"].__dict__.get("post")
    sys.modules["requests"].post = lambda *args, **kwargs: (captured.update(kwargs["json"]), Response())[1]
    try:
        result = department.execute("Переведи текст: Привет")
    finally:
        if old_post is None:
            del sys.modules["requests"].post
        else:
            sys.modules["requests"].post = old_post
    assert result["ok"]
    prompt = captured["prompt"]
    assert "Переведи текст: Привет" in prompt
    assert "ПАСПОРТ ПРОЕКТА" not in prompt
    assert "project_context" not in prompt


def test_video_never_echoes_query_as_success():
    query = "что находится в видео"
    result = VideoDepartment().execute(query)
    assert result["department"] == "VIDEO"
    assert not result["ok"]
    assert result["text"] != query
    assert result["error"] == "VIDEO_NOT_FOUND"


def test_coding_rejects_irrelevant_answer_and_falls_back():
    department = CodingDepartment.__new__(CodingDepartment)
    department.model_chain = ["bad-model", "good-model"]
    answers = {
        "bad-model": "Числа Фибоначчи: 1, 1, 2, 3, 5, 8",
        "good-model": "Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 10 Name, Id, WorkingSet",
    }
    department._ask = lambda model, prompt: answers[model]
    result = department.execute("Покажи 10 процессов по памяти в PowerShell")
    assert result["ok"]
    assert result["model"] == "good-model"
    assert result["fallback_used"]


def test_coding_returns_managed_error_when_all_answers_are_irrelevant():
    department = CodingDepartment.__new__(CodingDepartment)
    department.model_chain = ["one", "two"]
    department._ask = lambda model, prompt: "SOLID и случайные пароли"
    result = department.execute("Покажи 10 процессов по памяти в PowerShell")
    assert not result["ok"]
    assert result["error"] == "CODING_GENERATION_FAILED"
    assert len(result["metadata"]["rejected_models"]) == 2


def test_audio_returns_result_or_required_diagnostic_error():
    unavailable = AudioDepartment().execute('озвучь текст "Привет"')
    assert unavailable["error"] == "AUDIO_ENGINE_NOT_AVAILABLE"
    success = AudioDepartment().execute(
        'озвучь текст "Привет"',
        context={"audio_engine": lambda **kwargs: "C:/output/hello.wav"},
    )
    assert success["ok"] and success["error"] is None
    missing = AudioDepartment().execute("распознай речь", context={"attachments": ["missing.wav"]})
    assert missing["error"] == "AUDIO_NOT_FOUND"


def test_video_full_model_cycle_and_required_errors():
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "sample.mp4"
        path.write_bytes(b"video")
        department = VideoDepartment.__new__(VideoDepartment)
        department.model = "vision-test"
        department.generate_url = "http://local/api/generate"
        department._sample_frames = lambda source: ["frame-1", "frame-2"]

        class Response:
            def raise_for_status(self): pass
            def json(self): return {"response": "На видео человек идёт по улице."}

        old_post = sys.modules["requests"].__dict__.get("post")
        sys.modules["requests"].post = lambda *args, **kwargs: Response()
        try:
            result = department.execute("Что находится в видео?", context={"attachments": [str(path)]})
        finally:
            if old_post is None:
                del sys.modules["requests"].post
            else:
                sys.modules["requests"].post = old_post
        assert result["ok"]
        assert result["text"] == "На видео человек идёт по улице."
        assert result["metadata"]["sampled_frames"] == 2


def test_archive_create_extract_and_format_guards():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        source = root / "source"
        source.mkdir()
        (source / "hello.txt").write_text("hello", encoding="utf-8")
        archive = root / "bundle.zip"
        department = ArchiveDepartment()
        created = department.execute(
            "заархивируй", context={"attachments": [str(source)], "output_path": str(archive)}
        )
        assert created["ok"] and archive.exists()
        output = root / "unpacked"
        extracted = department.execute(
            "распакуй архив", context={"attachments": [str(archive)], "output_path": str(output)}
        )
        assert extracted["ok"]
        assert list(output.rglob("hello.txt"))
        unsupported = root / "bad.txt"
        unsupported.write_text("x", encoding="utf-8")
        result = department.execute("распакуй архив", context={"attachments": [str(unsupported)]})
        assert result["error"] == "UNSUPPORTED_ARCHIVE_FORMAT"
        assert department.can_handle("распакуй архив backup.7z")
        assert department.can_handle("создай архив backup.rar")
