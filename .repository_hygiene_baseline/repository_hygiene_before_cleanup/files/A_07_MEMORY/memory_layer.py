from A_03_ORCHESTRATION.context_builder import ButlerContextBuilder
from A_02_MANAGERS.session_manager import ButlerSessionManager

class MemoryLayer:

    def __init__(self):
        self.builder = ButlerContextBuilder()
        self.session = ButlerSessionManager()

    def build_prompt(self, user_text, task_id="TASK_0001", session_history=None):

        if session_history is None:
            session_history = self.session.get_recent(limit=12)

        ctx = self.builder.assemble_context(
            active_task_id=task_id,
            current_session_history=session_history
        )

        return (
            ctx["assembled_prompt"]
            + "\n\n=== ЗАПРОС ПОЛЬЗОВАТЕЛЯ ===\n"
            + user_text
        )