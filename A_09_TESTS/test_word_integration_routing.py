# -*- coding: utf-8 -*-
import unittest
import sys
import types

requests = types.ModuleType("requests")
requests.get = lambda *args, **kwargs: None
requests.post = lambda *args, **kwargs: None
requests.Session = object
sys.modules.setdefault("requests", requests)
import BUTLER_OS
from A_04_AGENTS.DocumentsDepartment.runner import DocumentsDepartment
from A_04_AGENTS.SearchDepartment.runner import SearchDepartment


class WordIntegrationRoutingTests(unittest.TestCase):
    def setUp(self):
        self.documents = DocumentsDepartment()
        self.search = SearchDepartment()

    def test_center_title_is_documents_not_search(self):
        query = "Отцентрируй заголовок"
        self.assertTrue(self.documents.can_handle(query, {}))
        self.assertFalse(self.search.can_handle(query, {}))

    def test_real_price_search_remains_search(self):
        self.assertTrue(self.search.can_handle("Найди информацию о цене золота", {}))
        self.assertTrue(self.search.can_handle("Цена золота сегодня", {}))

    def test_document_save_bypasses_generic_filesystem_plan(self):
        self.assertTrue(BUTLER_OS._is_active_document_command("Сохрани документ", {}))
        self.assertTrue(BUTLER_OS._is_active_document_command("Сохранить Word-документ", {}))

    def test_unrelated_save_stays_outside_document_bypass(self):
        self.assertFalse(BUTLER_OS._is_active_document_command("Сохрани изображение", {}))
        self.assertFalse(BUTLER_OS._is_active_document_command("Сохрани текст в файл", {}))


if __name__ == "__main__":
    unittest.main()
