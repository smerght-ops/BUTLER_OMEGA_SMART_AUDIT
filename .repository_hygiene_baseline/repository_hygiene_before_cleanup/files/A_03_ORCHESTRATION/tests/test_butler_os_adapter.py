# -*- coding: utf-8 -*-

from A_03_ORCHESTRATION.butler_os_adapter import ButlerOSAdapter


adapter = ButlerOSAdapter()

print("[TEST] memory_summary")
print(adapter.memory_summary()[:200])

print("[TEST] skills_summary")
print(adapter.skills_summary()[:200])

print("[TEST] episodes_summary")
print(adapter.episodes_summary()[:200])

print("[TEST] full_summary")

data = adapter.full_summary()

assert isinstance(data, dict)

assert "memory" in data
assert "skills" in data
assert "episodes" in data

print("[OK] ADAPTER TEST PASSED")
