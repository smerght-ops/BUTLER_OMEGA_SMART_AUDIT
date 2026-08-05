# -*- coding: utf-8 -*-
import json
from A_04_AGENTS.OpenDocumentDepartment.runner import OpenDocumentDepartment

dept = OpenDocumentDepartment()
print("=== ТЕСТ ЭТАПА А: АВТОНОМНЫЙ ДЕПАРТАМЕНТ ===")
print("can_handle('открой первый') :", dept.can_handle("открой первый"))
print("can_handle('прочитай файл') :", dept.can_handle("прочитай файл"))

print("\nВызов execute('открой первый'):")
res = dept.execute("открой первый")
print("Результат execute:")
print(json.dumps(res, indent=2, ensure_ascii=False))
print("Тип ответа                 :", type(res).__name__)
