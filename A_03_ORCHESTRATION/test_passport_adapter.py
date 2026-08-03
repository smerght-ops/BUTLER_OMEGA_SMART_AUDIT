from A_03_ORCHESTRATION.butler_os_adapter import ButlerOSAdapter
import json

adapter = ButlerOSAdapter()

print("=" * 60)
print("PROJECT IDENTITY")
print("=" * 60)
print(json.dumps(adapter.project_identity(), indent=2, ensure_ascii=False))

print()
print("=" * 60)
print("CURRENT STAGE")
print("=" * 60)
print(adapter.current_stage())

print()
print("=" * 60)
print("FROZEN MODULES")
print("=" * 60)
print(json.dumps(adapter.frozen_modules(), indent=2, ensure_ascii=False))

print()
print("=" * 60)
print("PASSPORT SUMMARY")
print("=" * 60)
print(json.dumps(adapter.passport_summary(), indent=2, ensure_ascii=False))
