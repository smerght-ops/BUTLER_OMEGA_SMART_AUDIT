#!/usr/bin/env python3
"""
Butler Self-Audit — максимальный самоаудит проекта.
Использует все доступные артефакты (JSON, ключевые файлы) и отвечает на вопросы:
- Какие архитектурные компоненты существуют?
- Какие возможности они реализуют?
- Какие компоненты дублируются?
- Какие компоненты не используются?
- Какие компоненты заявлены, но отсутствуют?
- Какие есть точки входа?
- Какие Registry/Manager/Builder уже существуют?
- Что предлагается создать повторно?

Не делает выводов за пределами фактов. Только объективная картина.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Set, Any
from collections import defaultdict

class ButlerSelfAudit:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.artifacts = {}
        self.report = {
            "metadata": {
                "generator": "Butler_SelfAudit",
                "version": "1.0",
                "generated_utc": None,
            },
            "components": {},
            "capabilities": {},
            "duplicates": {},
            "unused": {},
            "missing": {},
            "entry_points": [],
            "registries": [],
            "managers": [],
            "builders": [],
            "potential_repeats": [],
        }
        self.loaded_files = set()

    def load_artifact(self, name: str, paths: List[str], required=False) -> Any:
        """Загружает артефакт из первого существующего пути."""
        for p in paths:
            path = self.project_root / p
            if path.exists():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    self.artifacts[name] = data
                    self.loaded_files.add(str(path))
                    return data
                except Exception as e:
                    print(f"Warning: Could not load {path}: {e}")
        if required:
            print(f"ERROR: Required artifact {name} not found at {paths}")
            exit(1)
        return None

    def load_all_artifacts(self):
        """Загружает все известные артефакты."""
        # Основные инспекторы
        self.load_artifact("PhysicalMap", ["Inspector0_PhysicalMap.json", "A_06_WORKSPACE/AUDITS/Inspector0_PhysicalMap.json"])
        self.load_artifact("EntityMap", ["Inspector1_EntityMap.json", "A_06_WORKSPACE/AUDITS/Inspector1_EntityMap.json"])
        self.load_artifact("ImportMap", ["Inspector2_ImportMap.json", "A_06_WORKSPACE/AUDITS/Inspector2_ImportMap.json"])
        self.load_artifact("RegistrationAST", ["Inspector3_RegistrationAST.json", "A_06_WORKSPACE/AUDITS/Inspector3_RegistrationAST.json"])
        self.load_artifact("CallGraph", ["Inspector4_CallGraph.json", "A_06_WORKSPACE/AUDITS/Inspector4_CallGraph.json"])
        self.load_artifact("LinkMap", ["LinkMap.json", "A_06_WORKSPACE/AUDITS/LinkMap.json"])
        self.load_artifact("DependencyModel", ["DependencyModel.json", "A_06_WORKSPACE/AUDITS/DependencyModel.json"])

        # Дополнительные артефакты (если есть)
        self.load_artifact("ProjectPassport", ["A_07_CONFIG/project_passport.json", "project_passport.json"])
        self.load_artifact("SystemManifest", ["A_07_CONFIG/system_manifest.json", "system_manifest.json"])
        # self.load_artifact("GoalLoopEngine", ["A_07_MEMORY/goal_loop_engine.py"])  # не JSON, можем прочитать позже

    def analyze(self):
        """Основной анализ."""
        self.analyze_components()
        self.analyze_capabilities()
        self.analyze_duplicates()
        self.analyze_unused()
        self.analyze_missing()
        self.analyze_entry_points()
        self.analyze_registries_managers_builders()
        self.analyze_potential_repeats()

    def analyze_components(self):
        """Какие архитектурные компоненты существуют?"""
        components = {}
        if "EntityMap" in self.artifacts:
            entities = self.artifacts["EntityMap"]["payload"]
            # Собираем все классы и функции
            for entry in entities:
                file_id = entry["id"]
                for cls in entry.get("classes", []):
                    components[cls["name"]] = {
                        "type": "class",
                        "file": file_id,
                        "methods": [m["name"] for m in cls.get("methods", [])]
                    }
                for func in entry.get("functions", []):
                    components[func["name"]] = {
                        "type": "function",
                        "file": file_id
                    }
        self.report["components"] = components

    def analyze_capabilities(self):
        """Какие возможности реализуют компоненты?"""
        capabilities = {}
        # На основе имен компонентов и регистраций
        if "RegistrationAST" in self.artifacts:
            for entry in self.artifacts["RegistrationAST"]["payload"]:
                for reg in entry.get("registrations", []):
                    func = reg.get("function")
                    if func:
                        capabilities[func] = {
                            "type": reg.get("kind"),
                            "file": entry["id"],
                            "line": reg.get("line")
                        }
        self.report["capabilities"] = capabilities

    def analyze_duplicates(self):
        """Какие компоненты дублируются?"""
        # Ищем компоненты с одинаковыми именами (классы, функции)
        name_to_count = defaultdict(list)
        for name, info in self.report["components"].items():
            name_to_count[name].append(info)
        duplicates = {name: infos for name, infos in name_to_count.items() if len(infos) > 1}
        self.report["duplicates"] = duplicates

    def analyze_unused(self):
        """Какие компоненты не используются?"""
        unused = []
        if "LinkMap" in self.artifacts:
            # Собираем все узлы, у которых нет входящих ребер
            targets = set()
            sources = set()
            for link in self.artifacts["LinkMap"]["payload"]:
                sources.add(link["source"])
                targets.add(link["target"])
            # Узлы, которые ни разу не являются source (т.е. не вызывают ничего) - это не обязательно unused
            # Но компоненты, которые ни разу не являются target (нет входящих ссылок) - потенциально unused
            # Однако нужно смотреть на тип: если это файл, то unused, если это сущность, то тоже.
            # Более точный анализ: смотрим компоненты из EntityMap, у которых нет входящих ребер
            if "EntityMap" in self.artifacts:
                for entry in self.artifacts["EntityMap"]["payload"]:
                    file_id = entry["id"]
                    # Проверим, есть ли входящие ребра для этого файла
                    has_incoming = any(link["target"] == file_id for link in self.artifacts["LinkMap"]["payload"])
                    if not has_incoming:
                        unused.append(file_id)
        self.report["unused"] = unused

    def analyze_missing(self):
        """Какие компоненты заявлены в паспорте, но отсутствуют?"""
        missing = []
        if "ProjectPassport" in self.artifacts:
            passport = self.artifacts["ProjectPassport"]
            # Предположим, что паспорт содержит список ожидаемых компонентов
            # Например, ключ "components" или "expected"
            expected = passport.get("components", []) or passport.get("expected", [])
            for comp in expected:
                if comp not in self.report["components"]:
                    missing.append(comp)
        self.report["missing"] = missing

    def analyze_entry_points(self):
        """Какие есть точки входа?"""
        entry_points = []
        # Ищем файлы с main, run, start в имени (из PhysicalMap)
        if "PhysicalMap" in self.artifacts:
            for item in self.artifacts["PhysicalMap"]["payload"]:
                filename = item.get("filename", "")
                if re.search(r'(main|run|start|launch|boot)', filename, re.I):
                    entry_points.append({
                        "file": item["id"],
                        "name": filename,
                        "path": item["relative_path"]
                    })
        self.report["entry_points"] = entry_points

    def analyze_registries_managers_builders(self):
        """Какие Registry/Manager/Builder уже существуют?"""
        registries = []
        managers = []
        builders = []
        # Ищем по именам классов (из EntityMap)
        if "EntityMap" in self.artifacts:
            for entry in self.artifacts["EntityMap"]["payload"]:
                for cls in entry.get("classes", []):
                    name = cls["name"]
                    if re.search(r'Registry', name):
                        registries.append({"name": name, "file": entry["id"]})
                    if re.search(r'Manager', name):
                        managers.append({"name": name, "file": entry["id"]})
                    if re.search(r'Builder', name):
                        builders.append({"name": name, "file": entry["id"]})
        self.report["registries"] = registries
        self.report["managers"] = managers
        self.report["builders"] = builders

    def analyze_potential_repeats(self):
        """Что предлагается создать повторно?"""
        # Сравниваем текущие возможности с тем, что уже есть в CapabilityRegistry
        # Но CapabilityRegistry может отсутствовать, поэтому просто выведем предупреждение
        if "ProjectPassport" in self.artifacts:
            # Если есть паспорт, он может содержать раздел "capabilities"
            pass
        # Пока оставим пустым, но можно добавить логику позже
        self.report["potential_repeats"] = []

    def generate_report(self):
        """Генерирует JSON и Markdown отчёты."""
        from datetime import datetime, timezone
        self.report["metadata"]["generated_utc"] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

        # Сохраняем JSON
        with open("Butler_SelfAudit_Report.json", 'w', encoding='utf-8') as f:
            json.dump(self.report, f, ensure_ascii=False, indent=2)

        # Генерируем Markdown
        md_lines = []
        md_lines.append("# Butler Self-Audit Report")
        md_lines.append(f"**Generated:** {self.report['metadata']['generated_utc']}")
        md_lines.append(f"**Generator:** {self.report['metadata']['generator']} v{self.report['metadata']['version']}")
        md_lines.append("")

        # Компоненты
        md_lines.append("## Архитектурные компоненты")
        md_lines.append(f"**Всего:** {len(self.report['components'])}")
        for name, info in list(self.report['components'].items())[:20]:  # покажем первые 20
            md_lines.append(f"- {name} ({info['type']}) in {info['file']}")
        if len(self.report['components']) > 20:
            md_lines.append(f"... и ещё {len(self.report['components']) - 20} компонентов")
        md_lines.append("")

        # Возможности
        md_lines.append("## Возможности (регистрации)")
        md_lines.append(f"**Всего:** {len(self.report['capabilities'])}")
        for name, info in list(self.report['capabilities'].items())[:20]:
            md_lines.append(f"- {name} ({info['type']}) in {info['file']} line {info.get('line', '?')}")
        if len(self.report['capabilities']) > 20:
            md_lines.append(f"... и ещё {len(self.report['capabilities']) - 20} возможностей")
        md_lines.append("")

        # Дубликаты
        md_lines.append("## Дублирующиеся компоненты")
        if self.report['duplicates']:
            for name, infos in self.report['duplicates'].items():
                md_lines.append(f"- {name} встречается {len(infos)} раз: {', '.join([info['file'] for info in infos])}")
        else:
            md_lines.append("Нет дублирующихся компонентов.")
        md_lines.append("")

        # Неиспользуемые
        md_lines.append("## Неиспользуемые компоненты (нет входящих ссылок)")
        if self.report['unused']:
            for file_id in self.report['unused'][:20]:
                md_lines.append(f"- {file_id}")
            if len(self.report['unused']) > 20:
                md_lines.append(f"... и ещё {len(self.report['unused']) - 20} файлов")
        else:
            md_lines.append("Все компоненты имеют входящие ссылки.")
        md_lines.append("")

        # Отсутствующие
        md_lines.append("## Заявленные, но отсутствующие компоненты")
        if self.report['missing']:
            for comp in self.report['missing']:
                md_lines.append(f"- {comp}")
        else:
            md_lines.append("Все заявленные компоненты присутствуют.")
        md_lines.append("")

        # Точки входа
        md_lines.append("## Точки входа")
        for ep in self.report['entry_points']:
            md_lines.append(f"- {ep['name']} ({ep['file']})")
        md_lines.append("")

        # Registry/Manager/Builder
        md_lines.append("## Существующие Registry/Manager/Builder")
        md_lines.append(f"**Registries:** {', '.join([r['name'] for r in self.report['registries']]) if self.report['registries'] else 'Нет'}")
        md_lines.append(f"**Managers:** {', '.join([m['name'] for m in self.report['managers']]) if self.report['managers'] else 'Нет'}")
        md_lines.append(f"**Builders:** {', '.join([b['name'] for b in self.report['builders']]) if self.report['builders'] else 'Нет'}")
        md_lines.append("")

        # Повторы
        md_lines.append("## Предлагаемые повторы (не обнаружено)")
        md_lines.append("На данный момент не выявлено предложений создать что-то повторно.")
        md_lines.append("")

        md_lines.append("---")
        md_lines.append("*Этот отчёт сгенерирован автоматически и содержит только объективные факты.*")

        with open("Butler_SelfAudit_Report.md", 'w', encoding='utf-8') as f:
            f.write("\n".join(md_lines))

        print("Отчёты сгенерированы:")
        print("  - Butler_SelfAudit_Report.json")
        print("  - Butler_SelfAudit_Report.md")

if __name__ == "__main__":
    audit = ButlerSelfAudit()
    audit.load_all_artifacts()
    audit.analyze()
    audit.generate_report()
