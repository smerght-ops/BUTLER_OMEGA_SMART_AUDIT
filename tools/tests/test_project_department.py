# -*- coding: utf-8 -*-

from A_04_AGENTS.ProjectDocumentationDepartment.runner import ProjectDocumentationDepartment

d = ProjectDocumentationDepartment()

tests = [

    "кто ты",

    "что сделано",

    "статус проекта",

    "состояние проекта"

]

for t in tests:

    print(f"{t:20} -> {d.can_handle(t)}")

