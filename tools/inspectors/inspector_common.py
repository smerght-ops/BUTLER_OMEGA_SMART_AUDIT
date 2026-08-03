# -*- coding: utf-8 -*-
"""
Inspector Common Library v1.0
READ ONLY.
Общие функции для всех Inspector.
"""

from pathlib import Path
import json
from datetime import datetime, timezone


def utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")


def read_json(path):
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    with Path(path).open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_source(path):
    return Path(path).read_text(
        encoding="utf-8-sig",
        errors="ignore"
    )


def python_files(physical_map):
    root = Path(physical_map["metadata"]["project_root"])

    for item in physical_map["payload"]:
        if item.get("kind") != "python":
            continue

        yield {
            "id": item.get("id"),
            "relative_path": item["relative_path"],
            "path": root / item["relative_path"]
        }


def make_metadata(
    schema,
    version,
    generator,
    input_name,
    statistics
):
    return {
        "schema": schema,
        "schema_version": version,
        "generator": generator,
        "generated_utc": utc_now(),
        "input": input_name,
        "statistics": statistics
    }
