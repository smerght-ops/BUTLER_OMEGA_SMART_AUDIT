# -*- coding: utf-8 -*-

from collections import deque
from uuid import uuid4


class SessionQueue:

    def __init__(self):

        self.queue = deque()

    def push(
        self,
        task,
        source="USER"
    ):

        item = {
            "id": str(uuid4()),
            "source": source,
            "task": task
        }

        self.queue.append(item)

        return item

    def pop(self):

        if not self.queue:
            return None

        return self.queue.popleft()

    def size(self):

        return len(self.queue)

    def is_empty(self):

        return len(self.queue) == 0
