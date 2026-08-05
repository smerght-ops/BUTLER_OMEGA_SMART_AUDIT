# -*- coding: utf-8 -*-

from A_03_ORCHESTRATION.router_integration import RouterIntegration

router = RouterIntegration()

tests = [

    "кто ты",

    "что сделано",

    "что дальше",

    "паспорт",

    "статус"

]

markers = [

    "BUTLER OMEGA SMART PASSPORT",

    "СВОДКА ИСТОРИИ",

    "NEXT ROADMAP TASKS"

]

for t in tests:

    r = router.dispatch(t)

    ok = any(m in r for m in markers)

    print(f"{t:20} -> {'OK' if ok else 'FAIL'}")
