class MemoryLoop:
    def __init__(self):
        self._memory = []

    def remember(self, value):
        self._memory.append(value)

    def recall(self):
        return list(self._memory)


if __name__ == "__main__":
    mem = MemoryLoop()
    mem.remember("OK")

    if mem.recall() != ["OK"]:
        raise RuntimeError("MemoryLoop self-test failed")

    print("MEMORY LOOP LAB PASSED")
