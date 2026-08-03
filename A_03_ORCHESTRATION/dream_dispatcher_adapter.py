# -*- coding: utf-8 -*-

from A_04_AGENTS.professor import DispatcherAgent


class DreamDispatcherAdapter:

    def __init__(self):
        self.dispatcher = DispatcherAgent()

    def execute_employee(
        self,
        employee="AUTO",
        system_prompt="",
        user_content=""
    ):
        return self.dispatcher.execute_employee(
            employee=employee,
            system_prompt=system_prompt,
            user_content=user_content
        )
