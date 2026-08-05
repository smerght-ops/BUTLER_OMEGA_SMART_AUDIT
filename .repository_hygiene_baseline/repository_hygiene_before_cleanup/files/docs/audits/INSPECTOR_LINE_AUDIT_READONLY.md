# INSPECTOR LINE AUDIT — READ ONLY

Generated: 2026-07-09 09:03:26


============================================================
## BaseInspector.py
============================================================

STATUS: FOUND
SIZE  : 5480 bytes
DATE  : 2026-07-08 00:52:08
LINES : 133

### FIRST 40 LINES
#!/usr/bin/env python3
"""
BaseInspector — общий каркас для всех измерительных приборов.
Обеспечивает:
- загрузку PhysicalMap
- фильтрацию файлов по kind и передачу полной информации о файле
- обработку файлов с pathlib и кодировкой utf-8-sig
- сбор ошибок и сохранение относительных путей (id)
- генерацию метаданных и статистики
- запись JSON с единой структурой
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class BaseInspector(ABC):
    SCHEMA: str = "base"
    SCHEMA_VERSION: str = "1.0"
    GENERATOR: str = "BaseInspector"
    GENERATOR_VERSION: str = "1.0"
    TARGET_KIND: str = "python"  # по умолчанию

    def __init__(self, input_path: str, output_path: str):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.errors: List[Dict] = []
        self.payload: List[Dict] = []
        self.metadata: Dict = {}
        self.project_root: Path = None

    def load_physical_map(self) -> Dict:
        """Загружает PhysicalMap из JSON."""
        try:
            with open(self.input_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:

### IMPORTS
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

### CLASSES
class BaseInspector(ABC):

### FUNCTIONS
    def __init__(self, input_path: str, output_path: str):
    def load_physical_map(self) -> Dict:
    def get_file_infos(self, physical_map: Dict) -> List[Dict]:
    def process_file(self, file_info: Dict) -> Dict:
    def run(self):
    def _add_statistics(self):

### MAIN / OUTPUT / INPUT MARKERS
- обработку файлов с pathlib и кодировкой utf-8-sig
- запись JSON с единой структурой
import json
from pathlib import Path
    SCHEMA: str = "base"
    SCHEMA_VERSION: str = "1.0"
    GENERATOR_VERSION: str = "1.0"
    def __init__(self, input_path: str, output_path: str):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.project_root: Path = None
        """Загружает PhysicalMap из JSON."""
            with open(self.input_path, 'r', encoding='utf-8') as f:
                return json.load(f)
            print(f"ERROR: Cannot read {self.input_path}: {e}", file=sys.stderr)
        self.project_root = Path(physical_map["metadata"]["project_root"])
                path = self.project_root / item["relative_path"]
                if path.exists():
                        "relative_path": item["relative_path"],  # обязательно есть
                        "path": path,
                    print(f"WARNING: File not found: {path}", file=sys.stderr)
            id, relative_path, path, kind, size_bytes, modified_utc
            "schema": self.SCHEMA,
            "schema_version": self.SCHEMA_VERSION,
            "generator_version": self.GENERATOR_VERSION,
            "input": {
                "physical_map": str(self.input_path),
        # Запись выходного JSON
        output = {
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            print(f"ERROR: Failed to write output: {e}", file=sys.stderr)
        print(f"OUTPUT  : {self.output_path}")

============================================================
## InspectorKnowledgeLayer.py
============================================================

STATUS: FOUND
SIZE  : 4344 bytes
DATE  : 2026-07-08 10:28:17
LINES : 161

### FIRST 40 LINES
#!/usr/bin/env python3
# InspectorKnowledgeLayer.py
# READ ONLY. Только поиск упоминаний. Без записи, без pip, без subprocess.

import sys
import re
from pathlib import Path

MAX_FILE_SIZE = 10 * 1024 * 1024

TEXT_EXT = {
    ".txt", ".md", ".json", ".yml", ".yaml",
    ".ini", ".cfg", ".py", ".ps1", ".bat", ".cmd"
}

IGNORE_DIRS = {
    "__pycache__", ".git", "venv", ".venv", "env",
    "node_modules", "chroma_db", "dist", "build",
    "A_00_ARCHIVE_BACKUPS", "ROLLBACK_POINTS",
    "EMERGENCY_BEFORE_RESTORE"
}

IGNORE_EXT = {
    ".pyc", ".pyo", ".dll", ".exe",
    ".7z", ".zip", ".rar", ".bin", ".dat"
}

INTERNAL_KNOWLEDGE_DIRS = [
    "A_00_ARCHITECTURE",
    "A_07_CONFIG",
    "A_08_LOGS"
]

EXTERNAL_KNOWLEDGE_DIRS = [
    r"C:\Users\KOS\Desktop\Работа с батлером файлы\Docs",
    r"C:\Users\KOS\Desktop\Работа с батлером файлы\Data"
]

HISTORY_DIRS = [
    "A_08_LOGS",

### IMPORTS
import sys
import re
from pathlib import Path

### CLASSES

### FUNCTIONS
def ignored(p: Path) -> bool:
def safe_read(p: Path) -> str:
def make_patterns(query: str):
def search_roots(query: str, roots):
def print_block(title: str, data: dict):
def main():

### MAIN / OUTPUT / INPUT MARKERS
# READ ONLY. Только поиск упоминаний. Без записи, без pip, без subprocess.
from pathlib import Path
    ".txt", ".md", ".json", ".yml", ".yaml",
def ignored(p: Path) -> bool:
def safe_read(p: Path) -> str:
        raw = p.read_bytes()
        base = Path(base)
            text = safe_read(f)
                rel = str(f.relative_to(Path.cwd()))
    for path, snippets in sorted(data.items()):
        print(f"- {path} ({len(snippets)} fragments)")
    root = Path.cwd()
    external_roots = [Path(d) for d in EXTERNAL_KNOWLEDGE_DIRS]
if __name__ == "__main__":

============================================================
## Inspector-Discovery.py
============================================================

STATUS: FOUND
SIZE  : 9029 bytes
DATE  : 2026-07-08 02:56:59
LINES : 234

### FIRST 40 LINES
#!/usr/bin/env python3
"""
UltimateRealityDiscovery (any) — полный поиск по проекту для запрошенной capability.
Собирает все доказательства из всех артефактов: файлы, классы, функции, импорты,
вызовы, регистрации, связи, JSON, паспорты, манифесты. Группирует в единую capability.
Использует логику OR для ключевых слов.
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict, deque

