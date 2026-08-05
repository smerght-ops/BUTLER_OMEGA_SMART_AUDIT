# -*- coding: utf-8 -*-

from A_07_CONFIG.project_state import ProjectState


class PassportReport:

    def __init__(self):
        self.state = ProjectState()

    def print_header(self):
        identity = self.state.identity()

        print("=" * 70)
        print("               BUTLER OMEGA SMART PASSPORT")
        print("=" * 70)

        print(f"Project : {identity.get('name')}")
        print(f"Version : {identity.get('version')}")
        print(f"Stage   : {self.state.current_stage()}")

    def print_components(self):

        print()
        print("=" * 70)
        print("REGISTERED COMPONENTS")
        print("=" * 70)

        for item in self.state.modules():
            print(f"[OK] {item['name']}")

        print()
        print(f"Total Components : {len(self.state.modules())}")

    def print_footer(self):

        print()
        print("=" * 70)
        print("NEXT OFFICIAL TASK")
        print("=" * 70)

        print("SEMANTIC_REASONING_ENGINE")

        print("=" * 70)

    def print_report(self):

        self.print_header()
        self.print_components()
        self.print_footer()


if __name__ == "__main__":
    PassportReport().print_report()
