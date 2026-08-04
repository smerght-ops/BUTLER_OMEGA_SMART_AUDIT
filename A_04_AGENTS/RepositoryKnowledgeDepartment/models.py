"""Immutable engineering models for RepositoryKnowledgeDepartment."""

from dataclasses import asdict, dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Tuple


SCHEMA_VERSION = 1


@dataclass(frozen=True)
class Diagnostic:
    source: str
    status: str
    reason: str = ""
    details: Mapping[str, Any] = field(default_factory=dict)
    line: int | None = None
    column: int | None = None

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class FileRecord:
    identifier: str
    name: str
    relative_path: str
    category: str
    size: int
    sha256: str
    encoding: str
    mtime_ns: int
    module: str | None = None
    symbols: Tuple[Mapping[str, Any], ...] = ()
    imports: Tuple[Mapping[str, Any], ...] = ()
    calls: Tuple[Mapping[str, Any], ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class EdgeRecord:
    identifier: str
    source: str
    target: str
    edge_type: str
    source_file: str
    source_line: int | None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class RepositoryIndex:
    schema_version: int
    index_version: str
    repository_version: str
    build_timestamp: str
    source_versions: Mapping[str, Any]
    nodes: Tuple[Mapping[str, Any], ...]
    edges: Tuple[Mapping[str, Any], ...]
    collections: Mapping[str, Tuple[str, ...]]
    diagnostics: Tuple[Mapping[str, Any], ...]
    statistics: Mapping[str, Any]

    @staticmethod
    def immutable_mapping(value):
        return MappingProxyType(dict(value))

    def to_dict(self):
        return {
            "schema_version": self.schema_version,
            "index_version": self.index_version,
            "repository_version": self.repository_version,
            "build_timestamp": self.build_timestamp,
            "source_versions": dict(self.source_versions),
            "nodes": [dict(item) for item in self.nodes],
            "edges": [dict(item) for item in self.edges],
            "collections": {key: list(value) for key, value in self.collections.items()},
            "diagnostics": [dict(item) for item in self.diagnostics],
            "statistics": dict(self.statistics),
        }