ROOT = Path.cwd()

def load_artifact(name):
    filenames = {
        "PhysicalMap": "Inspector0_PhysicalMap.json",
        "EntityMap": "Inspector1_EntityMap.json",
        "ImportMap": "Inspector2_ImportMap.json",
        "RegistrationAST": "Inspector3_RegistrationAST.json",
        "CallGraph": "Inspector4_CallGraph.json",
        "LinkMap": "LinkMap.json",
        "DependencyModel": "DependencyModel.json",
    }
    path = ROOT / filenames.get(name, "")
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except:
        return None

def find_entities_by_keywords(keywords, entity_map, physical_map):
    """Находит сущности, чьи имена содержат хотя бы одно ключевое слово."""
    entities = set()
    for entry in entity_map.get("payload", []):
        file_id = entry["id"]
        file_path = None

### IMPORTS
import json
import re
import sys
from pathlib import Path
from collections import defaultdict, deque

### CLASSES

### FUNCTIONS
def load_artifact(name):
def find_entities_by_keywords(keywords, entity_map, physical_map):
def collect_entity_evidence(entity_name, artifacts):
def build_capability_cluster(keywords, artifacts):
def main():

### MAIN / OUTPUT / INPUT MARKERS
вызовы, регистрации, связи, JSON, паспорты, манифесты. Группирует в единую capability.
import json
from pathlib import Path
ROOT = Path.cwd()
def load_artifact(name):
        "PhysicalMap": "Inspector0_PhysicalMap.json",
        "EntityMap": "Inspector1_EntityMap.json",
        "ImportMap": "Inspector2_ImportMap.json",
        "RegistrationAST": "Inspector3_RegistrationAST.json",
        "CallGraph": "Inspector4_CallGraph.json",
        "LinkMap": "LinkMap.json",
        "DependencyModel": "DependencyModel.json",
    path = ROOT / filenames.get(name, "")
    if not path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
        file_path = None
                    file_path = item["relative_path"]
                entities.add((name, "class", file_id, file_path))
                entities.add((name, "function", file_id, file_path))
                evidence["links"].add((json.dumps(link, ensure_ascii=False, sort_keys=True), None))
    for entity, etype, file_id, file_path in entities:
        all_files.add((file_id, file_path))
    for entity, etype, file_id, file_path in entities:
            final_entities.add((entity, etype, file_id, file_path))
        "PhysicalMap": load_artifact("PhysicalMap"),
        "EntityMap": load_artifact("EntityMap"),
        "ImportMap": load_artifact("ImportMap"),
        "RegistrationAST": load_artifact("RegistrationAST"),
        "CallGraph": load_artifact("CallGraph"),
        "LinkMap": load_artifact("LinkMap"),
        "DependencyModel": load_artifact("DependencyModel"),
    for file_id, file_path in sorted(files):
        if file_path:
            print(f"  - {file_path} (id: {file_id})")
    for entity, etype, file_id, file_path in sorted(cluster):
    for entity, etype, file_id, file_path in sorted(cluster):
