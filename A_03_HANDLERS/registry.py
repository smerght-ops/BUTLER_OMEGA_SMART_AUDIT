from pathlib import Path

from A_03_HANDLERS.code_handler import CodeHandler
from A_03_HANDLERS.text_handler import TextHandler
from A_03_HANDLERS.docx_handler import DocxHandler
from A_03_HANDLERS.pdf_handler import PDFHandler
from A_03_HANDLERS.spreadsheet_handler import SpreadsheetHandler
from A_03_HANDLERS.image_handler import ImageHandler
from A_03_HANDLERS.archive_handler import ArchiveHandler


class HandlerRegistry:

    def __init__(self):

        self.handlers = [
            CodeHandler(),
            TextHandler(),
            DocxHandler(),
            PDFHandler(),
            SpreadsheetHandler(),
            ImageHandler(),
            ArchiveHandler(),
        ]

    def get_handler(self, file_path):

        path = Path(file_path)

        for handler in self.handlers:
            if handler.can_handle(path):
                return handler

        return None


registry = HandlerRegistry()