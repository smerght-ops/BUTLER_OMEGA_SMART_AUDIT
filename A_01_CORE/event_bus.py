import sys
import threading

sys.stdout.reconfigure(encoding='utf-8')

class EventBus:
    _listeners = {}
    _lock = threading.RLock()

    @classmethod
    def subscribe(cls, event_type: str, listener):
        """Регистрация подписчика на определенное событие"""
        with cls._lock:
            cls._listeners.setdefault(event_type, [])
            if listener not in cls._listeners[event_type]:
                cls._listeners[event_type].append(listener)
        return listener

    @classmethod
    def unsubscribe(cls, event_type: str, listener):
        with cls._lock:
            listeners = cls._listeners.get(event_type, [])
            if listener in listeners:
                listeners.remove(listener)

    @classmethod
    def publish(cls, event_type: str, data=None):
        """Публикация события для всех подписчиков"""
        with cls._lock:
            listeners = tuple(cls._listeners.get(event_type, ()))
        if listeners:
            for listener in listeners:
                try:
                    listener(data)
                except Exception as e:
                    print(f"✗ [EVENT BUS ERROR] Ошибка в обработчике {listener.__name__}: {e}")
