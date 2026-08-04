"""Specialized architectural graph view over the canonical RKD index."""

from pathlib import Path

from A_03_ORCHESTRATION.repository_knowledge_gateway import get_index


def build_architectural_graph(root=None):
    project_root = Path(root or Path(__file__).resolve().parents[1]).resolve()
    payload = get_index(project_root)
    index = payload["data"]
    return {
        "index_version": index["index_version"],
        "repository_version": index["repository_version"],
        "nodes": index["nodes"],
        "edges": index["edges"],
        "source": "RepositoryKnowledgeDepartment",
    }


def find_import_targets(target, root=None):
    graph = build_architectural_graph(root)
    node_by_id = {node["identifier"]: node for node in graph["nodes"]}
    matches = []
    for edge in graph["edges"]:
        destination = node_by_id.get(edge.get("target"), {})
        label = destination.get("module") or destination.get("name") or ""
        if target.casefold() in str(label).casefold():
            matches.append(edge)
    return matches
