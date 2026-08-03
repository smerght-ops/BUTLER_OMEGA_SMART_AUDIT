# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

class Department(ABC):
    name = "BaseDepartment"

    @abstractmethod
    def can_handle(self, text: str) -> bool:
        pass

    @abstractmethod
    def execute(self, text: str) -> str:
        pass

    def fallback(self, text: str) -> str:
        return f"[{self.name}] Резервный контур пока не настроен."