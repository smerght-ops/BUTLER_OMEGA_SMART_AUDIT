# -*- coding: utf-8 -*-
import sys
import ast
import json
import os
from pathlib import Path

# Подключаем локальный scope_loader
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))
from scope_loader import is_allowed

ROOT = Path.cwd()
OUTPUT_FILE = ROOT / "PROJECT_FACTS_IMPORTS.json"

def parse_file(filepath):
    # utf-8-sig автоматически съедает маркер U+FEFF (BOM), если он есть
    try:
        content = filepath.read_text(encoding="utf-8-sig")
        tree = ast.parse(content, filename=str(filepath))
        
        imports = []
        from_imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module if node.module else ""
                names = [alias.name for alias in node.names]
                from_imports.append({"module": module, "names": names})
                
        return {
            "file": filepath.relative_to(ROOT).as_posix(),
            "imports": imports,
            "from_imports": from_imports,
            "errors": []
        }
    except SyntaxError as e:
        return {
            "file": filepath.relative_to(ROOT).as_posix(),
            "imports": [],
            "from_imports": [],
            "errors": [f"SyntaxError: {e}"]
        }
    except Exception as e:
        return {
            "file": filepath.relative_to(ROOT).as_posix(),
            "imports": [],
            "from_imports": [],
            "errors": [f"Error: {e}"]
        }

def main():
    print("Запуск AST-парсера (интеграция scope_loader v1.0)...")
    results = []
    
    # Оставляем ключ для обратной совместимости формата,
    # но саму фильтрацию теперь делает scope_loader
    excluded_zones = ["Filtered by scope_loader"] 
    
    for root, dirs, files in os.walk(ROOT):
        for file in files:
            if not file.endswith(".py"):
                continue
                
            full_path = Path(root) / file
            rel_path = full_path.relative_to(ROOT).as_posix()
            
            # Единая точка принятия решений
            if is_allowed(rel_path):
                results.append(parse_file(full_path))

    final_data = {
        "excluded_zones": excluded_zones,
        "python_imports": results
    }

    OUTPUT_FILE.write_text(json.dumps(final_data, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print("="*70)
    print("AST PARSER READY")
    print("="*70)
    print(f"Обработано рабочих файлов: {len(results)}")
    print(f"Результат сохранен в: {OUTPUT_FILE.name}")

if __name__ == "__main__":
    main()
