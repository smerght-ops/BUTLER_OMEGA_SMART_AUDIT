# -*- coding: utf-8 -*-

from engineering_object_catalog import EngineeringObjectCatalog


class ConflictResolution:
    """
    PHASE 5.2

    Resolves duplicate EngineeringObjects.
    """

    def resolve(self, catalog: EngineeringObjectCatalog):

        unique = EngineeringObjectCatalog()

        for obj in catalog.all():

            if unique.exists(obj.object_id):
                continue

            unique.register(obj)

        return unique


if __name__ == "__main__":

    from engineering_object import EngineeringObject

    catalog = EngineeringObjectCatalog()

    obj1 = EngineeringObject()
    obj1.object_id = "ENG-000001"
    obj1.name = "Passport"

    obj2 = EngineeringObject()
    obj2.object_id = "ENG-000001"
    obj2.name = "Passport Duplicate"

    catalog.register(obj1)
    catalog.register(obj2)

    resolver = ConflictResolution()

    result = resolver.resolve(catalog)

    print("=== CONFLICT RESOLUTION TEST ===")
    print()
    print("OBJECTS :", result.count())
    print("FIRST   :", result.all()[0].name)