if __name__ == "__main__":

============================================================
## Inspector-Discovery_v2.py
============================================================

STATUS: FOUND
SIZE  : 16099 bytes
DATE  : 2026-07-08 19:01:57
LINES : 1802

### FIRST 40 LINES
#!/usr/bin/env python3





"""





Inspector-Discovery v2 — семантический Discovery с канонизацией и архитектурным графом.





Объединяет синонимы, фильтрует бэкапы, строит граф зависимостей и определяет главный вход.





"""











import json




### IMPORTS
import json
import re
import sys
from pathlib import Path
from collections import defaultdict, deque

### CLASSES

### FUNCTIONS
def load_artifact(name):
def normalize_entity_name(name):
def find_entities_by_semantic(keywords, entity_map, physical_map):
def collect_entity_evidence(entity_name, artifacts):
def build_capability_cluster(keywords, artifacts):
def main():

### MAIN / OUTPUT / INPUT MARKERS
import json
from pathlib import Path
ROOT = Path.cwd()
def load_artifact(name):
        "PhysicalMap": "Inspector0_PhysicalMap.json",
        "EntityMap": "Inspector1_EntityMap.json",
        "ImportMap": "Inspector2_ImportMap.json",
        "RegistrationAST": "Inspector3_RegistrationAST.json",
        "CallGraph": "Inspector4_CallGraph.json",
        "LinkMap": "LinkMap.json",
        "DependencyModel": "DependencyModel.json",
        "ExecutionRegistry": "A_07_CONFIG/execution_registry.json",
        "GoalsRegistry": "A_07_CONFIG/goals_registry.json",
        "ProjectPassport": "A_07_CONFIG/project_passport.json",
    path = ROOT / filenames.get(name, "")
    if not path.exists():
        return json.loads(path.read_text(encoding="utf-8-sig"))
        file_path = None
                    file_path = item["relative_path"]
        if file_path and re.search(r'(BACKUP|BAK|OLD|COPY|backup|bak|old|copy)', file_path):
                entities.add((name, "class", file_id, file_path))
                entities.add((name, "function", file_id, file_path))
                evidence["links"].add((json.dumps(link, ensure_ascii=False, sort_keys=True), None))
    for entity, etype, file_id, file_path in entities:
        all_files.add((file_id, file_path))
    for entity, etype, file_id, file_path in entities:
            final_entities.add((entity, etype, file_id, file_path))
        "PhysicalMap": load_artifact("PhysicalMap"),
        "EntityMap": load_artifact("EntityMap"),
        "ImportMap": load_artifact("ImportMap"),
        "RegistrationAST": load_artifact("RegistrationAST"),
        "CallGraph": load_artifact("CallGraph"),
        "LinkMap": load_artifact("LinkMap"),
        "DependencyModel": load_artifact("DependencyModel"),
        "ExecutionRegistry": load_artifact("ExecutionRegistry"),
        "GoalsRegistry": load_artifact("GoalsRegistry"),
        "ProjectPassport": load_artifact("ProjectPassport"),
    for file_id, file_path in sorted(files):
        if file_path and not re.search(r'(BACKUP|BAK|OLD|COPY|backup|bak|old|copy)', file_path):
            print(f"  - {file_path} (id: {file_id})")
    for entity, etype, file_id, file_path in sorted(cluster):
    for entity, etype, file_id, file_path in sorted(cluster):
