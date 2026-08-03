from A_03_ORCHESTRATION.butler_harness import ButlerHarness

h = ButlerHarness()

r = h.execute(
    department_name="TEST",
    task="hello",
    executor=lambda: {"ok": True}
)

print(r)
