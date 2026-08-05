# BUTLER UTF-8 STDIN ACCEPTANCE

Дата: 16.07.2026  
Рабочий каталог: `C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART`  
Выбранный способ: **A — cmd.exe и UTF-8-файл без BOM**

## Observation

Production-код не изменялся. Созданы только разрешённые диагностические файлы:

- `A_09_TESTS\butler_utf8_stdin_russian_commands.txt`
- `A_09_TESTS\butler_utf8_stdin_browser_commands.txt`
- `A_09_TESTS\butler_utf8_stdin_russian.log`
- `A_09_TESTS\butler_utf8_stdin_browser.log`
- настоящий отчёт

Кодировки процедуры:

- stdin: UTF-8 без BOM, подтверждено фактическими байтами;
- stdout: вывод официальной цепочки перенаправлен `cmd.exe` в файл, `START_BUTLER_OS.ps1` задаёт UTF-8;
- stderr: объединён со stdout штатным оператором `cmd.exe` `2>&1`.

## Preliminary integrity

| Production-файл | SHA-256 до запуска |
|---|---|
| `START_BUTLER_OS.bat` | `B7BFA9E6E12CD183F1BCABA47E15F3B2EF62119E3E5E4FE633242E3DC7DE763B` |
| `START_BUTLER_OS.ps1` | `19830434057098141BBDF1DAF4290244E56BF96A0F2E1A10E2663B4E932C774D` |
| `BUTLER_OS.py` | `BFD856CF69C97999D1519AF0DAE8198B555E16142FB60771256EADA6043CC113` |

## Command files

### Russian control command

Полный путь:

```text
C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\A_09_TESTS\butler_utf8_stdin_russian_commands.txt
```

- размер: 18 bytes;
- SHA-256: `97CE708D268725C058276856F00C841ED86B2C00471E9D34DF2C72C2A728EE28`;
- BOM: отсутствует;
- последние байты: двойной LF;
- фактические байты:

```text
D0 BA D1 82 D0 BE 20 D1 82 D1 8B 0A 65 78 69 74 0A 0A
```

### Browser control command

Полный путь:

```text
C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\A_09_TESTS\butler_utf8_stdin_browser_commands.txt
```

- размер: 48 bytes;
- SHA-256: `CB8B3A8647465E8F620DDAD83F4E18AA696F771AEE547B3D4D18B6DE08237764`;
- BOM: отсутствует;
- последние байты: двойной LF;
- первые 24 bytes:

```text
D0 9E D1 82 D0 BA D1 80 D0 BE D0 B9 20 D1 81 D0 B0 D0 B9 D1 82 20 68 74
```

## Проверка №1 — `кто ты`

Точная команда:

```text
C:\Windows\System32\cmd.exe /d /s /c ""C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\START_BUTLER_OS.bat" < "C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\A_09_TESTS\butler_utf8_stdin_russian_commands.txt" > "C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\A_09_TESTS\butler_utf8_stdin_russian.log" 2>&1"
```

Полный непрерывный объединённый журнал:

```text
C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\A_09_TESTS\butler_utf8_stdin_russian.log
```

- размер журнала: 8568 bytes;
- SHA-256 журнала: `DDA80876445ACB2982F75351AAC48E5C67124E597BE98FE3FB98468FA81270D4`;
- рабочий терминал появился: да;
- `[KOS] >` появился: да;
- команда обработана: да;
- Result header: `[BUTLER | PROJECT_DOCUMENTATION | model=PROJECT_DOCUMENTATION_DEPARTMENT | 4ms]`;
- `UnicodeDecodeError`: отсутствует;
- `exit` обработан: да;
- сессия Butler закрыта: да;
- BAT завершился штатно: нет, журнал заканчивается ожидающим `pause`;
- PID и код завершения повторной попытки не сохранены из-за внешнего тайм-аута сборщика evidence;
- зависшие процессы официальной цепочки после очистки: отсутствуют.

Участок обработки команды и завершения:

```text
BUTLER OMEGA OS v1.1 — WORK TERMINAL
[OK] Ядро загружено.
[OK] SmartDispatcherV2 подключен.
[OK] Департаменты доступны.

[KOS] >
[BUTLER | PROJECT_DOCUMENTATION | model=PROJECT_DOCUMENTATION_DEPARTMENT | 4ms]
...
[KOS] >
[OK] Butler OS остановлен.

[OK] Butler session closed
Press any key to continue . . .
```

