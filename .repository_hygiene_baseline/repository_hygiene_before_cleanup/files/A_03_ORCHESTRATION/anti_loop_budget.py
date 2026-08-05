# -*- coding: utf-8 -*-

class AntiLoopBudget:

    def __init__(self, limit=5):
        self.limit = limit
        self.counter = 0

    def allow(self):

        self.counter += 1

        return self.counter <= self.limit

    def reset(self):

        self.counter = 0

    def status(self):

        return {
            "counter": self.counter,
            "limit": self.limit,
            "remaining": max(0, self.limit - self.counter)
        }
