from .base import Inspector, patterns


class PrivacyInspector(Inspector):
    inspector_id = "privacy"
    cache_per_file = True

    def run(self, context, policy):
        violations, warnings = [], []
        for item in context.files:
            if item.text is None:
                continue
            for rule_id, regex, severity in patterns(policy, "privacy_patterns"):
                for match in regex.finditer(item.text):
                    finding = self.finding(
                        f"PRIVACY_{rule_id.upper()}", severity, f"Обнаружены конфиденциальные данные: {rule_id}.",
                        "Удалите или обезличьте данные и подтвердите право на публикацию.", item.path, match.group(0),
                    )
                    (warnings if severity in {"INFO", "WARNING", "HIGH"} else violations).append(finding)
        return violations, warnings
