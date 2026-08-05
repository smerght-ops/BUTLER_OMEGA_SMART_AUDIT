# -*- coding: utf-8 -*-

from A_04_AGENTS.CodingDepartment.runner import CodingDepartment
from A_04_AGENTS.MemoryDepartment.runner import MemoryDepartment
from A_04_AGENTS.VisionDepartment.runner import VisionDepartment
from A_04_AGENTS.ImageDepartment.runner import ImageDepartment
from A_04_AGENTS.AudioDepartment.runner import AudioDepartment
from A_04_AGENTS.TextDepartment.runner import TextDepartment
from A_04_AGENTS.VideoDepartment.runner import VideoDepartment
from A_04_AGENTS.ArchiveDepartment.runner import ArchiveDepartment
from A_04_AGENTS.SearchDepartment.runner import SearchDepartment
from A_04_AGENTS.DocumentsDepartment.runner import DocumentsDepartment
from A_04_AGENTS.OpenDocumentDepartment.runner import OpenDocumentDepartment
from A_07_MEMORY.semantic_memory import SemanticMemory
from A_03_ORCHESTRATION.butler_harness import ButlerHarness


class SmartDispatcherV2:

    def __init__(self):
        self.semantic_memory = SemanticMemory()
        self.harness = ButlerHarness()

        self.departments = [
            SearchDepartment(),
            OpenDocumentDepartment(),
            CodingDepartment(),
            MemoryDepartment(),
            VisionDepartment(),
            ImageDepartment(),
            DocumentsDepartment(),
            AudioDepartment(),
            TextDepartment(),
            VideoDepartment(),
            ArchiveDepartment(),
        ]

    def _dept_name(self, dept):
        return str(
            getattr(
                dept,
                "NAME",
                type(dept).__name__
            )
        )

    def dispatch(self, query: str, context: dict = None) -> dict:
        context = context or {}
        q = (query or "").strip()

        for dept in self.departments:
            if dept.can_handle(q, context):
                logger.info(f"Dispatcher: Маршрут направлен в {self._dept_name(dept)}")
                return dept.execute(q, context)

        return {
            "ok": False,
            "text": "Команда не распознана ни одним департаментом.",
            "error": "UNKNOWN_INTENT"
        }
