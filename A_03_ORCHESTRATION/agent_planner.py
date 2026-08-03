from pathlib import Path
import json

class AgentPlanner:
    def __init__(self, plan_dir="A_00_AVARIYKA/LAB_PLANS"):
        self.plan_dir = Path(plan_dir)
        self.plan_dir.mkdir(parents=True, exist_ok=True)

    def create_plan(self, plan_id, description):
        return {"plan_id": plan_id, "description": description, "steps": [], "status": "pending"}

    def save_checkpoint(self, plan_id, plan_data):
        f = self.plan_dir / f"{plan_id}.json"
        with open(f, "w", encoding="utf-8") as fp:
            json.dump(plan_data, fp)

    def load_unfinished_plan(self, plan_id):
        f = self.plan_dir / f"{plan_id}.json"
        if not f.exists():
            return None
        with open(f, "r", encoding="utf-8") as fp:
            return json.load(fp)