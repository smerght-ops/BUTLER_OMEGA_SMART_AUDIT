# -*- coding: utf-8 -*-

"""
Stage 9.2

Goal Interpreter
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Goal:

    id: str
    description: str


class GoalInterpreter:

    GOALS = {

        # ---------- Python ----------

        "python version":
            Goal("GOAL_PYTHON_VERSION","Show Python version"),

        "покажи версию python":
            Goal("GOAL_PYTHON_VERSION","Show Python version"),

        "версия python":
            Goal("GOAL_PYTHON_VERSION","Show Python version"),

        # ---------- PowerShell ----------

        "powershell version":
            Goal("GOAL_POWERSHELL_VERSION","Show PowerShell version"),

        "покажи версию powershell":
            Goal("GOAL_POWERSHELL_VERSION","Show PowerShell version"),

        "версия powershell":
            Goal("GOAL_POWERSHELL_VERSION","Show PowerShell version"),

        # ---------- Audit ----------

        "run audit":
            Goal("GOAL_RUN_AUDIT","Run architecture audit"),

        "запусти аудит":
            Goal("GOAL_RUN_AUDIT","Run architecture audit"),

        "сделай аудит":
            Goal("GOAL_RUN_AUDIT","Run architecture audit"),
    }

    @classmethod
    def interpret(cls, text: str):

        if not text:
            return None

        key = " ".join(
            text.strip().lower().split()
        )

        return cls.GOALS.get(key)


if __name__=="__main__":

    tests = [

        "python version",
        "покажи версию python",

        "powershell version",
        "версия powershell",

        "run audit",
        "сделай аудит",

        "unknown"

    ]

    for t in tests:
        print(t,"->",GoalInterpreter.interpret(t))
