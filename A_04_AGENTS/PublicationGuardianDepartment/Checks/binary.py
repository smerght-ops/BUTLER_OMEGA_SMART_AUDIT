import mimetypes
from pathlib import PurePosixPath

from ..Contracts.models import Severity, Violation
from .base import Inspector, safe_digest


class BinaryInspector(Inspector):
    inspector_id = "binary"
    cache_per_file = True

    def run(self, context, policy):
        violations, warnings = [], []
        binary_policy = policy.get("binary", {})
        allowed = {ext.casefold() for ext in binary_policy.get("allowed_extensions", [])}
        denied = {ext.casefold() for ext in binary_policy.get("denied_extensions", [])}
        max_size = int(binary_policy.get("max_size_bytes", 10485760))
        for item in context.files:
            extension = PurePosixPath(item.path).suffix.casefold()
            declared_mime = mimetypes.guess_type(item.path)[0] or "application/octet-stream"
            detected_mime, dangerous = _detect_content_type(item.content)
            metadata = (f"declared_mime={declared_mime}; detected_mime={detected_mime}; "
                        f"ext={extension or '<none>'}; size={len(item.content)}; sha256={safe_digest(item.content)}")
            mismatch = detected_mime not in {"unknown", declared_mime} and declared_mime != "application/octet-stream"
            if extension in denied or len(item.content) > max_size or dangerous or mismatch:
                violations.append(Violation(
                    "BINARY_DENIED", Severity.BLOCK, "Бинарный объект запрещён политикой.",
                    "Удалите объект или согласуйте безопасное правило политики.", item.path, metadata,
                    self.inspector_id,
                ))
            elif item.text is None and extension not in allowed:
                warnings.append(Violation(
                    "BINARY_UNKNOWN", Severity(binary_policy.get("unknown_severity", "WARNING")),
                    "Обнаружен неизвестный бинарный формат.",
                    "Проверьте происхождение файла и явно разрешите тип в политике.", item.path, metadata,
                    self.inspector_id,
                ))
        return violations, warnings


def _detect_content_type(content: bytes):
    signatures = (
        (b"MZ", "application/x-dosexec", True),
        (b"\x7fELF", "application/x-executable", True),
        (b"%PDF-", "application/pdf", False),
        (b"\x89PNG\r\n\x1a\n", "image/png", False),
        (b"\xff\xd8\xff", "image/jpeg", False),
        (b"GIF87a", "image/gif", False),
        (b"GIF89a", "image/gif", False),
        (b"PK\x03\x04", "application/zip", False),
    )
    for signature, mime, dangerous in signatures:
        if content.startswith(signature):
            return mime, dangerous
    return "unknown", False
