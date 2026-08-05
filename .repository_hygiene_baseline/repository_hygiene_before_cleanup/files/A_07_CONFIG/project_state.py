# -*- coding: utf-8 -*-

from A_07_CONFIG.project_passport_loader import ProjectPassportLoader
from A_07_CONFIG.registry_loader import RegistryLoader


class ProjectState:

    def __init__(self):
        self.passport = ProjectPassportLoader()
        self.registry = RegistryLoader()

    def identity(self):
        return self.passport.get_identity()

    def current_stage(self):
        return self.passport.get_current_stage()

    def modules(self):
        return self.registry.get_modules()

    def summary(self):
        return {
            "identity": self.identity(),
            "current_stage": self.current_stage(),
            "modules": self.modules()
        }


if __name__ == "__main__":

    state = ProjectState()

    print("=== PROJECT STATE ===")
    print(state.summary())
