# -*- coding: utf-8 -*-
"""
BUTLER OMEGA SMART
ROADMAP 6.0

Semantic Query Parser
Stage 1.0
"""

import re
from typing import List

class SemanticQueryParser:

    def parse(self, text: str) -> List[str]:

        text = text.lower()

        tokens = re.findall(r"[а-яёa-z0-9_]+", text)

        seen = set()
        result = []

        aliases = {
            "крыши":"крыша",
            "крышу":"крыша",
            "крышей":"крыша",
            "автобуса":"автобус",
            "автобусе":"автобус",
            "автобусу":"автобус",
            "ремонта":"ремонт",
            "ремонте":"ремонт"
        }

        for t in tokens:

            t = aliases.get(t, t)

            if t not in seen:
                seen.add(t)
                result.append(t)

        return result


if __name__ == "__main__":

    p = SemanticQueryParser()

    print(p.parse("ремонт крыши автобуса"))
