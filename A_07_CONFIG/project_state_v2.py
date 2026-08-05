# -*- coding: utf-8 -*-

from A_07_CONFIG.project_passport_loader import ProjectPassportLoader
from A_07_CONFIG.registry_loader import RegistryLoader


class ProjectState:

    def __init__(self):
        self.passport = ProjectPassportLoader()
        self.registry = RegistryLoader()

        self.raw = self.passport.load_passport()

    def identity(self):
        return self.raw.get("project_identity", {})

    def current_stage(self):
        return self.identity().get("current_stage", "UNKNOWN")

    def roadmap(self):
        return self.raw.get("roadmap_pointer", {})

    def proofs(self):
        return self.raw.get("execution_proof_map", {})

    def limitations(self):
        return self.raw.get("known_limitations", {})

    def registry_info(self):
        return self.raw.get("architecture_registry", {})

    def modules(self):
        return self.registry.get_modules()

    def summary(self):
        return {
            "identity": self.identity(),
            "current_stage": self.current_stage(),
            "roadmap": self.roadmap(),
            "registry": self.registry_info(),
            "modules": self.modules()
        }


if __name__ == "__main__":

    state = ProjectState()

    print("=== PROJECT STATE ===")
    print(state.summary())
