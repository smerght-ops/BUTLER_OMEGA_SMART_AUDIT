import json
from pathlib import Path

def load_manifest():
    path = Path("A_07_CONFIG/system_manifest.json")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

config = load_manifest()