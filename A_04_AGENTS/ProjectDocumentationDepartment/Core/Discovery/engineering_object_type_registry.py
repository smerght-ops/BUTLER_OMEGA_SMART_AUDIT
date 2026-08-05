# -*- coding: utf-8 -*-

ENGINEERING_OBJECT_TYPES = {
    "DEPARTMENT",
    "AGENT",
    "DISCOVERY_AGENT",
    "INSPECTOR",
    "PROPOSAL",
    "REPORT",
    "CONTRACT",
    "ROADMAP",
    "PASSPORT",
    "REGISTRY",
    "STATE",
    "OBJECT",
    "TEST",
    "WORKFLOW",
    "SERVICE",
    "MODEL",
    "CONFIG",
    "SCRIPT",
    "DIRECTORY",
    "FILE"
}


def has_type(type_name: str) -> bool:
    return type_name.upper() in ENGINEERING_OBJECT_TYPES


if __name__ == "__main__":
    print("=== ENGINEERING OBJECT TYPE REGISTRY ===")
    print()
    print("REGISTERED:", len(ENGINEERING_OBJECT_TYPES))
    print()

    for t in sorted(ENGINEERING_OBJECT_TYPES):
        print(t)
