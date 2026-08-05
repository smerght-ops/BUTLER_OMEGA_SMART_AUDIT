# -*- coding: utf-8 -*-

class HybridResolver:

    KNOWN_HYBRIDS = {
        "тигрокрыса": ("tiger", "rat"),
        "тигрокрысу": ("tiger", "rat"),
        "бетонолошадь": ("concrete", "horse"),
        "монетокамень": ("coin", "stone"),
        "кастрюля-человек": ("cooking pot", "human"),
        "акула-человек": ("shark", "human"),
        "акулачеловек": ("shark", "human"),
        "монетакамень": ("coin", "stone"),
    }

    KNOWN_PARTS = [
        "тигр",
        "крыса",
        "кот",
        "волк",
        "слон",
        "кит",
        "дракон",
        "орёл",
        "медведь",
        "лев",
        "собака",
        "мышь"
    ]

    def resolve(self, text: str):

        q = text.lower().strip().strip(".,!?;:\"'")

        for name, entities in self.KNOWN_HYBRIDS.items():
            if name in q:
                return {
                    "is_hybrid": True,
                    "entity_1": entities[0],
                    "entity_2": entities[1],
                    "source": name,
                }

        for first in self.KNOWN_PARTS:

            if q.startswith(first):

                second = q[len(first):].strip()

                if second in self.KNOWN_PARTS:

                    return {
                        "is_hybrid": True,
                        "entity_1": first,
                        "entity_2": second
                    }

        return {
            "is_hybrid": False,
            "prompt": q
        }


if __name__ == "__main__":

    r = HybridResolver()

    tests = [
        "тигркрыса",
        "волккот",
        "слонкит",
        "дракон"
    ]

    for t in tests:
        print(t, "=>", r.resolve(t))
