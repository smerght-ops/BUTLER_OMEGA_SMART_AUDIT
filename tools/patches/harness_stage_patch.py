from pathlib import Path

path = Path("A_03_ORCHESTRATION/butler_harness.py")

code = path.read_text(encoding="utf-8")

old = '''loader.commit_proof("4.24_active_sync_proof", "RUNNING_AUTOMATICALLY")'''

new = '''loader.commit_proof("4.24_active_sync_proof", "RUNNING_AUTOMATICALLY")
                    loader.evaluate_stage_transitions()'''

if old in code:
    path.write_text(
        code.replace(old, new),
        encoding="utf-8"
    )
    print("OK")
else:
    print("TARGET_NOT_FOUND")
