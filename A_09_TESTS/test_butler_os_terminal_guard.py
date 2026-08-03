import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import BUTLER_OS


class ButlerTerminalGuardTests(unittest.TestCase):
    def test_service_lines_are_rejected(self):
        lines = (
            "=" * 70,
            "[OK] Ядро загружено.",
            "[OK] SmartDispatcherV2 подключен.",
            "[OK] Департаменты доступны.",
            "Введите exit / q / выход для завершения.",
            "[BUTLER | IMAGE | model=ComfyUI | 10ms]",
            "Изображение готово.",
            r"Файл: C:\Test\image.png",
            "[KOS] >",
        )
        self.assertTrue(all(BUTLER_OS._is_system_echo(line) for line in lines))

    def test_similar_human_request_is_not_rejected(self):
        self.assertFalse(BUTLER_OS._is_system_echo("Где находится файл: отчет.png?"))
        self.assertFalse(BUTLER_OS._is_system_echo("Почему изображение готово не полностью?"))

    def test_once_executes_exactly_once_without_input(self):
        result = {"ok": True, "department": "TEST", "text": "done"}
        with patch.object(BUTLER_OS, "clear_screen"), \
             patch.object(BUTLER_OS, "_execute_query", return_value=result) as execute, \
             patch("builtins.input", side_effect=AssertionError("input must not be called")), \
             redirect_stdout(io.StringIO()):
            BUTLER_OS.main("обычная команда")
        execute.assert_called_once_with("обычная команда")

    def test_once_rejects_echo_before_dispatch(self):
        with patch.object(BUTLER_OS, "clear_screen"), \
             patch.object(BUTLER_OS, "_execute_query") as execute, \
             redirect_stdout(io.StringIO()):
            BUTLER_OS.main("Изображение готово.")
        execute.assert_not_called()


if __name__ == "__main__":
    unittest.main()
