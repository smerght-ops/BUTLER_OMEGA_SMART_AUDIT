"""Read-only resource awareness for scheduling and runtime queries."""

from __future__ import annotations

import os
import socket
from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class ResourceSnapshot:
    captured_at: str
    cpu_count: int
    ram_available_bytes: int | None
    ram_total_bytes: int | None
    vram_available_bytes: int | None
    services: dict[str, bool]

    def to_dict(self) -> dict:
        return asdict(self)


class ResourceAwareness:
    SERVICES = {"ollama": ("127.0.0.1", 11434), "comfyui": ("127.0.0.1", 8188), "lm_studio": ("127.0.0.1", 1234)}

    @staticmethod
    def _memory() -> tuple[int | None, int | None]:
        try:
            import psutil
            memory = psutil.virtual_memory()
            return int(memory.available), int(memory.total)
        except (ImportError, OSError):
            return None, None

    @staticmethod
    def _online(address: tuple[str, int], timeout: float = 0.05) -> bool:
        try:
            with socket.create_connection(address, timeout=timeout):
                return True
        except OSError:
            return False

    def snapshot(self) -> ResourceSnapshot:
        available, total = self._memory()
        return ResourceSnapshot(
            captured_at=datetime.now(timezone.utc).isoformat(),
            cpu_count=os.cpu_count() or 1,
            ram_available_bytes=available,
            ram_total_bytes=total,
            vram_available_bytes=None,
            services={name: self._online(address) for name, address in self.SERVICES.items()},
        )
