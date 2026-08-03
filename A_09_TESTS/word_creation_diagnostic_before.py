# -*- coding: utf-8 -*-
import contextlib
import io
import sys
import types
import re
from pathlib import Path
from unittest.mock import patch

requests = types.ModuleType("requests")
requests.get = lambda *args, **kwargs: None
requests.post = lambda *args, **kwargs: None
requests.Session = object
sys.modules.setdefault("requests", requests)

import BUTLER_OS


CASES = [
    "Создай документ",
    "Создай пустой документ",
    "Создай новый документ",
    "Новый документ",
    'Создай документ с текстом "Тест"',
    'Создай документ и напиши "Пример"',
    "Создай Word-документ",
    "Создай Word-файл",
]


def main():
    for query in CASES:
        stream = io.StringIO()
        with patch("builtins.input", side_effect=[query, "exit"]), patch.object(BUTLER_OS, "clear_screen"):
            with contextlib.redirect_stdout(stream):
                BUTLER_OS.main()
        lines = [line for line in stream.getvalue().splitlines() if line.startswith("[BUTLER |") or line.startswith("[ERROR]")]
        output = stream.getvalue()
        assert "[BUTLER | DOCUMENTS" in output, output
        assert "[ERROR]" not in output, output
        match = re.search(r"DOCX успешно создан и открыт:\s*(.+\.docx)", output)
        assert match and Path(match.group(1).strip()).is_file(), output
        print(query, "=>", " | ".join(lines))


if __name__ == "__main__":
    main()
