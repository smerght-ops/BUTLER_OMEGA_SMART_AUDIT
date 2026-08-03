import sys

sys.stdout.reconfigure(encoding='utf-8')

class EventBus:
    _listeners = {}

    @classmethod
    def subscribe(cls, event_type: str, listener):
        """Регистрация подписчика на определенное событие"""
        if event_type not in cls._listeners:
            cls._listeners[event_type] = []
        cls._listeners[event_type].append(listener)

    @classmethod
    def publish(cls, event_type: str, data=None):
        """Публикация события для всех подписчиков"""
        if event_type in cls._listeners:
            for listener in cls._listeners[event_type]:
                try:
                    listener(data)
                except Exception as e:
                    print(f"✗ [EVENT BUS ERROR] Ошибка в обработчике {listener.__name__}: {e}")
