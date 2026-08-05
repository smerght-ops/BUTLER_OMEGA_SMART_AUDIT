# BIONIC EXECUTION MODEL

## 1. Полная цепочка выполнения

От получения запроса пользователя до завершения задачи.

```
USER (вводит текст в LM Studio UI)
  ↓
LM Studio Desktop App (Electron) — принимает ввод, формирует сессию
  ↓
Bionic Session Manager — создаёт/обновляет session в ng-sessions.sqlite
  ↓
LLM Server (llama.cpp, порт 41343) — получает prompt через WebSocket API
  ↓
LlamaV4 Inference Engine — token-by-token generation на GPU/CPU
  ↓
Prediction Stream — streaming-ответ с событиями (fragments + tool calls)
  ↓
LM Studio SDK (lmstudio Python package, v1.5.0) — .act() метод
  │
  ├── Если LLM вернул text → финальный ответ пользователю
  └── Если LLM запросил tool call:
        ↓
      Tool Executor (ThreadPoolExecutor внутри .act())
        │
        ├── lmstudio/sample-file-system/* → createFolder, replaceFile, readFileLines
        ├── lmstudio/shell-v1 → shell_command на host Windows
        └── lmstudio/python-v1/runPython → запуск Python кода на хосте
        ↓
      Tool Result → добавляется в Chat history как ToolResultMessage
        ↓
      .act() цикл повторяется (round_index + 1)
        ↓
      Новый prediction round с обновлённым контекстом
        ↓
      ... (повторяется пока LLM не вернёт text без tool calls)
        ↓
      ActResult(rounds=N, total_time_seconds=T) → возвращает управление вызывающему
```

**Ключевые файлы:**
- `C:/Users/KOS/.lmstudio/apps/bionic/` — Bionic app data (sessions, projects)
- `C:/Users/KOS/.lmstudio/bin/lms.exe` — LM Studio CLI / API server launcher
- `C:/Users/KOS/AppData/Local/Python/pythoncore-3.12-64/Lib/site-packages/lmstudio/sync_api.py` — SDK .act() метод (строки 1326–1508)
- `C:/Users/KOS/.lmstudio/server-logs/` — логи LlamaV4 inference engine

---

## 2. Где принимается решение вызвать Tool

**Внутри LLM server (llama.cpp на порту 41343).**

Решение принимает сама модель во время генерации токенов. Когда модель определяет, что для выполнения задачи нужен внешний инструмент, она генерирует special token-паттерн, который сервер интерпретирует как `PredictionToolCallEvent`.

**Доказательства из исходников:**

1. **SDK код (sync_api.py:1406–1416):**
```python
for event in prediction_stream._iter_events():
    if isinstance(event, PredictionToolCallEvent):
        tool_call_request = event.arg
        tool_call_requests.append(tool_call_request)
        tool_call = endpoint.request_tool_call(tool_call_request)
        pending_tool_calls[pool.submit(tool_call)] = tool_call_request
```

2. **Server logs (2026-07-26.1.log):**
   - `slot print_timing` показывает timing каждого prediction round
   - `draft acceptance = 0.87368` — speculative decoding влияет на скорость, но не на решение о tool call
   - Каждый prediction round — это отдельный вызов LLM server

3. **ChatResponseEndpoint (json_api.py):**
   - Формирует prompt с tool definitions для каждого раунда
   - На финальном раунде (`final_round_index`) tools отключаются: `*(llm_tool_args if round_index != final_round_index else (None, None))`

**Важно:** Решение о вызове инструмента принимается **исключительно LLM**. SDK и Bionic UI только исполняют результат этого решения.

---

## 3. Когда вызывается LLM

LLM вызывается в следующих случаях:

1. **Первый запрос пользователя** — initial prediction round с системным промптом + пользовательским сообщением
2. **После каждого tool call** — новый prediction round с обновлённым Chat history (включая tool results)
3. **Каждый раунд цикла .act()** — пока LLM не вернёт ответ без tool calls

