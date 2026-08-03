"""
Router Integration for Butler Omega
Automatically connects AgentRouter outputs to targets via RouterRegistry
Safe additive component with DK02 Memory Context Integration
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from A_03_ORCHESTRATION.agent_router import AgentRouter
from A_03_ORCHESTRATION.router_registry import RouterRegistry
from A_03_ORCHESTRATION.passport_commands import PassportCommandHandler
# Импортируем наш собранный стек памяти
from A_07_MEMORY.memory_orchestrator import MemoryOrchestrator


class RouterIntegration:

    def __init__(self):
        self.router = AgentRouter()
        self.registry = RouterRegistry()
        self.passport_handler = PassportCommandHandler()
        # Инициализируем мастер-контроллер памяти
        self.memory_orchestrator = MemoryOrchestrator()

    def dispatch(self, user_input: str) -> str:
        sys_response = self.passport_handler.handle_command(user_input)
        if sys_response is not None:
            return sys_response

        # DK02 MEMORY ENRICHMENT LAYER
        try:
            # Обогащаем промпт через пятиуровневый стек памяти (эвристика + скоринг + бюджет)
            # Так как модели в аргументах пока нет, передаем дефолтную для сборки контекста
            memory_payload = self.memory_orchestrator.build_ollama_payload(
                user_text=user_input,
                model="qwen35-ru:latest"
            )
            enriched_input = memory_payload.get("prompt", user_input)
        except Exception:
            enriched_input = user_input

        # Отправляем в роутер уже насыщенный контекстом текст
        route = self.router.route(enriched_input)
        target = self.registry.get_target(route)
        
        return target


if __name__ == "__main__":

    integrator = RouterIntegration()
    test_inputs = [
        "ошибка python traceback",
        "найди документ про станок",
        "нарисуй двигатель",
        "photo.jpg",
        "что ты думаешь об этом"
    ]

    for t in test_inputs:
        print(f"Input: {t} -> Target: {integrator.dispatch(t)}")