if __name__ == "__main__":

============================================================
## Inspector1_EntityMap.py
============================================================

STATUS: FOUND
SIZE  : 3518 bytes
DATE  : 2026-07-08 00:52:28
LINES : 105

### FIRST 40 LINES
#!/usr/bin/env python3
"""
Inspector 1 — Entity Map v1.3
READ ONLY. Извлекает сущности (классы, функции, переменные) из .py-файлов.
Не делает выводов. Только факты.
"""

import ast
from pathlib import Path
from typing import Dict, List

from BaseInspector import BaseInspector

class Inspector1_EntityMap(BaseInspector):
    SCHEMA = "entity_map"
    SCHEMA_VERSION = "1.3"
    GENERATOR = "Inspector1_EntityMap"
    GENERATOR_VERSION = "1.3"
    TARGET_KIND = "python"

    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        self.total_classes = 0
        self.total_functions = 0
        self.total_variables = 0

    def process_file(self, file_info: Dict) -> Dict:
        file_path = file_info["path"]
        try:
            source = file_path.read_text(encoding='utf-8-sig', errors='ignore')
            tree = ast.parse(source)
        except Exception as e:
            return {"id": file_info["id"], "error": str(e)}

        extractor = EntityExtractor()
        extractor.visit(tree)

        self.total_classes += len(extractor.classes)
        self.total_functions += len(extractor.functions)
        self.total_variables += len(extractor.variables)

### IMPORTS
import ast
from pathlib import Path
from typing import Dict, List
from BaseInspector import BaseInspector
    import sys

### CLASSES
class Inspector1_EntityMap(BaseInspector):
class EntityExtractor(ast.NodeVisitor):

### FUNCTIONS
    def __init__(self, input_path: str, output_path: str):
    def process_file(self, file_info: Dict) -> Dict:
    def _add_statistics(self):
    def __init__(self):
    def visit_ClassDef(self, node):
    def visit_FunctionDef(self, node):
    def visit_Assign(self, node):

### MAIN / OUTPUT / INPUT MARKERS
READ ONLY. Извлекает сущности (классы, функции, переменные) из .py-файлов.
from pathlib import Path
    SCHEMA = "entity_map"
    SCHEMA_VERSION = "1.3"
    GENERATOR_VERSION = "1.3"
    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        file_path = file_info["path"]
            source = file_path.read_text(encoding='utf-8-sig', errors='ignore')
if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "Inspector0_PhysicalMap.json"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "Inspector1_EntityMap.json"
    inspector = Inspector1_EntityMap(input_path, output_path)

============================================================
## Inspector2_ImportMap.py
============================================================

STATUS: FOUND
SIZE  : 2394 bytes
DATE  : 2026-07-08 00:50:23
LINES : 80

### FIRST 40 LINES
#!/usr/bin/env python3
"""
Inspector 2 — Import Map v1.3
READ ONLY. Извлекает импорты из .py-файлов.
Не делает выводов. Только факты.
"""

