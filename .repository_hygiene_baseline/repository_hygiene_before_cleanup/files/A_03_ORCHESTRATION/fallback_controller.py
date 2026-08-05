# -*- coding: utf-8 -*-

class FallbackController:

    def __init__(self):

        self.handlers = {}

    def register(
        self,
        department,
        fallback
    ):

        self.handlers[department] = fallback

    def run(
        self,
        department,
        error=None
    ):

        fn = self.handlers.get(department)

        if fn is None:

            return {
                "fallback_used": False,
                "error": error
            }

        result = fn()

        return {
            "fallback_used": True,
            "department": department,
            "result": result,
            "error": error
        }