## Проверка №2 — Browser-команда

Точная команда:

```text
C:\Windows\System32\cmd.exe /d /s /c ""C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\START_BUTLER_OS.bat" < "C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\A_09_TESTS\butler_utf8_stdin_browser_commands.txt" > "C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\A_09_TESTS\butler_utf8_stdin_browser.log" 2>&1"
```

Полный непрерывный объединённый журнал:

```text
C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART\A_09_TESTS\butler_utf8_stdin_browser.log
```

- размер журнала: 6628 bytes;
- SHA-256 журнала: `9ECE830B3E15D8AB8BC16B7697C21A30E9611BA4808358346FB24BDCE768FA4A`;
- рабочий терминал появился: да;
- `[KOS] >` появился: да;
- Browser-команда обработана: да;
- Result header: `[BUTLER | BROWSER | model=SystemBrowser | 39ms]`;
- URL сохранён: `https://example.com`;
- системный ответ: `Адрес передан системному браузеру: https://example.com`;
- `UnicodeDecodeError`: отсутствует;
- `exit` обработан: да;
- сессия Butler закрыта: да;
- BAT завершился штатно: нет, журнал заканчивается ожидающим `pause`;
- PID и код завершения не были сериализованы: сборщик evidence получил `OutOfMemoryException` после завершения процессной обработки;
- зависшие процессы официальной цепочки после очистки: отсутствуют.

Последние строки полного журнала:

```text
BUTLER OMEGA OS v1.1 — WORK TERMINAL
======================================================================
[OK] Ядро загружено.
[OK] SmartDispatcherV2 подключен.
[OK] Департаменты доступны.
Введите exit / q / выход для завершения.
======================================================================

[KOS] >
[BUTLER | BROWSER | model=SystemBrowser | 39ms]

Адрес передан системному браузеру: https://example.com

[KOS] >
[OK] Butler OS остановлен.

[OK] Butler session closed
Press any key to continue . . .
```

## Evidence

1. Оба command-файла имеют UTF-8-байты без BOM.
2. Оба запуска прошли через `START_BUTLER_OS.bat` и загрузили рабочий терминал.
3. Кириллические команды дошли до `BUTLER_OS.py` без повреждения и без `UnicodeDecodeError`.
4. Команда `кто ты` была фактически обработана Department.
5. BrowserDepartment фактически получил вторую команду, сохранил URL и передал его системному браузеру.
6. `exit` закрыл обе сессии Butler.
7. Дополнительный LF в перенаправленном файле не обеспечил завершение BAT: Python заранее буферизовал входной файл, и `pause` остался без доступного символа.
8. Диагностические процессы после принудительной очистки отсутствуют.

## Final integrity

| Production-файл | SHA-256 после запуска | Совпадает |
|---|---|---:|
| `START_BUTLER_OS.bat` | `B7BFA9E6E12CD183F1BCABA47E15F3B2EF62119E3E5E4FE633242E3DC7DE763B` | да |
| `START_BUTLER_OS.ps1` | `19830434057098141BBDF1DAF4290244E56BF96A0F2E1A10E2663B4E932C774D` | да |
| `BUTLER_OS.py` | `BFD856CF69C97999D1519AF0DAE8198B555E16142FB60771256EADA6043CC113` | да |

```text
PRODUCTION FILE CHANGES: 0
```

## Proven Statement

- UTF-8 stdin без BOM корректно передаёт русские команды официальному Butler: **доказано**.
- Русская команда фактически обработана: **доказано**.
- Browser-команда и URL переданы без повреждения: **доказано**.
- `UnicodeDecodeError` устранён на уровне автоматической процедуры ввода: **доказано**.
- Production-код не изменялся: **доказано SHA-256**.
- Новые диагностические процессы не остались: **доказано повторной проверкой процессов**.
- Штатное завершение BAT после `pause`: **не пройдено**.

## Conclusion

**FAIL**

UTF-8-подача команд работает корректно, но способ A в заданной форме не удовлетворяет обязательному условию штатного завершения BAT: дополнительный перевод строки после `exit` потребляется буферизированным stdin Python и не освобождает завершающий `pause`.