import ast
from pathlib import Path
from typing import Dict, List

from BaseInspector import BaseInspector

class Inspector2_ImportMap(BaseInspector):
    SCHEMA = "import_map"
    SCHEMA_VERSION = "1.3"
    GENERATOR = "Inspector2_ImportMap"
    GENERATOR_VERSION = "1.3"
    TARGET_KIND = "python"

    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        self.total_imports = 0

    def process_file(self, file_info: Dict) -> Dict:
        file_path = file_info["path"]
        try:
            source = file_path.read_text(encoding='utf-8-sig', errors='ignore')
            tree = ast.parse(source)
        except Exception as e:
            return {"id": file_info["id"], "error": str(e)}

        extractor = ImportExtractor()
        extractor.visit(tree)

        self.total_imports += len(extractor.imports)

        return {
            "id": file_info["id"],
            "imports": extractor.imports,

### IMPORTS
import ast
from pathlib import Path
from typing import Dict, List
from BaseInspector import BaseInspector
    import sys

### CLASSES
class Inspector2_ImportMap(BaseInspector):
class ImportExtractor(ast.NodeVisitor):

### FUNCTIONS
    def __init__(self, input_path: str, output_path: str):
    def process_file(self, file_info: Dict) -> Dict:
    def _add_statistics(self):
    def __init__(self):
    def visit_Import(self, node):
    def visit_ImportFrom(self, node):

### MAIN / OUTPUT / INPUT MARKERS
READ ONLY. Извлекает импорты из .py-файлов.
from pathlib import Path
    SCHEMA = "import_map"
    SCHEMA_VERSION = "1.3"
    GENERATOR_VERSION = "1.3"
    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        file_path = file_info["path"]
            source = file_path.read_text(encoding='utf-8-sig', errors='ignore')
if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "Inspector0_PhysicalMap.json"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "Inspector2_ImportMap.json"
    inspector = Inspector2_ImportMap(input_path, output_path)

============================================================
## Inspector3_RegistrationAST.py
============================================================

STATUS: FOUND
SIZE  : 3514 bytes
DATE  : 2026-07-08 01:03:12
LINES : 102

### FIRST 40 LINES
#!/usr/bin/env python3
"""
Inspector 3 — Registration AST v1.0
READ ONLY. Находит регистрации компонентов через AST (вызовы register, Dispatcher и т.п.).
Не делает выводов. Только факты.
"""

import ast
from pathlib import Path
from typing import Dict, List, Any

from BaseInspector import BaseInspector

class Inspector3_RegistrationAST(BaseInspector):
    SCHEMA = "registration_ast"
    SCHEMA_VERSION = "1.0"
    GENERATOR = "Inspector3_RegistrationAST"
    GENERATOR_VERSION = "1.0"
    TARGET_KIND = "python"

    REGISTRATION_NAMES = {
        'register', 'add_handler', 'register_department', 'register_agent',
        'register_engine', 'register_skill', 'register_service', 'register_module',
        'register_plugin', 'add_route', 'Dispatcher'
    }

    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        self.total_registrations = 0

    def process_file(self, file_info: Dict) -> Dict:
        file_path = file_info["path"]
        try:
            source = file_path.read_text(encoding='utf-8-sig', errors='ignore')
            tree = ast.parse(source)
        except Exception as e:
            return {"id": file_info["id"], "error": str(e)}

        extractor = RegistrationExtractor(self.REGISTRATION_NAMES)
        extractor.visit(tree)

### IMPORTS
import ast
from pathlib import Path
from typing import Dict, List, Any
from BaseInspector import BaseInspector
    import sys

### CLASSES
class Inspector3_RegistrationAST(BaseInspector):
class RegistrationExtractor(ast.NodeVisitor):

### FUNCTIONS
    def __init__(self, input_path: str, output_path: str):
    def process_file(self, file_info: Dict) -> Dict:
    def _add_statistics(self):
    def __init__(self, registration_names: set):
    def visit_Call(self, node):

### MAIN / OUTPUT / INPUT MARKERS
READ ONLY. Находит регистрации компонентов через AST (вызовы register, Dispatcher и т.п.).
from pathlib import Path
    SCHEMA = "registration_ast"
    SCHEMA_VERSION = "1.0"
    GENERATOR_VERSION = "1.0"
    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        file_path = file_info["path"]
            source = file_path.read_text(encoding='utf-8-sig', errors='ignore')
if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "Inspector0_PhysicalMap.json"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "Inspector3_RegistrationAST.json"
    inspector = Inspector3_RegistrationAST(input_path, output_path)

============================================================
## Inspector3_RegistrationMap.py
============================================================

STATUS: FOUND
SIZE  : 2841 bytes
DATE  : 2026-07-08 00:54:25
LINES : 81

### FIRST 40 LINES
#!/usr/bin/env python3
"""
Inspector 3 — Registration Map v1.0
READ ONLY. Находит регистрации компонентов в .py-файлах (паттерны register, Dispatcher и т.п.).
Не делает выводов. Только факты.
"""

import re
from pathlib import Path
from typing import Dict, List

from BaseInspector import BaseInspector

class Inspector3_RegistrationMap(BaseInspector):
    SCHEMA = "registration_map"
    SCHEMA_VERSION = "1.0"
    GENERATOR = "Inspector3_RegistrationMap"
    GENERATOR_VERSION = "1.0"
    TARGET_KIND = "python"

    # Паттерны регистраций (регулярные выражения)
    PATTERNS = [
        r'\bregister\s*\(',
        r'\badd_handler\s*\(',
        r'\bDispatcher\s*\(',
        r'\bregistry\b',
        r'\bfactory\b',
        r'self\.departments\b',
        r'\bregister_department\s*\(',
        r'\badd_route\s*\(',
        r'\bregister_agent\s*\(',
        r'\bregister_engine\s*\(',
        r'\bregister_skill\s*\(',
        r'\bregister_service\s*\(',
        r'\bregister_module\s*\(',
        r'\bregister_plugin\s*\(',
    ]
    # Компилируем регулярки с флагом re.IGNORECASE
    COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in PATTERNS]


