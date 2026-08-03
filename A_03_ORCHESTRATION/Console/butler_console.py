# -*- coding: utf-8 -*-

"""
Stage 10.1

BUTLER Console

Unified user interface.
"""

from A_02_MANAGERS.Planner.planner_engine import PlannerEngine


def main():

    print()

    print("="*60)
    print("          BUTLER OS")
    print("="*60)
    print()

    print("Type 'exit' to quit.")
    print()

    while True:

        cmd = input("BUTLER> ").strip()

        if not cmd:

            continue

        if cmd.lower() in ("exit","quit"):

            break

        PlannerEngine.execute(cmd)

        print()


if __name__ == "__main__":

    main()

