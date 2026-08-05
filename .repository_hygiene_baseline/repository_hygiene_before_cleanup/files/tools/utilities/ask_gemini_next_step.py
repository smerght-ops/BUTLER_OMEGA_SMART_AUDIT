# -*- coding: utf-8 -*-
import os
from pathlib import Path
from google import genai

ROOT = Path.cwd()
API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

prompt = """
Ты инженерный помощник проекта BUTLER_OMEGA_SMART.

ЖЕСТКИЕ ПРАВИЛА:
1. Не меняй дорожную карту.
2. Не предлагай альтернативы.
3. Дай только следующий PowerShell-шаг.
4. Не выполняй команды.
5. Не добавляй рассуждения.
6. Формат ответа: только PowerShell-блок.

ТЕКУЩЕЕ СОСТОЯНИЕ:
- Documentation Department V2 завершен.
- EvidenceDoctor V1/V2 status работает.
- Команда "доктор проекта" в Butler OS возвращает HEALTHY.
- Нужно продолжать V2.1 командный интерфейс EvidenceDoctor.
- Следующая цель: команды "статус", "пересобери", "аудит" должны корректно работать через Butler OS.

ДАЙ ТОЛЬКО СЛЕДУЮЩИЙ PowerShell-ШАГ.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=prompt
)

out = ROOT / "GEMINI_NEXT_STEP.md"
out.write_text(response.text, encoding="utf-8")

print(response.text)
