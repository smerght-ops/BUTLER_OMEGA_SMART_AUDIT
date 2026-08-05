# -*- coding: utf-8 -*-

"""
Stage 11.2

Image Session

Accumulates image semantics across dialogue.
"""

class ImageSession:

    _parts = []

    IMAGE_START = (
        "нарисуй",
        "сгенерируй",
        "создай изображение",
        "создай картинку",
        "сделай картинку",
        "сделай фото",
    )

    @classmethod
    def update(cls, text: str) -> str:

        text = (text or "").strip()

        low = text.lower()

        for cmd in cls.IMAGE_START:

            if low.startswith(cmd):

                cls._parts = []

                text = text[len(cmd):].strip()

                break

        if text:

            cls._parts.append(text)

        return ", ".join(cls._parts)

    @classmethod
    def current(cls):

        return ", ".join(cls._parts)

    @classmethod
    def clear(cls):

        cls._parts = []


if __name__ == "__main__":

    print(ImageSession.update("нарисуй девушку"))
    print(ImageSession.update("в полный рост"))
    print(ImageSession.update("на море"))
    print(ImageSession.update("под водопадом"))
    print(ImageSession.current())

