# -*- coding: utf-8 -*-

from A_07_MEMORY import profile_manager
from A_07_CONFIG.project_passport_loader import ProjectPassportLoader
from A_07_CONFIG.project_memory_loader import ProjectMemoryLoader


class ButlerOSAdapter:

    def __init__(self):
        self.passport = ProjectPassportLoader()
        self.memory_loader = ProjectMemoryLoader()

    def memory_summary(self):
        return profile_manager.get_memory_summary()

    def skills_summary(self):
        return profile_manager.get_skills_summary()

    def episodes_summary(self):
        return profile_manager.get_episodes_summary()

    def passport_summary(self):
        return self.passport.load_passport()

    def project_identity(self):
        return self.passport.get_identity()

    def frozen_modules(self):
        return self.passport.get_frozen_modules()

    def current_stage(self):
        return self.passport.get_current_stage()

    def passport_summary_text(self):

        p = self.passport_summary()

        frozen = p["architecture_freeze"]["frozen_modules"]
        active = p["architecture_freeze"]["active_modules"]

        frozen_text = "\n".join(
            [f"- {x}" for x in frozen]
        )

        active_text = "\n".join(
            [f"- {x}" for x in active]
        )

        return f"""
===== BUTLER PASSPORT =====

NAME:
{p["project_identity"]["name"]}

VERSION:
{p["project_identity"]["version"]}

CURRENT STAGE:
{p["project_identity"]["current_stage"]}

FROZEN MODULES:
{frozen_text}

ACTIVE MODULES:
{active_text}

CURRENT TASK:
{p["roadmap_pointer"]["current_task"]}

NEXT TASK:
{p["roadmap_pointer"]["next_task"]}
""".strip()

    def built_features(self):
        return self.memory_loader.get_built_features()

    def current_work(self):
        return self.memory_loader.get_current_work()

    def next_work(self):
        return self.memory_loader.get_next_work()

    def project_memory_summary_text(self):
        built = self.built_features()
        current = self.current_work()
        next_w = self.next_work()
        built_text = "\n".join([f"- {x}" for x in built])
        current_text = "\n".join([f"- {x}" for x in current])
        next_text = "\n".join([f"- {x}" for x in next_w])
        return f"""===== PROJECT OMEGA SMART MEMORY =====\n\nBUILT FEATURES:\n{built_text}\n\nCURRENT WORK:\n{current_text}\n\nNEXT WORK:\n{next_text}""".strip()

    def full_summary(self):
        return {
            "memory": self.memory_summary(),
            "skills": self.skills_summary(),
            "episodes": self.episodes_summary(),
            "passport": self.passport_summary()
        }

