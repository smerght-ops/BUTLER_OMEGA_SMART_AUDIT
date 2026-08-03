# -*- coding: utf-8 -*-

"""
MemoryAdvisor
ЗАГЛУШКА v0.1

Назначение:
- анализ последних сообщений;
- извлечение долговременных фактов;
- подготовка структуры для USER_MEMORY.

Пока ничего не меняет автоматически.
"""

class MemoryAdvisor:

    def __init__(self):
        pass

    def extract_facts(self, history):

        if not history:
            return {"facts": []}

        return {
            "facts": []
        }
