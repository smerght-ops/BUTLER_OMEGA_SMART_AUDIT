# -*- coding: utf-8 -*-
from pathlib import Path


class AgentRouter:
    """
    Lightweight intent router.
    Safe additive component: does not modify existing Butler logic.
    """

    IMAGE_EXTENSIONS = {
        ".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp", ".tif", ".tiff"
    }

    CODE_WORDS = {
        "python", "код", "скрипт", "script", "traceback",
        "exception", "ошибка", "bug", "powershell", "ps1"
    }

    MEMORY_WORDS = {
        "память", "memory", "найди", "поиск", "search",
        "архив", "index", "индекс", "документ"
    }

    GENERATION_WORDS = {
        "нарисуй", "draw", "image", "изображение",
        "sdxl", "flux", "comfy", "картинка", "сгенерируй"
    }

    def route(self, user_input: str) -> str:

        text = str(user_input).lower().strip()

        p = Path(text)

        if p.suffix.lower() in self.IMAGE_EXTENSIONS:
            return "vision"

        for word in self.GENERATION_WORDS:
            if word in text:
                return "generation"

        for word in self.CODE_WORDS:
            if word in text:
                return "coder"

        for word in self.MEMORY_WORDS:
            if word in text:
                return "memory"

        return "analysis"


if __name__ == "__main__":

    router = AgentRouter()

    tests = [
        "ошибка python traceback",
        "найди документ про станок",
        "нарисуй двигатель",
        "photo.jpg",
        "что ты думаешь об этом"
    ]

    for t in tests:
        print(f"{t} -> {router.route(t)}")
