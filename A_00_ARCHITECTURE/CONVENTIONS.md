# BUTLER OMEGA SMART CONVENTIONS

ACTIVE FLOW

chat_router.py
    ->
smart_dispatcher_v2.py
    ->
ButlerHarness
    ->
Department
    ->
ProviderManager

RULES

1. Все новые функции идут через ButlerHarness.

2. Department не пишет файлы напрямую без Harness.

3. Department обязан иметь:
   - NAME
   - can_handle()
   - execute()

4. SemanticMemory используется через SmartDispatcherV2.

5. Legacy код не изменяется.

LEGACY

- professor.py
- run_professor_daemon.py
- dream_manager.py
- smart_dispatcher.py
