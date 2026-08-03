# -*- coding: utf-8 -*-
import contextlib
import hashlib
import io
import json
import sys
import types
import zipfile
from pathlib import Path
from unittest.mock import patch

requests = types.ModuleType("requests")
requests.get = lambda *args, **kwargs: None
requests.post = lambda *args, **kwargs: None
requests.Session = object
sys.modules.setdefault("requests", requests)

import BUTLER_OS
from A_03_ORCHESTRATION import dispatcher_bridge_v2


COMMANDS = [
    "Создай документ с двумя абзацами: Заголовок и Основной текст документа.",
    "Сделай заголовок жирным.",
    "Отцентрируй заголовок.",
    "Увеличь заголовок до 16.",
    "Выровняй основной текст по ширине.",
    "Сохрани документ.",
    "Сделай заголовок жирным.",
    "Отцентрируй заголовок.",
    "Увеличь заголовок до 16.",
    "Выровняй основной текст по ширине.",
    "Сохрани документ.",
    "exit",
]


def main():
    stream = io.StringIO()
    contracts = []
    official_dispatch = BUTLER_OS.dispatch

    def recording_dispatch(query, context=None):
        result = official_dispatch(query, context)
        contracts.append(result)
        return result

    with patch("builtins.input", side_effect=COMMANDS), patch.object(BUTLER_OS, "clear_screen"), patch.object(BUTLER_OS, "dispatch", recording_dispatch):
        with contextlib.redirect_stdout(stream):
            BUTLER_OS.main()

    documents = next(
        dept for dept in dispatcher_bridge_v2._dispatcher.departments
        if dispatcher_bridge_v2._dispatcher._dept_name(dept) == "DOCUMENTS"
    )
    path = Path(documents._active_docx)
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    doc = Document(path)
    paragraphs = doc.paragraphs
    first = paragraphs[0]
    second = paragraphs[1]
    with zipfile.ZipFile(path) as archive:
        required = {"[Content_Types].xml", "word/document.xml", "_rels/.rels"}
        zip_ok = required.issubset(set(archive.namelist()))

    result = {
        "commands": COMMANDS[:-1],
        "output": stream.getvalue(),
        "departments": [line for line in stream.getvalue().splitlines() if line.startswith("[BUTLER |")],
        "contracts": contracts,
        "path": str(path.resolve()),
        "exists": path.is_file(),
        "size": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "zip_required_parts": zip_ok,
        "paragraph_count": len(paragraphs),
        "first": {
            "text": first.text,
            "bold": all(run.bold is True for run in first.runs if run.text),
            "alignment": "CENTER" if first.alignment == WD_ALIGN_PARAGRAPH.CENTER else str(first.alignment),
            "font_sizes_pt": [run.font.size.pt if run.font.size else None for run in first.runs if run.text],
        },
        "second": {
            "text": second.text,
            "bold": any(run.bold is True for run in second.runs if run.text),
            "alignment": "JUSTIFY" if second.alignment == WD_ALIGN_PARAGRAPH.JUSTIFY else str(second.alignment),
        },
    }
    assert all(result.get("department") == "DOCUMENTS" for result in contracts), contracts
    assert all(result.get("ok") for result in contracts[:6]), contracts[:6]
    assert all(result.get("error") == "NO_CHANGES_MADE" for result in contracts[6:10]), contracts[6:10]
    assert contracts[10].get("ok") and contracts[10].get("error") is None, contracts[10]
    assert len(paragraphs) == 2
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