### IMPORTS
import re
from pathlib import Path
from typing import Dict, List
from BaseInspector import BaseInspector
    import sys

### CLASSES
class Inspector3_RegistrationMap(BaseInspector):

### FUNCTIONS
    def __init__(self, input_path: str, output_path: str):
    def process_file(self, file_info: Dict) -> Dict:
    def _add_statistics(self):

### MAIN / OUTPUT / INPUT MARKERS
READ ONLY. Находит регистрации компонентов в .py-файлах (паттерны register, Dispatcher и т.п.).
from pathlib import Path
    SCHEMA = "registration_map"
    SCHEMA_VERSION = "1.0"
    GENERATOR_VERSION = "1.0"
    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        file_path = file_info["path"]
            source = file_path.read_text(encoding='utf-8-sig', errors='ignore')
if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "Inspector0_PhysicalMap.json"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "Inspector3_RegistrationMap.json"
    inspector = Inspector3_RegistrationMap(input_path, output_path)

============================================================
## Inspector4_CallGraph.py
============================================================

STATUS: FOUND
SIZE  : 3111 bytes
DATE  : 2026-07-08 01:00:39
LINES : 97

### FIRST 40 LINES
#!/usr/bin/env python3
"""
Inspector 4 — Call Graph v1.0
READ ONLY. Собирает все вызовы функций и методов в .py-файлах (через AST).
Не делает выводов. Только факты.
"""

import ast
from pathlib import Path
from typing import Dict, List

from BaseInspector import BaseInspector

