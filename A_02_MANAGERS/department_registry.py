"""Canonical declarative table of routable production Departments."""

from importlib import import_module


DEPARTMENTS = {
    "PUBLICATION_GUARDIAN": {"module": "A_04_AGENTS.PublicationGuardianDepartment.runner", "class": "PublicationGuardianDepartment", "component_type": "DEPARTMENT", "order": 10},
    "REPOSITORY_KNOWLEDGE": {"module": "A_04_AGENTS.RepositoryKnowledgeDepartment.runner", "class": "RepositoryKnowledgeDepartment", "component_type": "DEPARTMENT", "order": 20},
    "ENGINEERING_REVIEW": {"module": "A_04_AGENTS.EngineeringReviewDepartment.runner", "class": "EngineeringReviewDepartment", "component_type": "DEPARTMENT", "order": 30},
    "PROJECT_DOCUMENTATION": {"module": "A_04_AGENTS.ProjectDocumentationDepartment.runner", "class": "ProjectDocumentationDepartment", "component_type": "DEPARTMENT", "order": 40},
    "BROWSER": {"module": "A_04_AGENTS.BrowserDepartment.runner", "class": "BrowserDepartment", "component_type": "DEPARTMENT", "order": 50},
    "IMAGE": {"module": "A_04_AGENTS.ImageDepartment.runner", "class": "ImageDepartment", "component_type": "DEPARTMENT", "order": 60},
    "VIDEO": {"module": "A_04_AGENTS.VideoDepartment.runner", "class": "VideoDepartment", "component_type": "DEPARTMENT", "order": 70},
    "AUDIO": {"module": "A_04_AGENTS.AudioDepartment.runner", "class": "AudioDepartment", "component_type": "DEPARTMENT", "order": 80},
    "ARCHIVE": {"module": "A_04_AGENTS.ArchiveDepartment.runner", "class": "ArchiveDepartment", "component_type": "DEPARTMENT", "order": 90},
    "FILESYSTEM": {"module": "A_04_AGENTS.FilesystemDepartment.runner", "class": "FilesystemDepartment", "component_type": "DEPARTMENT", "order": 100},
    "CODING": {"module": "A_04_AGENTS.CodingDepartment.runner", "class": "CodingDepartment", "component_type": "DEPARTMENT", "order": 110},
    "COMPUTER_USE": {"module": "A_04_AGENTS.ComputerUseDepartment.runner", "class": "ComputerUseDepartment", "component_type": "DEPARTMENT", "order": 115},
    "VISION": {"module": "A_04_AGENTS.VisionDepartment.runner", "class": "VisionDepartment", "component_type": "DEPARTMENT", "order": 120},
    "SEARCH": {"module": "A_04_AGENTS.SearchDepartment.runner", "class": "SearchDepartment", "component_type": "DEPARTMENT", "order": 130},
    "MEMORY": {"module": "A_04_AGENTS.MemoryDepartment.runner", "class": "MemoryDepartment", "component_type": "DEPARTMENT", "order": 140},
    "OPEN_DOCUMENT": {"module": "A_04_AGENTS.OpenDocumentDepartment.runner", "class": "OpenDocumentDepartment", "component_type": "DEPARTMENT", "order": 150},
    "DOCUMENTS": {"module": "A_04_AGENTS.DocumentsDepartment.runner", "class": "DocumentsDepartment", "component_type": "DEPARTMENT", "order": 160},
    "TEXT": {"module": "A_04_AGENTS.TextDepartment.runner", "class": "TextDepartment", "component_type": "DEPARTMENT", "order": 170},
    "HOME": {"module": "A_04_AGENTS.HomeDepartment.runner", "class": "HomeDepartment", "component_type": "DEPARTMENT", "order": 180}
}


COMPONENTS = {
    "GOAL_MANAGER": {"module": "A_02_MANAGERS.goal_manager", "class": "GoalManager", "component_type": "MANAGER", "status": "ACTIVE_SUPPORT", "routable": True, "order": 105},
    "CHAT_PROVIDER": {"module": "A_02_MANAGERS.smart_dispatcher", "class": "SmartDispatcher", "component_type": "SERVICE", "status": "ACTIVE_SUPPORT"}
}


def department_specs():
    return tuple(sorted(DEPARTMENTS.items(), key=lambda item: item[1]["order"]))


def routable_specs():
    """Return Departments plus explicitly routable support components."""
    support = (
        (name, spec) for name, spec in COMPONENTS.items()
        if spec.get("routable") is True
    )
    return tuple(sorted((*DEPARTMENTS.items(), *support),
                        key=lambda item: item[1]["order"]))


def instantiate_departments():
    instances = []
    for expected_name, spec in routable_specs():
        cls = getattr(import_module(spec["module"]), spec["class"])
        instance = cls()
        actual_name = str(getattr(instance, "NAME", "")).upper()
        if actual_name != expected_name:
            raise RuntimeError(f"ROUTABLE_NAME_MISMATCH:{expected_name}:{actual_name}")
        if not callable(getattr(instance, "can_handle", None)) or not callable(getattr(instance, "execute", None)):
            raise RuntimeError(f"ROUTABLE_CONTRACT_INVALID:{expected_name}")
        instances.append(instance)
    return instances
