# -*- coding: utf-8 -*-

from A_04_AGENTS.SearchDepartment.runner import SearchDepartment

d = SearchDepartment()

q = "найди паспорт"

print(q)
print(d.can_handle(q))
