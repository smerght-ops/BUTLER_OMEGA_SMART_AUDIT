from fnmatch import fnmatch

from .base import Inspector


class WhitelistInspector(Inspector):
    inspector_id = "whitelist"

    def run(self, context, policy):
        allowed = policy.get("whitelist", {}).get("paths", [])
        warnings = []
        for item in context.files:
            if any(fnmatch(item.path, rule) for rule in allowed):
                warnings.append(self.finding(
                    "WHITELIST_MATCH", "INFO", "Объект присутствует в whitelist; критические проверки сохранены.",
                    "Дополнительные действия не требуются.", item.path,
                ))
        return [], warnings
