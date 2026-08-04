import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_official_launcher_and_runtime_chain_contract():
    contract = json.loads((ROOT / "A_00_ARCHITECTURE/RUNTIME_CONTRACT.json").read_text(encoding="utf-8"))
    assert contract["runtime_status"] == "ACTIVE_PRODUCTION"
    assert contract["exclusive_entry_point_proven"] is True
    assert contract["official_launcher"] == "START_BUTLER_OS.ps1"
    assert contract["official_stop_launcher"] == "STOP_BUTLER_OS.ps1"
    assert "DepartmentExecutionGateway" in contract["runtime_chain"]
    assert "PermissionEngine" in contract["runtime_chain"]


def test_alternative_launchers_classified():
    contract = json.loads((ROOT / "A_00_ARCHITECTURE/RUNTIME_CONTRACT.json").read_text(encoding="utf-8"))
    rows = {row["path"]: row["status"] for row in contract["alternative_launchers"]}
    assert rows["START_BUTLER_RUNTIME_DIAGNOSTIC.bat"] == "DIAGNOSTIC"
    assert all(status != "ACTIVE_PRODUCTION" for status in rows.values())


def test_session_state_created_and_partial_start_rolls_back_owned_processes():
    launcher = (ROOT / "START_BUTLER_OS.ps1").read_text(encoding="utf-8")
    assert "butler.runtime-session.v1" in launcher
    assert "Write-State $state" in launcher
    assert "Stop-OwnedProcesses $state" in launcher
    assert "PARTIAL_START_FAILED" in launcher


def test_stop_uses_session_owned_pids_only():
    stop = (ROOT / "STOP_BUTLER_OS.ps1").read_text(encoding="utf-8")
    assert "active_session.json" in stop
    assert "if (-not $entry.owned)" in stop
    assert "command_token" in stop
    assert "Get-CimInstance Win32_Process -Filter" in stop
    assert "ComfyUI\\main.py" not in stop
    assert "ollama" not in stop.casefold()