class Inspector4_CallGraph(BaseInspector):
    SCHEMA = "call_graph"
    SCHEMA_VERSION = "1.0"
    GENERATOR = "Inspector4_CallGraph"
    GENERATOR_VERSION = "1.0"
    TARGET_KIND = "python"

    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        self.total_calls = 0

    def process_file(self, file_info: Dict) -> Dict:
        file_path = file_info["path"]
        try:
            source = file_path.read_text(encoding='utf-8-sig', errors='ignore')
            tree = ast.parse(source)
        except Exception as e:
            return {"id": file_info["id"], "error": str(e)}

        extractor = CallExtractor()
        extractor.visit(tree)

        self.total_calls += len(extractor.calls)

        return {
            "id": file_info["id"],
            "calls": extractor.calls,

### IMPORTS
import ast
from pathlib import Path
from typing import Dict, List
from BaseInspector import BaseInspector
    import sys

### CLASSES
class Inspector4_CallGraph(BaseInspector):
class CallExtractor(ast.NodeVisitor):

### FUNCTIONS
    def __init__(self, input_path: str, output_path: str):
    def process_file(self, file_info: Dict) -> Dict:
    def _add_statistics(self):
    def __init__(self):
    def visit_FunctionDef(self, node):
    def visit_ClassDef(self, node):
    def visit_Call(self, node):

### MAIN / OUTPUT / INPUT MARKERS
READ ONLY. Собирает все вызовы функций и методов в .py-файлах (через AST).
from pathlib import Path
    SCHEMA = "call_graph"
    SCHEMA_VERSION = "1.0"
    GENERATOR_VERSION = "1.0"
    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        file_path = file_info["path"]
            source = file_path.read_text(encoding='utf-8-sig', errors='ignore')
if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "Inspector0_PhysicalMap.json"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "Inspector4_CallGraph.json"
    inspector = Inspector4_CallGraph(input_path, output_path)

============================================================
## Inspector5_DependencyGraph.py
============================================================

STATUS: FOUND
SIZE  : 2679 bytes
DATE  : 2026-07-08 01:03:35
LINES : 66

### FIRST 40 LINES
#!/usr/bin/env python3
"""
Inspector 5 — Dependency Graph v1.0
Агрегирует данные из Inspector1-4 и строит граф зависимостей.
READ ONLY. Не делает выводов. Только факты и связи.
"""

import json
from pathlib import Path
from typing import Dict, List, Any

class Inspector5_DependencyGraph:
    def __init__(self, 
                 entity_path: str = "Inspector1_EntityMap.json",
                 import_path: str = "Inspector2_ImportMap.json",
                 registration_path: str = "Inspector3_RegistrationAST.json",
                 call_path: str = "Inspector4_CallGraph.json",
                 output_path: str = "Inspector5_DependencyGraph.json"):
        self.entity_path = Path(entity_path)
        self.import_path = Path(import_path)
        self.registration_path = Path(registration_path)
        self.call_path = Path(call_path)
        self.output_path = Path(output_path)
        self.graph = {
            "nodes": [],
            "edges": []
        }

    def load_json(self, path: Path) -> Dict:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"ERROR: Cannot read {path}: {e}")
            return {}

    def build(self):
        print("Loading data...")
        entities = self.load_json(self.entity_path)
        imports = self.load_json(self.import_path)

### IMPORTS
import json
from pathlib import Path
from typing import Dict, List, Any
    import sys

### CLASSES
class Inspector5_DependencyGraph:

### FUNCTIONS
    def __init__(self, 
    def load_json(self, path: Path) -> Dict:
    def build(self):
    def save(self):

### MAIN / OUTPUT / INPUT MARKERS
READ ONLY. Не делает выводов. Только факты и связи.
import json
from pathlib import Path
                 entity_path: str = "Inspector1_EntityMap.json",
                 import_path: str = "Inspector2_ImportMap.json",
                 registration_path: str = "Inspector3_RegistrationAST.json",
                 call_path: str = "Inspector4_CallGraph.json",
                 output_path: str = "Inspector5_DependencyGraph.json"):
        self.entity_path = Path(entity_path)
        self.import_path = Path(import_path)
        self.registration_path = Path(registration_path)
        self.call_path = Path(call_path)
        self.output_path = Path(output_path)
    def load_json(self, path: Path) -> Dict:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
            print(f"ERROR: Cannot read {path}: {e}")
        entities = self.load_json(self.entity_path)
        imports = self.load_json(self.import_path)
        registrations = self.load_json(self.registration_path)
        calls = self.load_json(self.call_path)
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(self.graph, f, ensure_ascii=False, indent=2)
            print(f"SUCCESS: Graph saved to {self.output_path}")
            print(f"ERROR: Failed to write output: {e}")
