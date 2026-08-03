# -*- coding: utf-8 -*-
from pathlib import Path

class SmartRouter:
    def detect(self, text: str) -> str:
        t = text.lower()
        if any(x in t for x in ["код", "python", "ошибка", "скрипт", "функция", "класс"]):
            return "code"
        if any(x in t for x in ["архитектура", "роутер", "диспетчер", "отдел", "factory", "ядро"]):
            return "architecture"
        if any(x in t for x in ["нарисуй", "картинк", "изображен", "comfyui"]):
            return "image"
        if any(x in t for x in ["фото", "картинку прочитай", "vision", "увидь"]):
            return "vision"
        if any(x in t for x in ["помнишь", "память", "как меня зовут", "любимый цвет"]):
            return "memory"
        return "chat"

if __name__ == "__main__":
    r = SmartRouter()
    tests = ["напиши код", "как меня зовут", "нарисуй тигракрысу", "спроектируй отделы Factory"]
    for q in tests:
        print(q, "=>", r.detect(q))