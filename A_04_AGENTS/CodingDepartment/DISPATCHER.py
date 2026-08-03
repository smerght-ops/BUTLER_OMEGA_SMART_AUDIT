# -*- coding: utf-8 -*-

from .runner import CodingDepartment

_department = CodingDepartment()

def can_handle(query: str) -> bool:
    return _department.can_handle(query)

def execute(query: str):
    return _department.execute(query)

def fallback(query: str):
    return _department.fallback(query)