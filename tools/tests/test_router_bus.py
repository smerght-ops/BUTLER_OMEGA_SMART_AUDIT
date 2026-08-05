# -*- coding: utf-8 -*-

from A_03_ORCHESTRATION.router_integration import RouterIntegration

router = RouterIntegration()

tests = [

    "кто ты",

    "что сделано",

    "что дальше",

    "паспорт"

]

for t in tests:

    print("=" * 70)
    print("QUERY:", t)
    print("=" * 70)

    result = router.dispatch(t)

    print(result)
    print()
