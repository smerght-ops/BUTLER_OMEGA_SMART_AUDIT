# -*- coding: utf-8 -*-

from .runner import CodingDepartment
from A_03_ORCHESTRATION.permission import DepartmentExecutionGateway

_department = CodingDepartment()
_gateway = DepartmentExecutionGateway()

def can_handle(query: str) -> bool:
    return _department.can_handle(query)

def execute(query: str):
    return _gateway.execute(_department, query)

def fallback(query: str):
    return _department.fallback(query)
