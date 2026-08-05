"""Read-only computer observation through the canonical Department boundary."""

from __future__ import annotations

import base64
import ctypes
import io
import os
import subprocess
import time

from A_03_ORCHESTRATION.permission import DepartmentExecutionGateway
from A_04_AGENTS.VisionDepartment.runner import VisionDepartment
from A_04_AGENTS.base_department import BaseDepartment


class ComputerObservationBackend:
    """OS reads only; every method returns data without changing desktop state."""

    def screenshot_base64(self) -> str:
        from PIL import ImageGrab
        image = ImageGrab.grab(all_screens=True)
        stream = io.BytesIO()
        image.save(stream, format="PNG")
        return base64.b64encode(stream.getvalue()).decode("ascii")

    def windows(self) -> list[dict]:
        if os.name != "nt":
            return []
        user32 = ctypes.windll.user32
        values = []
        callback_type = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

        def collect(hwnd, _lparam):
            length = user32.GetWindowTextLengthW(hwnd)
            if user32.IsWindowVisible(hwnd) and length:
                buffer = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buffer, length + 1)
                values.append({"handle": int(hwnd), "title": buffer.value})
            return True

        user32.EnumWindows(callback_type(collect), 0)
        return values

    def clipboard_text(self) -> str:
        if os.name != "nt":
            return ""
        completed = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", "Get-Clipboard -Raw"],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", errors="replace", timeout=5,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        if completed.returncode != 0:
            raise RuntimeError("CLIPBOARD_READ_FAILED")
        return completed.stdout

    def foreground(self) -> dict:
        if os.name != "nt":
            return {"handle": None, "title": "", "platform_supported": False}
        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        length = user32.GetWindowTextLengthW(hwnd)
        buffer = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buffer, length + 1)
        return {"handle": int(hwnd), "title": buffer.value, "platform_supported": True}


class ComputerUseDepartment(BaseDepartment):
    NAME = "COMPUTER_USE"
    VERSION = "1.0"
    CAPABILITIES = ("capture_screenshot", "list_windows", "read_clipboard", "inspect_navigation")
    DATA_READS = ("desktop pixels", "window titles", "clipboard text", "foreground window")
    DATA_WRITES = ()
    DANGER_LEVEL = "READ_ONLY"
    BLOCKED_MARKERS = (
        "click", "type ", "press ", "write ", "paste", "set clipboard", "move mouse",
        "launch ", "start program", "close window", "minimize", "maximize",
        "клик", "нажми", "напечатай", "вставь", "запусти", "закрой окно",
    )

    def __init__(self, backend=None, gateway=None, vision=None):
        self.backend = backend or ComputerObservationBackend()
        self.gateway = gateway or DepartmentExecutionGateway()
        self.vision = vision or VisionDepartment()

    def can_handle(self, query: str, context: dict = None) -> bool:
        normalized = str(query or "").casefold()
        return any(marker in normalized for marker in (
            "screenshot", "screen", "window", "clipboard", "скриншот", "экран", "окн", "буфер",
        ))

    def execute(self, query: str, context: dict = None, **kwargs) -> dict:
        started = time.perf_counter()
        context = dict(context or {})
        normalized = str(query or "").casefold()
        if any(marker in normalized for marker in self.BLOCKED_MARKERS):
            return self._result(started, False, "", "COMPUTER_USE_READ_ONLY_VIOLATION", {"read_only": True})
        action = str(context.get("action") or "").casefold()
        if not action:
            if "clipboard" in normalized or "буфер" in normalized:
                action = "read_clipboard"
            elif "window" in normalized or "окн" in normalized:
                action = "list_windows"
            elif "navigation" in normalized or "foreground" in normalized or "активн" in normalized:
                action = "inspect_navigation"
            else:
                action = "capture_screenshot"
        try:
            if action == "capture_screenshot":
                screenshot = self.backend.screenshot_base64()
                metadata = {"read_only": True, "action": action, "image_base64": screenshot, "format": ".png"}
                if context.get("analyze"):
                    analysis = self.gateway.execute(
                        self.vision, str(query), context={"image_base64": screenshot, "image_format": ".png"},
                    )
                    metadata["vision_analysis"] = analysis
                return self._result(started, True, "Screenshot captured in memory.", None, metadata)
            if action == "list_windows":
                windows = self.backend.windows()
                return self._result(started, True, f"Visible windows: {len(windows)}", None,
                                    {"read_only": True, "action": action, "windows": windows})
            if action == "read_clipboard":
                text = self.backend.clipboard_text()
                return self._result(started, True, text, None,
                                    {"read_only": True, "action": action, "length": len(text)})
            if action == "inspect_navigation":
                foreground = self.backend.foreground()
                return self._result(started, True, foreground.get("title", ""), None,
                                    {"read_only": True, "action": action, "foreground": foreground})
            return self._result(started, False, "", "COMPUTER_USE_ACTION_NOT_ALLOWED", {"read_only": True})
        except Exception as exc:
            return self._result(started, False, "", f"{type(exc).__name__}: {exc}", {"read_only": True, "action": action})

    def _result(self, started, ok, text, error, metadata):
        return {
            "ok": bool(ok), "department": self.NAME, "model": "ComputerUseDepartment",
            "latency_ms": max(0, int((time.perf_counter() - started) * 1000)),
            "text": str(text), "error": error, "metadata": dict(metadata),
        }
