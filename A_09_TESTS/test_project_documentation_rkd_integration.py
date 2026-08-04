import ast
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONSUMERS = (
    "A_04_AGENTS/ProjectDocumentationDepartment/Core/ast_parser.py",
    "A_04_AGENTS/ProjectDocumentationDepartment/Core/config_scanner.py",
    "A_04_AGENTS/ProjectDocumentationDepartment/Core/structural_extractor.py",
    "A_04_AGENTS/ProjectDocumentationDepartment/Core/ast_call_parser.py",
    "A_04_AGENTS/ProjectDocumentationDepartment/Core/ast_path_resolver.py",
    "A_01_CORE/project_indexer.py",
)


class ProjectDocumentationRkdIntegrationTests(unittest.TestCase):
    def test_consumers_use_gateway_adapter_without_repository_fallback(self):
        for relative in CONSUMERS:
            path = ROOT / relative
            tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=relative)
            imports = [node.module for node in ast.walk(tree)
                       if isinstance(node, ast.ImportFrom) and node.module]
            self.assertIn("A_03_ORCHESTRATION.repository_knowledge_gateway", imports, relative)
            self.assertFalse(any(module.endswith("RepositoryKnowledgeDepartment.service") for module in imports), relative)
            calls = []
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                if isinstance(node.func, ast.Attribute):
                    qualifier = node.func.value.id if isinstance(node.func.value, ast.Name) else ""
                    calls.append(f"{qualifier}.{node.func.attr}")
                elif isinstance(node.func, ast.Name):
                    calls.append(node.func.id)
            self.assertNotIn("os.walk", calls, relative)
            self.assertFalse(any(call.endswith(".rglob") for call in calls), relative)


if __name__ == "__main__":
    unittest.main()
