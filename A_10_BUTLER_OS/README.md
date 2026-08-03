# BUTLER-OS

Статус: первый слой вынесен из Factory в корень BUTLER_OMEGA.

Роли:
- Factory: лаборатория и полигон.
- A_10_BUTLER_OS/00_PRODUCTION: новый боевой слой.
- chat_router_WORKING_COPY.py: сохранённая рабочая копия текущего роутера.
- department_contract.py: единый контракт отделов.
- model_registry.py: утвержденный стек моделей.
- smart_router.py: первый детерминированный классификатор задач.

Следующий шаг:
подключить smart_router.py к текущему chat_router.py и убрать ручной выбор модели для обычных запросов.