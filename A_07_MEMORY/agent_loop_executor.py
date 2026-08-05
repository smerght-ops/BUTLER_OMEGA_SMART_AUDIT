# -*- coding: utf-8 -*-

from A_07_MEMORY.project_history import ProjectHistory
from A_07_MEMORY.change_request_manager import ChangeRequestManager


class AgentLoopExecutor:

    def __init__(self):
        self.history = ProjectHistory()
        self.cr = ChangeRequestManager()

    def get_last_state(self):
        records = self.history.get_closed_milestones()
        if not records:
            return None
        return records[-1]

    def decide_next_action(self, state):
        """
        VERY SIMPLE POLICY ENGINE (v1)
        """
        if not state:
            return "INIT_SYSTEM"

        stage = state.get("stage", "")

        if "4.14" in stage:
            return "BUILD_AGENT_LOOP_V2"
        if "CR_PHASE" in stage:
            return "RESOLVE_CHANGE_REQUESTS"

        return "MAINTAIN_STATE"

    def run_cycle(self):

        state = self.get_last_state()
        action = self.decide_next_action(state)

        result = self.cr.propose_change(action)

        return {
            "state": state,
            "action": action,
            "result": result
        }
