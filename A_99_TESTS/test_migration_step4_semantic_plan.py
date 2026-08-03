# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from A_03_ORCHESTRATION.agent_core_coordinator import AgentCoreCoordinator
from A_03_ORCHESTRATION.ConversationContext.context_engine import (
    ConversationContextEngine,
)
from A_04_AGENTS.FilesystemDepartment.runner import FilesystemDepartment
from A_04_AGENTS.HomeDepartment.runner import HomeDepartment
from CapabilityRegistry import CapabilityRegistry


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_DONE = ROOT / "A_06_WORKSPACE" / "ARCHIVE_DONE"


class _Memory:
    def __init__(self):
        self.queries = []

    def build_memory_packet(self, query):
        self.queries.append(query)
        return {
            "budget_context": "ARCHIVE_DONE historically contained stale.txt",
            "provenance": [{"source": "test-memory"}],
            "used_tokens": 7,
        }


class Step4SemanticPlanTests(unittest.TestCase):
    def test_a_registry_exposes_existing_filesystem_read(self):
        record = next(
            item for item in CapabilityRegistry().all()
            if item["id"] == "filesystem_analyze_folder_folder"
        )
        self.assertEqual(record["department"], "FILESYSTEM")
        self.assertEqual(record["action"], "analyze_folder")
        self.assertEqual(record["confidence"], "confirmed")

    def test_b_c_live_archive_result_matches_disk(self):
        expected = sorted(
            path.relative_to(ARCHIVE_DONE).as_posix()
            for path in ARCHIVE_DONE.rglob("*")
        )
        self.assertTrue(ARCHIVE_DONE.is_dir())
        result = FilesystemDepartment().execute(
            "current directory state",
            context={"capability_action": "analyze_folder", "path": str(ARCHIVE_DONE)},
        )
        self.assertTrue(result["ok"], result)
        observed = sorted(
            item["relative_path"]
            for item in result["metadata"]["analysis_snapshot"]["entries"]
        )
        self.assertEqual(observed, expected)
        self.assertTrue(result["metadata"]["read_only"])

    def test_owner_query_is_a_generic_live_filesystem_read(self):
        query = "Батлер, что у тебя лежит в папке ARCHIVE_DONE?"
        filesystem = FilesystemDepartment()
        self.assertTrue(filesystem.can_handle(query))
        result = filesystem.execute(query)
        self.assertTrue(result["ok"], result)
        self.assertEqual(
            Path(result["metadata"]["path"]),
            ARCHIVE_DONE,
        )
        expected_names = sorted(
            path.name for path in ARCHIVE_DONE.iterdir()
        )
        self.assertTrue(expected_names)
        for name in expected_names:
            self.assertIn(name, result["text"])

    def test_two_turn_directory_referent_reaches_agent_and_fallback(self):
        ConversationContextEngine.last_department = None
        ConversationContextEngine.last_user_query = ""
        ConversationContextEngine.last_referent = None
        ConversationContextEngine.last_observation = None
        ConversationContextEngine.last_correlation_id = None

        turn_1 = "Батлер, что у тебя лежит в папке ARCHIVE_DONE?"
        turn_2 = (
            "Теперь изучи содержимое этого архива и расскажи мне "
            "человеческим языком, что там находится"
        )
        filesystem = FilesystemDepartment()
        first_result = filesystem.execute(turn_1)
        first_result["metadata"]["correlation_id"] = "turn-1"
        ConversationContextEngine.update(turn_1, first_result)

        second_context = ConversationContextEngine.enrich_context(
            turn_2,
            {"request_envelope": {"correlation_id": "turn-2"}},
        )
        self.assertEqual(second_context["path"], str(ARCHIVE_DONE))
        conversation = second_context["conversation_context"]
        self.assertEqual(conversation["previous_correlation_id"], "turn-1")
        self.assertEqual(conversation["referent"]["path"], str(ARCHIVE_DONE))
        self.assertEqual(
            conversation["previous_observation"]["department"],
            "FILESYSTEM",
        )
        self.assertTrue(conversation["previous_observation"]["entries"])

        captured_dispatch = []

        def dispatch(query, context):
            captured_dispatch.append(context)
            return filesystem.execute(query, context=context)

        core = AgentCoreCoordinator(dispatch)
        capability_id = "filesystem_analyze_folder_folder"
        replies = iter([
            {
                "role": "assistant", "content": "",
                "tool_calls": [{"function": {
                    "name": core.TOOL_NAME,
                    "arguments": {
                        "capability_id": capability_id,
                        "query": turn_2,
                    },
                }}],
            },
            {"role": "assistant", "content": "Сводка по текущему содержимому."},
        ])
        model_messages = []

        def chat(messages, tools):
            model_messages.append(json.loads(json.dumps(
                messages, ensure_ascii=False,
            )))
            return next(replies)

        core._chat = chat
        result = core.execute(turn_2, second_context)
        self.assertEqual(result["text"], "Сводка по текущему содержимому.")
        self.assertIn("ARCHIVE_DONE", model_messages[0][1]["content"])
        self.assertEqual(
            captured_dispatch[0]["resolved_referent"]["path"],
            str(ARCHIVE_DONE),
        )
        self.assertEqual(captured_dispatch[0]["path"], str(ARCHIVE_DONE))

        fallback_result = filesystem.execute(turn_2, context=second_context)
        self.assertTrue(fallback_result["ok"], fallback_result)
        self.assertEqual(
            Path(fallback_result["metadata"]["path"]),
            ARCHIVE_DONE,
        )

    def test_d_live_data_policy_and_provenance_reach_tool_boundary(self):
        memory = _Memory()
        calls = []

        def dispatch(query, context):
            calls.append((query, context))
            return {
                "ok": True, "department": "FILESYSTEM", "model": "test",
                "latency_ms": 0, "text": "live observation", "error": None,
                "metadata": {"analysis_snapshot": {"entries": []}},
            }

        core = AgentCoreCoordinator(dispatch, memory_orchestrator=memory)
        capability_id = "filesystem_analyze_folder_folder"
        replies = iter([
            {
                "role": "assistant", "content": "",
                "tool_calls": [{"function": {
                    "name": core.TOOL_NAME,
                    "arguments": {
                        "capability_id": capability_id,
                        "query": "read current state",
                        "context": {"path": str(ARCHIVE_DONE)},
                    },
                }}],
            },
            {"role": "assistant", "content": "Ответ основан на live observation."},
        ])
        captured = []

        def chat(messages, tools):
            captured.append(json.loads(json.dumps(messages, ensure_ascii=False)))
            return next(replies)

        core._chat = chat
        envelope = {"correlation_id": "corr-step4", "input_method": "keyboard"}
        result = core.execute(
            "Что сейчас находится в каталоге?",
            {"request_envelope": envelope},
        )
        self.assertEqual(memory.queries, ["Что сейчас находится в каталоге?"])
        self.assertEqual(result["text"], "Ответ основан на live observation.")
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][1]["request_envelope"], envelope)
        self.assertEqual(
            calls[0][1]["memory_packet"]["provenance"],
            [{"source": "test-memory"}],
        )
        system = captured[0][0]["content"]
        self.assertIn("memory as historical context", system)
        self.assertIn("filesystem read capability", system)
        self.assertIn("stale.txt", captured[0][1]["content"])
        self.assertIn("live observation", captured[1][-1]["content"])

    def test_e_nonexistent_path_is_reported_honestly(self):
        missing = ARCHIVE_DONE / "__step4_path_that_does_not_exist__"
        result = FilesystemDepartment().execute(
            "current directory state",
            context={"capability_action": "analyze_folder", "path": str(missing)},
        )
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"], "FILESYSTEM_FOLDER_NOT_FOUND")

    def test_f_home_ambiguous_query_does_not_create_reminder(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = HomeDepartment()
            home.root = Path(temporary)
            home.storage_path = home.root / "home.json"
            self.assertFalse(home.can_handle("Расскажи про домен приложения"))
            result = home.execute("Расскажи про домен приложения")
            self.assertFalse(result["ok"])
            self.assertEqual(result["error"], "HOME_INTENT_UNCONFIRMED")
            self.assertFalse(home.storage_path.exists())

    def test_g_explicit_reminder_still_works(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = HomeDepartment()
            home.root = Path(temporary)
            home.storage_path = home.root / "home.json"
            query = "Напомни мне завтра проверить отчёт"
            self.assertTrue(home.can_handle(query))
            result = home.execute(query)
            self.assertTrue(result["ok"], result)
            stored = json.loads(home.storage_path.read_text(encoding="utf-8"))
            self.assertEqual(len(stored["reminders"]), 1)
            self.assertIn("проверить отчёт", stored["reminders"][0]["title"])

    def test_h_three_dependent_observation_rounds(self):
        observations = []

        def dispatch(query, context):
            index = len(observations) + 1
            observations.append((query, context))
            return {
                "ok": True, "department": "FILESYSTEM", "model": "test",
                "latency_ms": 0, "text": f"observation-{index}", "error": None,
                "metadata": {"step": index},
            }

        core = AgentCoreCoordinator(dispatch)
        capability_id = "filesystem_analyze_folder_folder"
        replies = []
        for index in range(1, 4):
            replies.append({
                "role": "assistant", "content": "",
                "tool_calls": [{"function": {
                    "name": core.TOOL_NAME,
                    "arguments": {
                        "capability_id": capability_id,
                        "query": f"dependent-step-{index}",
                        "context": {"path": str(ARCHIVE_DONE)},
                    },
                }}],
            })
        replies.append({"role": "assistant", "content": "three steps complete"})
        replies = iter(replies)
        seen_messages = []

        def chat(messages, tools):
            seen_messages.append(json.loads(json.dumps(messages)))
            return next(replies)

        core._chat = chat
        result = core.execute("Выполни три зависимых шага")
        self.assertEqual(result["text"], "three steps complete")
        self.assertEqual(len(observations), 3)
        self.assertIn("observation-1", seen_messages[1][-1]["content"])
        self.assertIn("observation-2", seen_messages[2][-1]["content"])
        self.assertIn("observation-3", seen_messages[3][-1]["content"])

    def test_i_j_k_l_steps_1_to_3_and_voice_contracts_remain(self):
        os_source = (ROOT / "BUTLER_OS.py").read_text(encoding="utf-8-sig")
        voice_source = (
            ROOT / "A_09_INTERFACE" / "voice_input.py"
        ).read_text(encoding="utf-8-sig")
        semantic_source = (
            ROOT / "A_07_MEMORY" / "semantic_memory.py"
        ).read_text(encoding="utf-8-sig")
        search_source = (
            ROOT / "A_07_MEMORY" / "search_engine.py"
        ).read_text(encoding="utf-8-sig")
        orchestrator_source = (
            ROOT / "A_07_MEMORY" / "memory_orchestrator_v2.py"
        ).read_text(encoding="utf-8-sig")
        self.assertIn("def _create_request_envelope", os_source)
        self.assertIn('"correlation_id": str(uuid.uuid4())', os_source)
        self.assertIn("request_envelope_factory=_create_request_envelope", os_source)
        self.assertIn("MemoryOrchestratorV2(token_budget=1200)", os_source)
        self.assertIn("memory_orchestrator=_memory_orchestrator", os_source)
        self.assertIn('"value": value', semantic_source)
        self.assertIn('rec.get("text") or rec.get("value", "")', search_source)
        self.assertIn('record.get("knowledge_id")', orchestrator_source)
        self.assertIn(".get('value')", orchestrator_source)
        self.assertIn("request_envelope_factory", voice_source)
        self.assertIn('input_method="voice"', voice_source)
        self.assertIn("except AgentCoreUnavailable as exc:", os_source)
        self.assertIn('"agent_core_fallback": True', os_source)
        self.assertIn('"agent_core_error": str(exc)', os_source)


if __name__ == "__main__":
    unittest.main()
