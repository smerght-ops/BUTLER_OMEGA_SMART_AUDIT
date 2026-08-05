# -*- coding: utf-8 -*-

class EngineeringObjectIdentifier:
    """
    Generates stable Engineering Object IDs.

    Format:
        ENG-000001
        ENG-000002
        ...
    """

    def __init__(self, prefix="ENG"):
        self.prefix = prefix
        self._next = 1

    def next_id(self):
        object_id = f"{self.prefix}-{self._next:06d}"
        self._next += 1
        return object_id


if __name__ == "__main__":
    gen = EngineeringObjectIdentifier()

    print("=== ENGINEERING OBJECT IDENTIFIER TEST ===")
    print()

    for _ in range(5):
        print(gen.next_id())
