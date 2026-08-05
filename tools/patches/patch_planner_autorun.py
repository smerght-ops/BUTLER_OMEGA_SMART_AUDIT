from pathlib import Path

p=Path(r"A_02_MANAGERS\Planner\planner_engine.py")
t=p.read_text(encoding="utf-8")

if "from A_02_MANAGERS.TaskRunner.runner_once import run_once" not in t:
    t=t.replace(
        "from A_02_MANAGERS.TaskRunner.recipe_writer import RecipeWriter",
        "from A_02_MANAGERS.TaskRunner.recipe_writer import RecipeWriter\nfrom A_02_MANAGERS.TaskRunner.runner_once import run_once"
    )

old="""        print(state)

        return path"""

new="""        print(state)

        print()
        print("AUTORUN...")

        run_once()

        return path"""

t=t.replace(old,new)

p.write_text(t,encoding="utf-8")

print("PLANNER AUTORUN PATCH OK")
