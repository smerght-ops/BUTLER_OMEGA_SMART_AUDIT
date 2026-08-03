# -*- coding: utf-8 -*-
import contextlib
import io
import sys
import types
from unittest.mock import patch

requests = types.ModuleType("requests")
requests.get = lambda *args, **kwargs: None
requests.post = lambda *args, **kwargs: None
requests.Session = object
sys.modules.setdefault("requests", requests)

import BUTLER_OS


def main():
    stream = io.StringIO()
    commands = [
        "Отцентрируй заголовок",
        "Сохрани документ",
        "Создай пустой документ",
        "Сделай заголовок жирным",
        'Создай документ с текстом "Заголовок"',
        "Выровняй основной текст по ширине",
        "exit",
    ]
    with patch("builtins.input", side_effect=commands), patch.object(BUTLER_OS, "clear_screen"):
        with contextlib.redirect_stdout(stream):
            BUTLER_OS.main()
    output = stream.getvalue()
    assert output.count("[BUTLER | DOCUMENTS") == 6, output
    assert output.count("[ERROR] DOCUMENT_NOT_FOUND") == 2, output
    assert output.count("[ERROR] FORMAT_TARGET_NOT_FOUND") == 2, output
    assert "[BUTLER | SEARCH" not in output, output
    assert "FILESYSTEM_OPERATION_FAILED" not in output, output
    print(output)


if __name__ == "__main__":
    main()
