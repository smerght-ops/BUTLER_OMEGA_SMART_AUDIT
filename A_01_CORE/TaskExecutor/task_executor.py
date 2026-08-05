from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from tools.inspectors.CapabilityRegistry import CapabilityRegistry

from .task_decomposer import TaskDecomposer, TaskIntent
from .task_plan import TaskPlan
from .task_step import TaskStep
from A_07_MEMORY.semantic_memory import SemanticMemory
from A_01_CORE.skill_runtime import SkillManager


class TaskExecutor:
    """Planning facade. It never invokes departments or performs task actions."""

    def __init__(self, registry_path=None):
        default_path = Path(__file__).resolve().parents[2] / "CapabilityRegistry.json"
        self.registry = CapabilityRegistry(registry_path or default_path)
        self.decomposer = TaskDecomposer()
        self.skill_memory = SemanticMemory()
        self.skill_manager = SkillManager(memory=self.skill_memory)

    def plan(self, request: str) -> dict:
        goal = str(request or "").strip()
        project = self.decomposer.project_spec(goal)
        if project is not None:
            return self._with_learned_skill(self._project_plan(goal, project))
        intents = list(self.decomposer.decompose(goal))
        # Reorder: generate_text must come before create_docx
        has_generate_text = any(i.requested_action == "generate_text" for i in intents)
        has_create_docx = any(i.requested_action == "create_docx" for i in intents)
        if has_generate_text and has_create_docx:
            generate_idx = next((i for i, intent in enumerate(intents) if intent.requested_action == "generate_text"), None)
            create_idx = next((i for i, intent in enumerate(intents) if intent.requested_action == "create_docx"), None)
            if generate_idx is not None and create_idx is not None and generate_idx > create_idx:
                # Move generate_text before create_docx
                intents[generate_idx], intents[create_idx] = intents[create_idx], intents[generate_idx]
                # Update depends_on_previous flags after swap (TaskIntent is frozen)
                intents = [
                    replace(intent, depends_on_previous=False) if i == 0
                    else replace(intent, depends_on_previous=True) if intent.requested_action == "create_docx"
                    else intent
                    for i, intent in enumerate(intents)
                ]
        capabilities = self.registry.all()
        steps: list[TaskStep] = []
        latest_outputs: dict[str, int] = {}

        for intent in intents:
            order = len(steps) + 1
            dependency = (order - 1,) if intent.depends_on_previous and order > 1 else ()
            record = self._resolve(intent, capabilities)
            if intent.missing_action and record is None:
                steps.append(TaskStep(
                    order=order,
                    department="FILESYSTEM",
                    action=intent.missing_action,
                    object=intent.object_candidates[0] if intent.object_candidates else "unknown",
                    status="missing_capability",
                    requested_action=intent.requested_action,
                    source_text=intent.source_text,
                    depends_on=dependency,
                    arguments=dict(intent.arguments),
                ))
                continue

            if record is None:
                steps.append(TaskStep(
                    order=order,
                    department="UNKNOWN",
                    action=intent.requested_action,
                    object=intent.object_candidates[0] if intent.object_candidates else "unknown",
                    status="missing_capability",
                    requested_action=intent.requested_action,
                    source_text=intent.source_text,
                    depends_on=dependency,
                    arguments=dict(intent.arguments),
                ))
                continue

            arguments = dict(intent.arguments)
            arguments.setdefault("query", intent.source_text)
            if intent.depends_on_previous and order > 1:
                arguments.setdefault("previous_result", f"{{{{step_{order - 1}.output}}}}")
                if record["action"].startswith(("extract_", "analyze_", "recognize_")):
                    arguments.setdefault("attachments", [f"{{{{step_{order - 1}.output}}}}"])
            if record["action"] == "save_text":
                if "folder" in latest_outputs:
                    arguments["folder"] = f"{{{{step_{latest_outputs['folder']}.output}}}}"
                if "text" in latest_outputs:
                    arguments["content"] = f"{{{{step_{latest_outputs['text']}.output}}}}"
            elif record["action"] == "save_image":
                if "folder" in latest_outputs:
                    arguments["folder"] = f"{{{{step_{latest_outputs['folder']}.output}}}}"
                if "image" in latest_outputs:
                    arguments["source"] = f"{{{{step_{latest_outputs['image']}.output}}}}"

            steps.append(TaskStep(
                order=order,
                department=record["department"],
                action=record["action"],
                object=record["object"],
                status="planned",
                capability_id=record["id"],
                requested_action=intent.requested_action,
                source_text=intent.source_text,
                depends_on=dependency,
                arguments=arguments,
            ))
            if record["action"] == "create_folder":
                latest_outputs["folder"] = order
            elif record["output"] == "image":
                latest_outputs["image"] = order
            elif record["output"] in {"text", "code"}:
                latest_outputs["text"] = order

        return self._with_learned_skill(TaskPlan(goal=goal, steps=steps).to_dict())

    def _with_learned_skill(self, plan):
        signature = [step.get("capability_id") or step.get("action") for step in plan.get("steps", [])]
        skill = self.skill_manager.match_active(signature)
        plan["procedural_memory"] = {
            "signature": signature,
            "reused": bool(skill),
            "skill_id": skill.get("skill_id") if skill else None,
            "source": skill.get("source") if skill else None,
        }
        return plan

    def _project_plan(self, goal, project) -> dict:
        capabilities = {record["action"]: record for record in self.registry.all()}
        steps: list[TaskStep] = []

        def add(action, source_text, arguments, output_name, artifact_type):
            order = len(steps) + 1
            record = capabilities.get(action)
            steps.append(TaskStep(
                order=order,
                department=record["department"] if record else "UNKNOWN",
                action=action,
                object=record["object"] if record else artifact_type,
                status="planned" if record else "missing_capability",
                capability_id=record["id"] if record else None,
                requested_action=action,
                source_text=source_text,
                depends_on=(order - 1,) if order > 1 else (),
                arguments=arguments,
                output_artifact=output_name,
                artifact_type=artifact_type,
            ))
            return order

        folder_step = add(
            "create_folder", "Создай корневую папку проекта.",
            {"folder_name": project.project_name, "location": project.location},
            "project_folder", "directory_path",
        )
        poem_steps = []
        image_steps = []
        for index in range(1, project.count + 1):
            poem = add(
                "generate_text", f"Напиши стихотворение {index} о море.",
                {"query": f"Напиши самостоятельное стихотворение №{index} о море."},
                f"poem_text_{index}", "text",
            )
            poem_steps.append(poem)
            add(
                "save_text", f"Сохрани стихотворение {index}.",
                {"folder": f"{{{{step_{folder_step}.output}}}}", "content": f"{{{{step_{poem}.output}}}}", "filename": f"poem_{index}.txt"},
                f"poem_file_{index}", "file_path",
            )
            image = add(
                "generate_comfyui_image", f"Создай иллюстрацию {index} к стихотворению.",
                {"query": f"Морская книжная иллюстрация №{index}, вдохновлённая стихотворением: {{{{step_{poem}.output}}}}"},
                f"image_source_{index}", "image",
            )
            image_steps.append(image)
            add(
                "save_image", f"Сохрани иллюстрацию {index}.",
                {"folder": f"{{{{step_{folder_step}.output}}}}", "source": f"{{{{step_{image}.output}}}}", "filename": f"image_{index}.png"},
                f"image_file_{index}", "file_path",
            )

        contents = "\n\n".join(f"Стихотворение {i}:\n{{{{step_{step}.output}}}}" for i, step in enumerate(poem_steps, 1))
        contents_step = add(
            "save_text", "Создай общий файл содержания проекта.",
            {"folder": f"{{{{step_{folder_step}.output}}}}", "content": contents, "filename": "CONTENTS.txt"},
            "contents_file", "summary",
        )
        archive_step = add(
            "create_archive", "Упакуй папку проекта в ZIP-архив.",
            {"attachments": [f"{{{{step_{folder_step}.output}}}}"], "output_path": f"{{{{step_{folder_step}.output}}}}.zip"},
            "final_zip", "archive_path",
        )
        add(
            "write_profile_fact", "Запомни путь к архиву проекта.",
            {"query": f"Запомни project_archive = {{{{step_{archive_step}.output}}}}"},
            "memory_record", "memory_record",
        )
        plan = TaskPlan(goal=goal, steps=steps).to_dict()
        plan["variables"] = {
            "project_name": project.project_name,
            "count": project.count,
            "count_source": project.count_source,
            "location": project.location,
        }
        plan["outputs"] = {"final_zip_step": archive_step, "contents_step": contents_step}
        return plan

    @staticmethod
    def _resolve(intent: TaskIntent, capabilities: list[dict]) -> dict | None:
        best = None
        best_score = 0
        for record in capabilities:
            action = str(record.get("action", ""))
            verb = action.split("_", 1)[0]
            object_name = str(record.get("object", ""))
            score = 0

            if action == intent.missing_action:
                score += 200
            if object_name in intent.object_candidates:
                score += 100 - intent.object_candidates.index(object_name)
            if verb in intent.action_families:
                score += 50 - intent.action_families.index(verb)
            if not any((object_name in intent.object_candidates, verb in intent.action_families)):
                continue
            if object_name == "unknown":
                score -= 20
            if record.get("confidence") == "confirmed":
                score += 5

            if score > best_score or (
                score == best_score and best is not None and record["id"] < best["id"]
            ):
                best = record
                best_score = score
        return best


if __name__ == "__main__":
    import json
    import sys

    query = " ".join(sys.argv[1:]).strip()
    print(json.dumps(TaskExecutor().plan(query), ensure_ascii=False, indent=2))
