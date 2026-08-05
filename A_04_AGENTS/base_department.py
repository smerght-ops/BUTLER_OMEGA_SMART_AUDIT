# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

class BaseDepartment(ABC):
    NAME = "BASE"

    @abstractmethod
    def can_handle(self, query: str, context: dict = None) -> bool:
        pass

    @abstractmethod
    def execute(self, query: str, context: dict = None, **kwargs) -> dict:
        pass

    def __repr__(self):
        return f"<Department: {self.NAME}>"