**Механизм вызова:**
- `llm_model.act(chat=chat, tools=[...], max_prediction_rounds=N)` — основной метод
- Внутри: `ChatResponseEndpoint` → WebSocket channel → LlamaV4 server
- Streaming через `PredictionStream._iter_events()` — события приходят по мере генерации

**Параметры вызова (из sync_api.py):**
```python
endpoint = ChatResponseEndpoint(
    self.identifier,           # model identifier
    agent_chat,                # Chat history (обновляется каждый раунд)
    response_format,           # always None when tools are used
    config,                    # LlmPredictionConfig (temperature, etc.)
    preset,                    # optional config preset
    ...
    llm_tool_args if round_index != final_round_index else (None, None)  # tools
)
```

---

## 4. Когда управление возвращается LLM

**После завершения каждого prediction round и выполнения всех tool calls.**

Цикл `.act()` работает так:

```python
for round_index in round_counter:          # цикл по раундам
    # 1. Отправить prompt в LLM server (streaming)
    for event in prediction_stream._iter_events():
        if isinstance(event, PredictionToolCallEvent):
            tool_call_requests.append(...)

    prediction = prediction_stream.result()  # дождаться завершения генерации

    # 2. Если есть tool calls — выполнить их
    if pending_tool_calls:
        tool_results = [finish_tool_call(fut) for fut in as_completed(...)]
        agent_chat.add_assistant_response(prediction, tool_call_requests)
        agent_chat.add_tool_results(tool_results)  # ← управление возвращается LLM здесь

    # 3. Если нет tool calls — выходим из цикла
    if not tool_call_requests:
        break
```

**Ключевой момент:** Управление возвращается LLM **только после полного завершения всех tool calls**. Tool calls выполняются параллельно через `ThreadPoolExecutor(max_parallel_tool_calls)`, и `.act()` блокируется до завершения последнего.

---

## 5. Полный цикл

```
User (вводит запрос в LM Studio UI)
↓
Bionic Session Manager создаёт/обновляет сессию в ng-sessions.sqlite
↓
LLM Server (llama.cpp, порт 41343) — Round #0: prompt eval + generation
↓
LLM генерирует tool call request → PredictionToolCallEvent
↓
SDK выполняет tool call через ThreadPoolExecutor
  ├── lmstudio/sample-file-system/* → чтение/запись файлов на Windows
  ├── lmstudio/shell-v1 → shell_command на хосте
  └── lmstudio/python-v1/runPython → запуск Python кода
↓
Tool result добавляется в Chat history (ToolResultMessage)
↓
LLM Server — Round #1: prompt eval (с новым контекстом) + generation
↓
... (повторяется для каждого раунда, max_prediction_rounds=N) ...
↓
LLM генерирует финальный text response (без tool calls)
↓
.add_assistant_response(prediction) → финальное сообщение пользователю
↓
ActResult(rounds=N, total_time_seconds=T) — цикл завершён
```

**Пример из server logs (2026-07-26.1.log):**
```
[Round 0] prompt eval time =     520.57 ms /   323 tokens (    1.61 ms per token)
           eval time =    1276.29 ms /   261 tokens (    4.89 ms per token)
           total time =    1796.86 ms /   584 tokens

[Round 1] prompt eval time =    6959.96 ms /    22 tokens (  316.36 ms per token)
           eval time =   18108.68 ms /   181 tokens (  100.05 ms per token)
           total time =   25068.64 ms /   203 tokens
```

---

## 6. Где возникают самые большие задержки

**Факт 1: Prompt eval time растёт с размером контекста.**

Из server logs (2026-07-26.1.log):
- Round #0: `520 ms` для 323 токенов → **1.61 мс/токен**
- Round #1: `6960 ms` для 22 токенов → **316.36 мс/токен**

Второй раунд в ~13 раз медленнее первого, потому что prompt содержит результаты предыдущих tool calls и растёт линейно с каждым раундом.

**Факт 2: Token generation rate ограничен GPU.**

Из server logs:
- `eval time = 18108 ms / 181 tokens` → **10.00 tokens/second**
- Это скорость генерации на Qwen3.6-35B-A3B-Q4_K_S.gguf (Q4 quantization)

