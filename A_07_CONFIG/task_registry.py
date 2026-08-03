# -*- coding: utf-8 -*-
import sys

TASKS = {

    "task_verify_contour":[

        [sys.executable,"-m","py_compile","A_07_MEMORY/semantic_core.py"],
        [sys.executable,"-m","py_compile","A_07_MEMORY/agent_planner.py"],
        [sys.executable,"-m","A_07_MEMORY.STAGE1_ACCEPTANCE"]
    ],

    "task_run_full_audit":[

        [sys.executable,"-m","py_compile","A_02_MANAGERS/smart_dispatcher_v2.py"],
        [sys.executable,"-m","py_compile","A_02_MANAGERS/TaskRunner/runner.py"],
        [sys.executable,"-m","py_compile","A_07_MEMORY/semantic_core.py"],
        [sys.executable,"-m","py_compile","A_07_MEMORY/agent_planner.py"],
        [sys.executable,"-m","py_compile","A_07_CONFIG/task_registry.py"],
        [sys.executable,"-m","A_07_MEMORY.STAGE1_ACCEPTANCE"]

    ],

    "task_flush_invalid_facts":[

        [sys.executable,"-c","print('MEMORY FLUSH READY')"]

    ],

    "task_generate_docs":[

        [sys.executable,"-m","A_07_MEMORY.architectural_knowledge_graph"]

    ],

    "verify":[

        [sys.executable,"-m","py_compile","A_07_MEMORY/semantic_core.py"],
        [sys.executable,"-m","A_07_MEMORY.STAGE1_ACCEPTANCE"]

    ]

}
