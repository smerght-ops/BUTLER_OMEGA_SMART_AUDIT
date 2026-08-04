# -*- coding: utf-8 -*-
"""Repository Knowledge Department — engineering knowledge service for Butler Omega.

All operations are read-only. The department reads PROJECT_SCOPE.yaml,
system_manifest.json and the project AST tree to build an internal index that
powers fast queries without repeated full-tree traversal.
"""
from A_04_AGENTS.RepositoryKnowledgeDepartment.runner import RepositoryKnowledgeDepartment

__all__ = ["RepositoryKnowledgeDepartment"]
