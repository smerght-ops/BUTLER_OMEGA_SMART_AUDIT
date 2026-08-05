# -*- coding: utf-8 -*-

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
CORE = Path(__file__).resolve().parent
DISCOVERY = CORE / "Discovery"
SCANNERS = CORE / "Scanners"

for p in (DISCOVERY, SCANNERS):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from engineering_evidence import EngineeringEvidence
from engineering_evidence_collection import EngineeringEvidenceCollection

from object_merge import ObjectMerge
from conflict_resolution import ConflictResolution
from source_priority import SourcePriority
from evidence_consolidation import EvidenceConsolidation

from passport_scanner import PassportScanner
from registry_scanner import RegistryScanner
from project_state_scanner import ProjectStateScanner
from goals_scanner import GoalsScanner
from execution_scanner import ExecutionScanner
from history_scanner import HistoryScanner
from ledger_scanner import LedgerScanner
from audit_scanner import AuditScanner
from reports_scanner import ReportsScanner
from observations_scanner import RollbackScanner
from snapshot_scanner import SnapshotScanner
from harness_scanner import HarnessScanner
from services_scanner import ServicesScanner


class EngineeringPipeline:

    def __init__(self):
        self.project_root = ROOT
        self.collection = EngineeringEvidenceCollection()

    def _add_dict_object(self, row, source_name):
        e = EngineeringEvidence()
        e.object_id = str(row.get("id") or row.get("name") or row.get("type") or source_name)
        e.object_name = str(row.get("name") or row.get("type") or source_name)
        e.object_type = str(row.get("type") or source_name)
        e.source = str(row.get("source") or source_name)
        e.value = row
        self.collection.add(e)

    def collect(self):
        scan_jobs = [
            ("PASSPORT", PassportScanner(), self.project_root / "A_07_CONFIG" / "project_passport.json"),
            ("REGISTRY", RegistryScanner(), self.project_root / "A_07_CONFIG" / "project_registry.json"),
            ("PROJECT_STATE", ProjectStateScanner(), self.project_root / "A_07_CONFIG" / "project_state.json"),
            ("GOALS", GoalsScanner(), self.project_root / "A_07_CONFIG" / "goals_registry.json"),
            ("EXECUTION", ExecutionScanner(), self.project_root / "A_07_MEMORY" / "execution_registry.json"),
            ("HISTORY", HistoryScanner(), None),
            ("LEDGER", LedgerScanner(), self.project_root / "A_08_LOGS" / "PROJECT_LEDGER.txt"),
            ("AUDIT", AuditScanner(), None),
            ("REPORTS", ReportsScanner(), self.project_root / "A_06_WORKSPACE" / "reports"),
            ("OBSERVATIONS", RollbackScanner(), self.project_root / "A_08_LOGS" / "OBSERVATIONS.jsonl"),

            ("SNAPSHOT", SnapshotScanner(), self.project_root / "A_00_SNAPSHOTS"),
            ("HARNESS", HarnessScanner(), None),
            ("SERVICES", ServicesScanner(), None),
        ]

        for source_name, scanner, arg in scan_jobs:
            try:
                rows = scanner.scan() if arg is None else scanner.scan(arg)
                for row in rows:
                    if isinstance(row, dict):
                        self._add_dict_object(row, source_name)
            except Exception as ex:
                self._add_dict_object({
                    "type": "SCAN_ERROR",
                    "name": source_name,
                    "source": source_name,
                    "error": str(ex),
                }, "SCAN_ERROR")

        return self.collection

    def execute(self):
        self.collect()

        priority = SourcePriority().resolve(self.collection)
        catalog = ObjectMerge().merge(priority)
        catalog = ConflictResolution().resolve(catalog)

        return EvidenceConsolidation().consolidate(catalog, priority)
