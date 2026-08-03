from abc import ABC, abstractmethod
from pathlib import Path

class BaseHandler(ABC):
    supported_extensions = []

    def can_handle(self, path: Path) -> bool:
        return path.suffix.lower() in self.supported_extensions

    @abstractmethod
    def extract(self, path: Path) -> dict:
        """
        Возвращает:
        {
            "success": bool,
            "text": str,
            "metadata": dict
        }
        """
        raise NotImplementedError
