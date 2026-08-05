import unittest

from A_04_COMPONENTS.MemoryAdvisor.memory_advisor import MemoryAdvisor

class TestMemoryAdvisor(unittest.TestCase):

    def test_empty(self):
        adv = MemoryAdvisor()
        self.assertEqual(
            adv.extract_facts([]),
            {"facts": []}
        )

if __name__ == "__main__":
    unittest.main()
