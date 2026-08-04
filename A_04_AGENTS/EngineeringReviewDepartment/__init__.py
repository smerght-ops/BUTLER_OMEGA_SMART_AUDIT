# -*- coding: utf-8 -*-
"""Engineering Review Department — read-only engineering verification system.

This department performs a complete engineering review of project changes
without modifying any files. All checks are analysis-only.
"""

from .runner import EngineeringReviewDepartment

__all__ = ["EngineeringReviewDepartment"]
