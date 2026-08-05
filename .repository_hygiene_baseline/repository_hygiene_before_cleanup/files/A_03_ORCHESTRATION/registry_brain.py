import json
from pathlib import Path

class RegistryBrain:

    def __init__(self):
        self.registry_path = Path(__file__).resolve().parent / "department_registry.json"

        self.default_registry = {
            "TEXT": {
                "department": "Text_Department",
                "capabilities": ["chat", "summarization", "analysis"],
                "preferred_models": ["qwen35-ru:latest", "codestral:latest"]
            },
            "VISION": {
                "department": "Vision_Department",
                "capabilities": ["image_analysis", "ocr", "scene_understanding"],
                "preferred_models": ["qwen2.5-vl:latest", "llava:latest"]
            },
            "ART": {
                "department": "Art_Department",
                "capabilities": ["prompt_generation", "creative_design"],
                "preferred_models": ["DeepSeek-GPU:latest", "gemma-4:latest"]
            },
            "AUDIO": {
                "department": "Audio_Department",
                "capabilities": ["speech_to_text", "voice_tasks"],
                "preferred_models": []
            },
            "CODE": {
                "department": "Codestral_Engineer",
                "capabilities": ["code_generation", "refactoring"],
                "preferred_models": ["codestral:latest", "DeepSeek-Coder-V2-Lite-Instruct-Q6_K:latest"]
            }
        }

        self.registry = self.load()

    def load(self):
        if self.registry_path.exists():
            try:
                return json.loads(self.registry_path.read_text(encoding="utf-8"))
            except Exception:
                return self.default_registry
        return self.default_registry

    def save(self):
        self.registry_path.write_text(
            json.dumps(self.registry, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def route(self, semantic_decision: dict):

        task_type = semantic_decision.get("type", "TEXT")

        if task_type not in self.registry:
            task_type = "TEXT"

        department = self.registry[task_type]["department"]
        models = self.registry[task_type]["preferred_models"]

        return {
            "department": department,
            "models": models,
            "capabilities": self.registry[task_type]["capabilities"]
        }

    def update_department(self, key, data):
        self.registry[key] = data
        self.save()

    def list_departments(self):
        return list(self.registry.keys())


if __name__ == "__main__":
    rb = RegistryBrain()
    print(rb.route({"type": "VISION"}))
