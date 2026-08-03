# -*- coding: utf-8 -*-

from A_02_MANAGERS.smart_dispatcher_v2 import SmartDispatcherV2

d = SmartDispatcherV2()

tests = [

    "кто ты",

    "что сделано",

    "статус проекта",

    "состояние проекта"

]

for t in tests:

    print("="*70)
    print(t)

    r = d.dispatch(t)

    print(r)

