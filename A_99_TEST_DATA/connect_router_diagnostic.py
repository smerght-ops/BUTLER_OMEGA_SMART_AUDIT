from pathlib import Path

file_path = Path("A_03_ORCHESTRATION") / "chat_router.py"
if not file_path.exists():
    print("[-] Ошибка: chat_router.py не найден!")
    exit(1)

content = file_path.read_text(encoding="utf-8")

# Целевой маркер для точечной врезки
old_target = '        out_file.write_text(result, encoding="utf-8")'

# Улучшенный код теста: сохраняем промпт + передаем в SmartDispatcherV2 + ловим и печатаем результат
new_target = (
    '        out_file.write_text(result, encoding="utf-8")\n\n'
    '        # === ДИАГНОСТИЧЕСКАЯ ВРЕЗКА ВЕХИ 4.15.4 (КОНТРОЛЬ РЕЗУЛЬТАТА) ===\n'
    '        try:\n'
    '            from A_02_MANAGERS.smart_dispatcher_v2 import SmartDispatcherV2\n'
    '            print("\\n[*] Роутер: Передаю сгенерированный промпт в SmartDispatcherV2...")\n'
    '            dispatcher = SmartDispatcherV2()\n'
    '            dispatch_query = f"нарисуй {result}"\n'
    '            \n'
    '            # Вызываем и жестко фиксируем ответ отдела\n'
    '            dispatch_result = dispatcher.dispatch(dispatch_query)\n'
    '            \n'
    '            print("\\n" + "="*50)\n'
    '            print("[✓] ОТВЕТ ОТ ДИСПЕТЧЕРА ИНТЕГРАЦИИ:")\n'
    '            print(dispatch_result)\n'
    '            print("="*50 + "\\n")\n'
    '        except Exception as dispatcher_err:\n'
    '            print(f"[!] Ошибка на магистрали Диспетчера: {dispatcher_err}")'
)

if old_target in content:
    content = content.replace(old_target, new_target)
    file_path.write_text(content, encoding="utf-8")
    print("[OK] Сигнальный провод врезан с контролем вывода. Скрипт готов к тесту.")
else:
    print("[-] Ошибка: Точка врезки out_file.write_text не найдена!")
