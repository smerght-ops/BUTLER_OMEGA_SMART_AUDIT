# -*- coding: utf-8 -*-
from pathlib import Path

class ButlerDreamManager:
    def __init__(self, project_root=None):
        self.root = Path(project_root) if project_root else Path(__file__).resolve().parent.parent
        self.storage_dir = self.root / "A_05_STORAGE"
        self.tasks_dir = self.storage_dir / "tasks"
        self.checkpoint_file = self.storage_dir / "checkpoint.md"

    def consolidate_completed_task(self, dispatcher, task_id, employee="AUTO"):
        task_folder = self.tasks_dir / task_id
        progress_file = task_folder / "progress.md"
        summary_file = task_folder / "summary.md"

        if not progress_file.exists():
            print(f"DREAM_MANAGER: РџР РћРџРЈР©Р•РќРћ. progress.md РЅРµ РЅР°Р№РґРµРЅ РґР»СЏ {task_id}")
            return False

        raw_task_logs = progress_file.read_text(encoding="utf-8")

        system_distill = (
            "РўС‹ Р°РЅР°Р»РёС‚РёС‡РµСЃРєРёР№ РјРѕРґСѓР»СЊ dream_manager.py РІ СЃРёСЃС‚РµРјРµ BUTLER_OMEGA_SMART.\n"
            "РР·РІР»РµРєРё РёР· Р»РѕРіРѕРІ С‚РѕР»СЊРєРѕ С‚РµС…РЅРёС‡РµСЃРєСѓСЋ СЃСѓС‚СЊ:\n"
            "1. Р§РўРћ РЎР”Р•Р›РђРќРћ.\n"
            "2. РџР РРќРЇРўР«Р• Р Р•РЁР•РќРРЇ.\n"
            "3. РРЎРџР РђР’Р›Р•РќРќР«Р• РћРЁРР‘РљР.\n"
            "Р‘РµР· Р»РёС€РЅРёС… РІСЃС‚СѓРїР»РµРЅРёР№."
        )

        summary_content = dispatcher.execute_employee(
            employee=employee,
            system_prompt=system_distill,
            user_content=raw_task_logs
        )

        if not summary_content:
            print(f"DREAM_MANAGER: РћРЁРР‘РљРђ. РЎРѕС‚СЂСѓРґРЅРёРє РЅРµ РїРѕРґРіРѕС‚РѕРІРёР» summary РґР»СЏ {task_id}")
            return False

        task_folder.mkdir(parents=True, exist_ok=True)
        summary_file.write_text(f"# SUMMARY {task_id}\n\n{summary_content}", encoding="utf-8")

        self._update_global_checkpoint(dispatcher, task_id, summary_content, employee)
        print("DREAM_MANAGER: Р’Р«РџРћР›РќР•РќРћ")
        return True

    def _update_global_checkpoint(self, dispatcher, last_task_id, last_task_summary, employee):
        system_checkpoint = (
            "РўС‹ РјРѕРґСѓР»СЊ СЃРёРЅС…СЂРѕРЅРёР·Р°С†РёРё СЃРѕСЃС‚РѕСЏРЅРёСЏ РїСЂРѕРµРєС‚Р°.\n"
            "РЎС„РѕСЂРјРёСЂСѓР№ checkpoint.md СЃС‚СЂРѕРіРѕ РІ С„РѕСЂРјР°С‚Рµ:\n"
            "# РўР•РљРЈР©РР™ РЎРўРђРўРЈРЎ РЎРРЎРўР•РњР«\n"
            "- **РџРѕСЃР»РµРґРЅСЏСЏ Р·Р°РєСЂС‹С‚Р°СЏ Р·Р°РґР°С‡Р°**: ...\n"
            "- **Р§С‚Рѕ РёР·РјРµРЅРёР»РѕСЃСЊ РІ Р°СЂС…РёС‚РµРєС‚СѓСЂРµ**: ...\n"
            "- **Р‘Р»РёР¶Р°Р№С€РёР№ С€Р°Рі РґР»СЏ Р”РёСЃРїРµС‚С‡РµСЂР°**: ...\n"
            "Р’С‹РґР°Р№ С‚РѕР»СЊРєРѕ Markdown."
        )

        user_input = f"РџРѕСЃР»РµРґРЅСЏСЏ Р·Р°РґР°С‡Р°: {last_task_id}\nР’С‹Р¶РёРјРєР°:\n{last_task_summary}"

        new_checkpoint = dispatcher.execute_employee(
            employee=employee,
            system_prompt=system_checkpoint,
            user_content=user_input
        )

        if new_checkpoint:
            self.checkpoint_file.write_text(new_checkpoint, encoding="utf-8")
            print("checkpoint.md РѕР±РЅРѕРІР»РµРЅ")
        else:
            print("checkpoint.md РЅРµ РёР·РјРµРЅРµРЅ")

if __name__ == "__main__":
    class FakeDispatcher:
        def execute_employee(self, employee, system_prompt, user_content):
            return (
                "1. Р§РўРћ РЎР”Р•Р›РђРќРћ: С‚РµСЃС‚РѕРІР°СЏ РєРѕРЅСЃРѕР»РёРґР°С†РёСЏ РІС‹РїРѕР»РЅРµРЅР°.\n"
                "2. РџР РРќРЇРўР«Р• Р Р•РЁР•РќРРЇ: DreamManager СЂР°Р±РѕС‚Р°РµС‚ С‡РµСЂРµР· dispatcher.execute_employee.\n"
                "3. РРЎРџР РђР’Р›Р•РќРќР«Р• РћРЁРР‘РљР: РїСЂСЏРјРѕР№ РІС‹Р·РѕРІ РјРѕРґРµР»Рё РёСЃРєР»СЋС‡РµРЅ."
            )

    dm = ButlerDreamManager()
    test_task = dm.tasks_dir / "TASK-TEST"
    test_task.mkdir(parents=True, exist_ok=True)
    (test_task / "progress.md").write_text(
        "РўРµСЃС‚РѕРІР°СЏ Р·Р°РґР°С‡Р°: РїСЂРѕРІРµСЂРёС‚СЊ DreamManager Р±РµР· РїСЂСЏРјРѕР№ РїСЂРёРІСЏР·РєРё Рє РјРѕРґРµР»Рё.",
        encoding="utf-8"
    )
    dm.consolidate_completed_task(FakeDispatcher(), "TASK-TEST")
