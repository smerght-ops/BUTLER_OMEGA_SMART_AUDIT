from A_07_MEMORY.profile_manager import load_profile
from pathlib import Path
import json

class MemoryCore:

    def __init__(self):
        self.profile = load_profile()

    def get_user_name(self):
        return self.profile.get("user_name", {}).get("name", {}).get("value")

    def get_preferences(self):
        return self.profile.get("preferences", {})

    def build_memory_packet(self, session_history=None, task_id=None):

        packet = {
            "user": self.get_user_name(),
            "preferences": self.get_preferences(),
            "session": session_history or "",
            "task_id": task_id or None
        }

        return packet

    def inject_into_prompt(self, base_prompt: str, session_history=None, task_id=None):

        mem = self.build_memory_packet(session_history, task_id)

        memory_block = f"""
=== MEMORY CORE ===
USER: {mem['user']}
TASK: {mem['task_id']}
SESSION: {mem['session']}
PREFERENCES: {json.dumps(mem['preferences'], ensure_ascii=False)}
===================
"""

        return memory_block + "\n\n" + base_prompt


if __name__ == "__main__":
    mc = MemoryCore()
    print(mc.inject_into_prompt("TEST PROMPT"))
