# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List


@dataclass
class EngineeringEvidence:
    """
    Universal engineering evidence object.

    Represents one verified observation collected
    by PROJECT_DOCUMENTATION_DEPARTMENT.

    Read-only.
    """

    source: str = ""
    object_type: str = ""
    object_name: str = ""

    discovery_method: str = ""

    evidence: List[str] = field(default_factory=list)

    confidence: int = 0

    status: str = "DISCOVERED"

    notes: str = ""
