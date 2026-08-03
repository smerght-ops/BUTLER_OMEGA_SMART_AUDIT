import unittest

from A_01_CORE.TaskExecutor.task_executor import TaskExecutor


class TaskExecutorAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.planner = TaskExecutor()

    def departments(self, query):
        return [step["department"] for step in self.planner.plan(query)["steps"]]

    def test_1_poem(self):
        plan = self.planner.plan("Напиши стихотворение.")
        self.assertEqual(["TEXT"], self.departments("Напиши стихотворение."))
        self.assertEqual("planned", plan["status"])

    def test_2_translate_document(self):
        self.assertEqual(
            ["DOCUMENTS", "TEXT"],
            self.departments("Переведи документ."),
        )

    def test_3_describe_and_save(self):
        plan = self.planner.plan("Опиши изображение и сохрани описание.")
        self.assertEqual(["VISION", "FILESYSTEM"], [x["department"] for x in plan["steps"]])
        self.assertEqual("planned", plan["status"])

    def test_4_create_folder(self):
        plan = self.planner.plan("Создай папку.")
        self.assertEqual(["FILESYSTEM"], [x["department"] for x in plan["steps"]])
        self.assertEqual("planned", plan["status"])

    def test_5_find_pdf_and_summarize(self):
        self.assertEqual(
            ["SEARCH", "DOCUMENTS", "TEXT"],
            self.departments("Найди PDF и сделай краткое содержание."),
        )

    def test_6_composite_task(self):
        query = (
            "Напиши стихотворение, создай папку, сохрани туда стихотворение "
            "и нарисуй иллюстрацию."
        )
        plan = self.planner.plan(query)
        self.assertEqual(
            ["TEXT", "FILESYSTEM", "FILESYSTEM", "IMAGE", "FILESYSTEM"],
            [x["department"] for x in plan["steps"]],
        )
        self.assertEqual("planned", plan["status"])

    def test_planner_does_not_execute(self):
        plan = self.planner.plan("Создай папку.")
        self.assertNotIn("result", plan)
        self.assertTrue(all(step["status"] in {"planned", "missing_capability"} for step in plan["steps"]))

    def test_stage5_project_expands_explicit_count(self):
        query = (
            "Создай на рабочем столе проект «Стихи о море». Напиши пять стихотворений. "
            "Для каждого создай отдельную иллюстрацию. Создай общий файл содержания, "
            "упакуй проект в ZIP-архив и запомни путь к архиву."
        )
        plan = self.planner.plan(query)
        self.assertEqual("planned", plan["status"])
        self.assertEqual(5, plan["variables"]["count"])
        self.assertEqual("explicit", plan["variables"]["count_source"])
        self.assertEqual(24, len(plan["steps"]))
        self.assertEqual(5, sum(step["action"] == "generate_text" for step in plan["steps"]))
        self.assertEqual(5, sum(step["action"] == "generate_comfyui_image" for step in plan["steps"]))
        self.assertEqual("create_archive", plan["steps"][-2]["action"])
        self.assertEqual("write_profile_fact", plan["steps"][-1]["action"])

    def test_stage5_project_defaults_count_and_documents_source(self):
        query = (
            "Создай проект «Стихи о море» со стихотворениями и иллюстрациями, "
            "создай ZIP-архив и запомни путь."
        )
        plan = self.planner.plan(query)
        self.assertEqual(3, plan["variables"]["count"])
        self.assertEqual("default", plan["variables"]["count_source"])


if __name__ == "__main__":
    unittest.main()
