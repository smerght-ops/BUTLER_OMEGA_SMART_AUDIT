# -*- coding: utf-8 -*-
import re
import subprocess
from pathlib import Path

ROOT = Path.cwd()
CORE = ROOT / "A_04_AGENTS" / "ProjectDocumentationDepartment" / "Core"
FACTS = ROOT / "facts"

BAD = r"A_00_AVARIYKA|A_00_HISTORY|A_99_TEST_DATA|STABLE_BEFORE|_BAK_|_BEFORE_"

GENERATORS = [
    CORE / "ast_parser.py",
    CORE / "ast_call_parser.py",
    CORE / "config_scanner.py",
    CORE / "ast_path_resolver.py",
    CORE / "structural_extractor.py",
    CORE / "evidence_builder.py",
]

def run(cmd):
    p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return p.returncode, p.stdout, p.stderr

def count_bad(path):
    if not path.exists():
        return -1
    txt = path.read_text(encoding="utf-8", errors="replace")
    return len(re.findall(BAD, txt))

def suggest():
    print("-" * 70)
    print("ADVISOR")
    print("-" * 70)

    ev = count_bad(FACTS / "PROJECT_EVIDENCE.json")
    rep = count_bad(ROOT / "ARCHITECTURE_REPORT_V2.md")

    if ev != 0:
        print(f"PROJECT_EVIDENCE : DIRTY ({ev})")
        print("Recommendation  : python evidence_doctor.py rebuild")

    if rep != 0:
        print(f"REPORT           : DIRTY ({rep})")
        print("Recommendation  : python evidence_doctor.py audit")

    if ev == 0 and rep == 0:
        print("STATUS           : HEALTHY")
        print("Recommendation   : No actions required.")

    print("-" * 70)

def main():
    print("=" * 70)
    print("EVIDENCE DOCTOR V1 READONLY")
    print("=" * 70)

    ok = True

    for script in GENERATORS:
        code, out, err = run(["python", str(script)])
        name = script.name
        if code == 0:
            print(f"{name.ljust(28)} OK")
        else:
            print(f"{name.ljust(28)} FAIL")
            print(err.strip())
            ok = False
            break

    evidence = FACTS / "PROJECT_EVIDENCE.json"
    report = ROOT / "ARCHITECTURE_REPORT_V2.md"
    audit = ROOT / "run_audit_v2.py"

    ev_bad = count_bad(evidence)
    rep_bad = count_bad(report)

    audit_txt = audit.read_text(encoding="utf-8", errors="replace") if audit.exists() else ""
    audit_ok = "PROJECT_EVIDENCE.json" in audit_txt and "PROJECT_EVIDENCE_LITE.json" not in audit_txt

    print("-" * 70)
    print(f"PROJECT_EVIDENCE.json      {'CLEAN' if ev_bad == 0 else 'DIRTY'} ({ev_bad})")
    print(f"ARCHITECTURE_REPORT_V2.md  {'CLEAN' if rep_bad == 0 else 'DIRTY'} ({rep_bad})")
    print(f"run_audit_v2.py source     {'OK' if audit_ok else 'FAIL'}")
    print("-" * 70)

    if ok and ev_bad == 0 and rep_bad == 0 and audit_ok:
        print("STATUS: HEALTHY")
    else:
        print("STATUS: DIRTY")

    suggest()

    print("=" * 70)

def dispatch():

    import sys

    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "status"

    if cmd == "status":
        main()

    elif cmd == "rebuild":
        for s in GENERATORS:
            print(f"RUN {s.name}")
            subprocess.run(["python", str(s)], cwd=ROOT)

    elif cmd == "audit":
        subprocess.run(["python", str(ROOT / "run_audit_v2.py")], cwd=ROOT)

    elif cmd == "plan":
        print("=" * 70)
        print("EVIDENCE DOCTOR DRY RUN")
        print("=" * 70)
        print("[1] Rebuild evidence")
        print("[2] Run architecture audit")
        print("[3] Check PROJECT_EVIDENCE.json")
        print("[4] Check ARCHITECTURE_REPORT_V2.md")
        print("[5] No files will be modified")
        print("=" * 70)

    elif cmd == "apply":
        print("=" * 70)
        print("SAFE ACTIONS")
        print("=" * 70)
        print("Planned actions:")
        print("  - Rebuild evidence")
        print("  - Run architecture audit")
        print("")
        print("Waiting for confirmation...")
        print("=" * 70)

    elif cmd == "confirm":
        print("=" * 70)
        print("CONFIRMED")
        print("=" * 70)

        for s in GENERATORS:
            print(f"RUN {s.name}")
            subprocess.run(["python", str(s)], cwd=ROOT)

        subprocess.run(["python", str(ROOT / "run_audit_v2.py")], cwd=ROOT)

        print("")
        main()

    else:
        print("Unknown command:", cmd)
        print("Available: status | rebuild | audit | plan | apply | confirm")


if __name__ == "__main__":
    dispatch()
