# -*- coding: utf-8 -*-

import subprocess
import sys
import shutil
from pathlib import Path
import os

ROOT=Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

from A_07_CONFIG.task_registry import TASKS
from A_02_MANAGERS.recipe_generator import RecipeGenerator
from A_02_MANAGERS.recipe_validator import RecipeValidator
from A_07_MEMORY.agent_planner import AgentPlannerV2


class TaskRunner:

    def __init__(self):

        self.root = Path.cwd()

        self.backup_dir = (
            self.root /
            "A_00_AVARIYKA" /
            "RunnerTransact"
        )

        self.backup_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.active_backups = {}

    def backup_file(self,file_rel_path):

        src=self.root / Path(file_rel_path)

        if not src.exists():

            print("[BACKUP ERROR]",file_rel_path)
            sys.exit(1)

        bak=self.backup_dir / Path(file_rel_path)

        bak.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.copy2(src,bak)

        self.active_backups[file_rel_path]=bak

        print("[BACKUP]",file_rel_path)

    def patch_file(self,file_rel_path,old_text,new_text):

        self.backup_file(file_rel_path)

        abs_path=self.root / Path(file_rel_path)

        content=abs_path.read_text(encoding="utf-8")

        if old_text not in content:

            print("[PATCH ERROR] Target text not found:",file_rel_path)

            self.rollback_all()

            sys.exit(1)

        updated=content.replace(old_text,new_text)

        abs_path.write_text(updated,encoding="utf-8")

        print("[PATCH]",file_rel_path)

    def rollback_all(self):

        if not self.active_backups:
            return

        print("="*70)
        print("ROLLBACK")
        print("="*70)

        for rel,bak in self.active_backups.items():

            shutil.copy2(
                bak,
                self.root / Path(rel)
            )

            print("[RESTORE]",rel)

    def execute_step(self,cmd):

        print("="*70)
        print("RUN:"," ".join(cmd))
        print("="*70)

        r=subprocess.run(cmd)

        if r.returncode!=0:

            self.rollback_all()

            sys.exit(r.returncode)

        print("[OK]")

    def run_strategic_step(self):
        """Связывает Мозг (Planner) и Руки (Runner) в единый цикл автоматизации"""
        planner = AgentPlannerV2()
        plan = planner.get_current_action_plan()

        # Проверяем, не завершены ли все задачи текущей фазы
        if plan.get("status") == "ALL_TASKS_COMPLETED" or plan.get("active_task") == "UNKNOWN":
            print("=" * 70)
            print("STRATEGIC PLAN STATUS: ALL ACTIVE TASKS COMPLETED")
            print("=" * 70)
            return

        active_task = plan["active_task"]
        print("=" * 70)
        print(f"STRATEGIC STEP DETECTED: {active_task.upper()}")
        print(f"Goal: {plan.get('active_goal')} | Phase: {plan.get('active_phase')}")
        print("=" * 70)

        if active_task not in TASKS:

            print("[STRATEGY ERROR] Recipe not found:", active_task)

            sys.exit(1)

        # Запускаем тактический рецепт. Если он упадет, сработает Fail-Fast + Rollback
        self.run_task(active_task)

        # Если мы дошли до этой строчки, значит run_task завершился успешно (SUCCESS)
        print(f"\n[STRATEGY] Committing success for task: {active_task}")
        if planner.complete_task(active_task):
            print("[STRATEGY] Strategic registry updated successfully. Phase advanced.")
        else:
            print("[STRATEGY ERROR] Failed to update goals_registry.json")
            sys.exit(1)

    def run_task(self,task):

        task=task.lower()

        if task not in TASKS:

            print("[ERROR]",task)

            sys.exit(1)

        print("="*70)
        print(task.upper())
        print("="*70)

        for step in TASKS[task]:

            if isinstance(step,dict):

                if step.get("action")=="patch":

                    self.patch_file(
                        file_rel_path=step["file"],
                        old_text=step["old"],
                        new_text=step["new"]
                    )

                else:

                    print("[ENGINE ERROR] Unknown action:",step)

                    self.rollback_all()

                    sys.exit(1)

            elif isinstance(step,list):

                self.execute_step(step)

            else:

                print("[ENGINE ERROR] Unknown step:",step)

                self.rollback_all()

                sys.exit(1)

        print("="*70)
        print("PIPELINE SUCCESS")
        print("="*70)


if __name__=="__main__":

    if len(sys.argv)<2:

        print("Usage: runner.py task")

        sys.exit(1)

    cmd = sys.argv[1].lower()
    runner = TaskRunner()
    if cmd == "step":
        runner.run_strategic_step()
    else:
        runner.run_task(cmd)
