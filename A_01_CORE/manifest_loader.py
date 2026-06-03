import json
from pathlib import Path


class ManifestLoader:

    @staticmethod
    def load():

        manifest_path = (
            Path(__file__).resolve().parent.parent
            / "A_07_CONFIG"
            / "system_manifest.json"
        )

        if not manifest_path.exists():
            raise FileNotFoundError(
                f"Manifest не найден: {manifest_path}"
            )

        with open(
            manifest_path,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)