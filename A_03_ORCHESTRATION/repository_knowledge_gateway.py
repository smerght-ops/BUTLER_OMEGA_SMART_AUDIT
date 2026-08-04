"""Approved inter-component client for Repository Knowledge queries."""

from pathlib import Path

from A_03_ORCHESTRATION.permission import DepartmentExecutionGateway
from A_04_AGENTS.RepositoryKnowledgeDepartment.lifecycle import get_department


class RepositoryKnowledgeUnavailableError(RuntimeError):
    """Raised when the canonical repository index cannot serve a query."""


def query_repository(root: Path, operation: str, value=None, filters=None):
    """Execute an RKD operation through the Department permission boundary."""
    department = get_department(Path(root))
    result = DepartmentExecutionGateway().execute(
        department,
        str(value or operation),
        context={
            "repository_knowledge": True,
            "repository_operation": operation,
            "repository_value": value,
            "repository_filters": filters,
        },
    )
    if not isinstance(result, dict) or not result.get("ok"):
        error = result.get("error") if isinstance(result, dict) else "INVALID_RKD_RESPONSE"
        raise RepositoryKnowledgeUnavailableError(f"RKD_UNAVAILABLE: {error}")
    payload = result.get("metadata", {}).get("repository_knowledge")
    if not isinstance(payload, dict) or not payload.get("success"):
        raise RepositoryKnowledgeUnavailableError("RKD_UNAVAILABLE: invalid operation payload")
    return payload


def list_repository_files(root: Path, extension=None):
    """Return canonical indexed relative paths without a fallback scan."""
    filters = {"type": "File"}
    if extension:
        filters["extension"] = extension
    payload = query_repository(root, "list_files", filters=filters)
    return [match["file"] for match in payload.get("data", {}).get("matches", [])]


def get_index(root: Path):
    return query_repository(root, "get_index")


def refresh_index(root: Path):
    return query_repository(root, "refresh_index")


def get_index_status(root: Path):
    return query_repository(root, "get_index_status")
