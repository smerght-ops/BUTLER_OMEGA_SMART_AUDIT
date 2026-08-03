from pathlib import PurePosixPath

from .base import Inspector


class ConfigurationInspector(Inspector):
    inspector_id = "configuration"
    cache_per_file = True

    def run(self, context, policy):
        findings = []
        denied = tuple(item.casefold() for item in policy.get("configuration", {}).get("denied_names", []))
        for item in context.files:
            name = PurePosixPath(item.path).name.casefold()
            if any(self._matches(name, rule) for rule in denied):
                findings.append(self.finding(
                    "CONFIGURATION_FILE", "BLOCK", "Конфигурационный файл запрещён политикой.",
                    "Удалите файл из объекта публикации и передавайте шаблон без значений.", item.path,
                ))
        return findings, []

    @staticmethod
    def _matches(name, rule):
        return name == rule or (rule.endswith(".*") and name.startswith(rule[:-1]))
