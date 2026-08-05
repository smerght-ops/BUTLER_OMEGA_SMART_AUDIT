# -*- coding: utf-8 -*-

from A_04_AGENTS.professor import DispatcherAgent


class ProfessorAdapter:

    def __init__(self):
        self.professor = DispatcherAgent()

    def process_agent_task(
        self,
        filepath,
        target_agent="auto"
    ):
        return self.professor.process_agent_task(
            filepath,
            target_agent
        )
