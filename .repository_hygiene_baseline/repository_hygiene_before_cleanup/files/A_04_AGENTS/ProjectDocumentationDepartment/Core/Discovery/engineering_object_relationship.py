# -*- coding: utf-8 -*-

class EngineeringObjectRelationship:
    """
    Stores parent/child relationships between Engineering Objects.
    """

    def __init__(self):
        self.parents = {}
        self.children = {}

    def add(self, parent_id: str, child_id: str):
        self.parents[child_id] = parent_id
        self.children.setdefault(parent_id, []).append(child_id)

    def get_parent(self, object_id: str):
        return self.parents.get(object_id)

    def get_children(self, object_id: str):
        return self.children.get(object_id, [])


if __name__ == "__main__":
    rel = EngineeringObjectRelationship()

    rel.add("ENG-000001", "ENG-000002")
    rel.add("ENG-000001", "ENG-000003")
    rel.add("ENG-000002", "ENG-000004")

    print("=== ENGINEERING OBJECT RELATIONSHIP TEST ===")
    print()
    print("PARENT :", rel.get_parent("ENG-000004"))
    print("CHILDREN :", rel.get_children("ENG-000001"))
