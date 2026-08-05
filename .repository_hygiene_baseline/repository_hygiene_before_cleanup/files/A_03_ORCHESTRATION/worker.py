# -*- coding: utf-8 -*-

from A_03_ORCHESTRATION.professor_adapter import ProfessorAdapter
from A_02_MANAGERS.queue_manager import QueueManager
from A_01_CORE.logger_config import setup_logger

# Интеграция шины безопасности Harness V3
from A_03_ORCHESTRATION.butler_harness import ButlerHarness

try:
    # AgentRouter DISABLED
    from A_03_ORCHESTRATION.router_registry import RouterRegistry
except Exception:
    AgentRouter = None
    RouterRegistry = None

logger = setup_logger('WORKER')


class Worker:

    def __init__(self):
        self.queue_manager = QueueManager()
        self.dispatcher = ProfessorAdapter()
        
        # Подключаем стабильную шину Harness V3
        self.harness = ButlerHarness()

        self.router = None
        self.registry = None

        if AgentRouter is not None and RouterRegistry is not None:
            try:
                self.router = None
                self.registry = RouterRegistry()
                logger.info('AgentRouter enabled in Worker.')
            except Exception as e:
                logger.error(f'AgentRouter disabled: {str(e)}')

    def _resolve_route(self, filepath):
        if self.router is None or self.registry is None:
            return 'auto'

        try:
            route_name = self.router.route(filepath)
            target_agent = self.registry.get_target(route_name)
            logger.info(f'Router selected route={route_name}, target={target_agent}')
            return target_agent
        except Exception as e:
            logger.error(f'Router fallback to auto: {str(e)}')
            return 'auto'

    def process_once(self):
        # Безопасно берем атомарно заблокированную задачу из очереди
        task = self.queue_manager.get_next_task()

        if not task:
            return False

        filepath = task['filepath']
        logger.info(f'Processing document: {filepath}')

        try:
            target_agent = self._resolve_route(filepath)

            # Определяем целевую лямбду выполнения для Harness
            def run_agent_pipeline():
                return self.dispatcher.process_agent_task(filepath, target_agent)

            # Change Request must be supplied explicitly by the task producer.
            cr_file = task.get('cr_name')

            # Прогоняем задачу через полный сквозной контур Guards
            harness_result = self.harness.execute(
                department_name="WORKER_CORE",
                task=f"Process file: {filepath} with agent: {target_agent}",
                executor=run_agent_pipeline,
                cr_name=cr_file
            )

            # Анализируем консолидированный вердикт пайплайна безопасности
            if harness_result.get("pipeline_status") == "SUCCESS":
                logger.info(f'Job for {filepath} successfully completed via Harness pipeline.')
            else:
                # Пайплайн заблокирован гвардами на ранней стадии
                logger.error(f'Harness BLOCKED task for {filepath}! Status: {harness_result.get("pipeline_status")}. Code: {harness_result.get("guard_code")}')
                return False

        except Exception as e:
            logger.error(f'Error processing {filepath} in worker loop: {str(e)}')
            return False

        return True


