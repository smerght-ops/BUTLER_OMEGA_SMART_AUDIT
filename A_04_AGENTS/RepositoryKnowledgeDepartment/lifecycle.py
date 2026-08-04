"""Thread-safe ownership of one RKD instance per normalized project root."""

from pathlib import Path
from threading import RLock

from .runner import RepositoryKnowledgeDepartment


_instances = {}
_lock = RLock()


def get_department(root):
    normalized = Path(root).resolve()
    with _lock:
        department = _instances.get(normalized)
        if department is None:
            department = RepositoryKnowledgeDepartment(normalized)
            _instances[normalized] = department
        return department


def clear_instances():
    """Test-only lifecycle reset; production callers reuse published instances."""
    with _lock:
        _instances.clear()