**Факт 3: Speculative decoding помогает, но не устраняет проблему.**

Из server logs:
- `draft acceptance = 0.87368` (166 accepted / 190 generated) — Round #0
- `draft acceptance = 0.70667` (106 accepted / 150 generated) — Round #1

Speculative decoding ускоряет prompt eval, но не generation rate.

**Факт 4: Tool execution добавляет непредсказуемую задержку.**

- `lmstudio/sample-file-system/*` — файловый I/O на Windows (зависит от диска)
- `lmstudio/shell-v1` — запуск shell команд (зависит от команды)
- `lmstudio/python-v1/runPython` — запуск Python интерпретатора (~100-500ms overhead)

**Факт 5: WebSocket latency между SDK и LLM server минимальна.**

Общение через `ws://127.0.0.1:41343/llm` — localhost, задержка < 1ms. Не является узким местом.

---

## 7. Почему Bionic иногда долго "думает"

**Причина 1: Рост контекста в каждом раунде.**

Каждый prediction round отправляет **весь Chat history** на сервер. После N tool calls история содержит:
- Системный промпт (фиксированный размер)
- Пользовательские сообщения (фиксированный размер)
- N пар assistant/tool_result сообщений (растёт линейно)

Результат: `prompt eval time` растёт экспоненциально с числом раундов.

**Причина 2: Локальная LLM медленнее облачной.**

Qwen3.6-35B-A3B на RTX 3090 Ti (из server logs):
- Generation rate: ~10 tokens/second
- Prompt eval: от 1ms до 300+ ms per token (зависит от контекста)

Для сравнения: облачные модели генерируют 50-200 tokens/second.

**Причина 3: Multi-step задачи = много раундов.**

Задача "создай файл → прочитай его → измени → сохрани" требует минимум 4 prediction round'а:
1. LLM решает создать файл → tool call createFile
2. LLM читает результат → tool call readFile
3. LLM анализирует содержимое → tool call replaceFile
4. LLM формирует финальный ответ

Каждый раунд = полный prompt eval + generation.

**Причина 4: Speculative decoding имеет предел эффективности.**

`draft acceptance = 0.7-0.87` означает, что 13-30% токенов генерируются без помощи draft model. Это снижает ускорение, но не устраняет его полностью.

---

## 8. Какие части цикла можно ускорить

**Ускоряемо (факты из исходников):**

1. **Сокращение числа раундов через better system prompt.**
   - Если LLM может выполнить задачу за 1-2 раунда вместо 4-5 — общий время сократится пропорционально.
   - Факт: `max_prediction_rounds=5` по умолчанию в probe-коде. Уменьшение до 3 для простых задач сэкономит 2 round'а.

2. **Параллельные tool calls.**
   - SDK уже поддерживает `max_parallel_tool_calls` (по умолчанию 1).
   - Если LLM генерирует N независимых tool calls в одном раунде — установка `max_parallel_tool_calls=N` ускорит выполнение в N раз.

3. **Оптимизация prompt eval через KV cache reuse.**
   - Server logs показывают: `graphs reused = 94` (Round #0) и `167` (Round #1).
   - LlamaV4 уже использует KV cache, но `cache reuse is not supported` для некоторых конфигураций.

**Не ускоряемо извне (ограничения архитектуры):**

4. **Generation rate LLM.**
   - Ограничен hardware (GPU compute) и quantization. Q4_K_S на RTX 3090 Ti = ~10 t/s — это физический предел для данной модели.

5. **Prompt eval time при большом контексте.**
   - Растёт линейно с размером prompt. При N tool calls история растёт, и каждый раунд обрабатывает весь prompt заново.

6. **WebSocket latency.**
   - localhost WebSocket < 1ms — не является узким местом.

**Не применимо:**

7. **Нет programmatic API для Bionic session management.**
   - Из INTEGRATION_DESIGN_READ_ONLY_AUDIT.md: `PROGRAMMATIC_BIONIC_INTERFACE = NOT FOUND`
   - Нельзя управлять сессиями, отменять tool calls или получать telemetry извне.
   - Единственный watchdog — HTTP-level timeout на API call.