if __name__ == "__main__":

============================================================
## Inspector5_LinkMap.py
============================================================

STATUS: FOUND
SIZE  : 5941 bytes
DATE  : 2026-07-08 01:07:47
LINES : 147

### FIRST 40 LINES
#!/usr/bin/env python3
"""
Inspector 5 — Link Map v1.0
READ ONLY. Объединяет факты из предыдущих инспекторов в нормализованный список связей.
Не строит граф. Не делает выводов. Только факты.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any

from BaseInspector import BaseInspector

class Inspector5_LinkMap(BaseInspector):
    SCHEMA = "link_map"
    SCHEMA_VERSION = "1.0"
    GENERATOR = "Inspector5_LinkMap"
    GENERATOR_VERSION = "1.0"
    TARGET_KIND = "python"  # не используется, но оставлен для совместимости

    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        self.links: List[Dict] = []
        self.total_links = 0

    def load_json(self, path: Path) -> Dict:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"ERROR: Cannot load {path}: {e}", file=sys.stderr)
            return {}

    def run(self):
        # Загружаем все артефакты
        physical_map = self.load_json(Path("Inspector0_PhysicalMap.json"))
        entity_map = self.load_json(Path("Inspector1_EntityMap.json"))
        import_map = self.load_json(Path("Inspector2_ImportMap.json"))
        registration_map = self.load_json(Path("Inspector3_RegistrationAST.json"))

### IMPORTS
import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from BaseInspector import BaseInspector
    import sys

### CLASSES
class Inspector5_LinkMap(BaseInspector):

### FUNCTIONS
    def __init__(self, input_path: str, output_path: str):
    def load_json(self, path: Path) -> Dict:
    def run(self):
    def _add_statistics(self):

### MAIN / OUTPUT / INPUT MARKERS
READ ONLY. Объединяет факты из предыдущих инспекторов в нормализованный список связей.
import json
from pathlib import Path
    SCHEMA = "link_map"
    SCHEMA_VERSION = "1.0"
    GENERATOR_VERSION = "1.0"
    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
    def load_json(self, path: Path) -> Dict:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
            print(f"ERROR: Cannot load {path}: {e}", file=sys.stderr)
        physical_map = self.load_json(Path("Inspector0_PhysicalMap.json"))
        entity_map = self.load_json(Path("Inspector1_EntityMap.json"))
        import_map = self.load_json(Path("Inspector2_ImportMap.json"))
        registration_map = self.load_json(Path("Inspector3_RegistrationAST.json"))
        call_graph = self.load_json(Path("Inspector4_CallGraph.json"))
            print("ERROR: One or more input files missing.", file=sys.stderr)
            "schema": self.SCHEMA,
            "schema_version": self.SCHEMA_VERSION,
            "generator_version": self.GENERATOR_VERSION,
            "input": {
                "physical_map": "Inspector0_PhysicalMap.json",
                "entity_map": "Inspector1_EntityMap.json",
                "import_map": "Inspector2_ImportMap.json",
                "registration_map": "Inspector3_RegistrationAST.json",
                "call_graph": "Inspector4_CallGraph.json",
        # Запись выходного JSON
        output = {
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            print(f"ERROR: Failed to write output: {e}", file=sys.stderr)
        print(f"OUTPUT  : {self.output_path}")
if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "Inspector0_PhysicalMap.json"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "Inspector5_LinkMap.json"
    inspector = Inspector5_LinkMap(input_path, output_path)
