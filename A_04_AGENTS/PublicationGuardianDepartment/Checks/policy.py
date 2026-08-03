from fnmatch import fnmatch

from .base import Inspector


class PolicyInspector(Inspector):
    inspector_id = "policy"

    def run(self, context, policy):
        findings, warnings = [], []
        rules = sorted(policy.get("rules", []), key=lambda item: item.get("priority", 0), reverse=True)
        for item in context.files:
            for rule in rules:
                if not fnmatch(item.path, rule.get("path", "*")):
                    continue
                category = rule.get("category")
                if category == "DENY":
                    findings.append(self.finding(
                        f"POLICY_{rule['id']}", "BLOCK", "Путь запрещён политикой публикации.",
                        rule.get("recommendation", "Удалите объект из публикации."), item.path,
                    ))
                elif category == "WARNING":
                    warnings.append(self.finding(
                        f"POLICY_{rule['id']}", "WARNING", "Путь требует дополнительной проверки.",
                        rule.get("recommendation", "Проверьте объект перед публикацией."), item.path,
                    ))
        required = set(policy.get("required_inspectors", []))
        missing = required.difference(context.registered_inspectors)
        for inspector_id in sorted(missing):
            findings.append(self.finding(
                "REQUIRED_INSPECTOR_MISSING", "BLOCK", f"Обязательный инспектор недоступен: {inspector_id}.",
                "Восстановите обязательный инспектор и повторите проверку.",
            ))
        return findings, warnings
