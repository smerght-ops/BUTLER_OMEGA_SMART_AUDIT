import unittest

from A_04_COMPONENTS.ProjectAuditor.project_auditor import ProjectAuditor

class TestProjectAuditor(unittest.TestCase):

    def test_stub(self):
        obj = ProjectAuditor()
        res = obj.run()
        self.assertEqual(res["status"], "not_implemented")

if __name__ == "__main__":
    unittest.main()
