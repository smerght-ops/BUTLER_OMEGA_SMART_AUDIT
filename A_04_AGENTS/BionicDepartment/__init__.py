# -*- coding: utf-8 -*-
"""Bionic Department — General Agent Worker / Builder for Butler Omega Smart.

Bionic is an untrusted intelligent Worker/Builder.
Butler remains the trusted orchestrator + policy owner + acceptance authority.

Key principles:
- Bionic produces artifacts in a bounded staging workspace only.
- Bionic self-report (PASS/Done/Successfully) is NOT evidence.
- Butler independently validates all artifacts via EvidenceGate.
- Lifecycle: PRODUCED → DELIVERED → VERIFIED → SYSTEM_ACCEPTANCE.
"""
