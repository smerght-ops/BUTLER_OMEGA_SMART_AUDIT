from A_03_ORCHESTRATION.anti_loop_budget import AntiLoopBudget

b = AntiLoopBudget(limit=3)

for i in range(5):
    print(i + 1, b.allow())

print(b.status())
