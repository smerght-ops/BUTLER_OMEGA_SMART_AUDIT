from pathlib import Path

p = Path(r"A_03_ORCHESTRATION\chat_router.py")

text = p.read_text(encoding="utf-8")

old = '''
    memory_file = Path(__file__).resolve().parent.parent / "A_05_STORAGE" / "USER_MEMORY.md"
    memory_text = memory_file.read_text(encoding="utf-8-sig") if memory_file.exists() else ""

    prompt = (
        "Ты локальный помощник Butler Omega. �спользуй долговременную память как источник истины о пользователе. Отвечай по-русски, понятно и по делу.\n\n"
        + "=== ДОЛГОВ� ЕМЕННАЯ ПАМЯТЬ ===\n"
        + memory_text
        + "\n\n=== ВОП� ОС ПОЛЬЗОВАТЕЛЯ ===\n"
        + text
    )
'''

new = '''
    prompt = MemoryLayer().build_prompt(
        user_text=text,
        task_id="TASK_0001"
    )
'''

text = text.replace(old, new)

p.write_text(text, encoding="utf-8")

print("PATCH OK")
