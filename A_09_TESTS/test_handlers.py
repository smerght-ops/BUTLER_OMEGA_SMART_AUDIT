from pathlib import Path
import sys

# ---- Butler project root bootstrap ----
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
# ---------------------------------------

from A_03_HANDLERS.registry import registry

TEST_DIR = PROJECT_ROOT / "A_99_TEST_DATA"

ok = 0
failed = 0

print("=" * 60)
print("BUTLER HANDLER TEST SUITE")
print("=" * 60)

if not TEST_DIR.exists():
    print(f"[FATAL] Missing directory: {TEST_DIR}")
    sys.exit(1)

for path in sorted(TEST_DIR.iterdir()):
    if not path.is_file():
        continue

    handler = registry.get_handler(path)

    if handler is None:
        print(f"[FAIL] {path.name:25} -> NO HANDLER")
        failed += 1
        continue

    try:
        result = handler.extract(path)

        if result.get("success", False):
            txt = str(result.get("text", "") or "")
            print(f"[ OK ] {path.name:25} {type(handler).__name__:20} len={len(txt)}")
            ok += 1
        else:
            print(f"[FAIL] {path.name:25} {type(handler).__name__:20} success=False")
            failed += 1

    except Exception as e:
        print(f"[FAIL] {path.name:25} {type(handler).__name__:20} {e}")
        failed += 1

print("=" * 60)
print(f"SUCCESS : {ok}")
print(f"FAILED  : {failed}")
print("=" * 60)

sys.exit(0 if failed == 0 else 1)