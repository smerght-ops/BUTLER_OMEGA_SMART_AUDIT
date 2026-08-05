# -*- coding: utf-8 -*-

from pathlib import Path


class InlineCodeEditor:

    def preview_replace(
        self,
        file_path,
        old_text,
        new_text
    ):

        path = Path(file_path)

        text = path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        if old_text not in text:

            return {
                "ok": False,
                "reason": "TEXT_NOT_FOUND"
            }

        updated = text.replace(
            old_text,
            new_text,
            1
        )

        return {
            "ok": True,
            "original_size": len(text),
            "new_size": len(updated),
            "changed": True
        }
