# -*- coding: utf-8 -*-

import re
import time
import webbrowser
import requests
import html
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qs, unquote

from A_04_AGENTS.base_department import BaseDepartment


class BrowserDepartment(BaseDepartment):
    """Open an explicitly requested HTTP(S) URL in the system browser."""

    NAME = "BROWSER"
    VERSION = "1.0"
    CAPABILITIES = ("open_url", "web_search")
    DEPENDENCIES = ("Python.webbrowser",)
    DATA_READS = ()
    DATA_WRITES = ()

    _INTENT_RE = re.compile(
        r"(?:открой|открыть|покажи|перейди|перейти|зайди|зайти)\b.*\b(?:сайт|страниц\w*|url|ссылк\w*|браузер)\b",
        re.IGNORECASE,
    )
    _SEARCH_INTENT_RE = re.compile(
        r"(?:найди|найти|поищи|отыщи|отыскать|найдите|покажи)\b.*\b(?:интернет\w*|сет\w*|онлайн|сайт\w*|страниц\w*|url|браузер)\b",
        re.IGNORECASE,
    )
    _DOWNLOAD_INTENT_RE = re.compile(r"(?:скачай|загрузи)\s+(?:файл\s+)?", re.IGNORECASE)
    _SEARCH_ENDPOINT = "https://www.google.com/search"
    _URL_RE = re.compile(r"(?:https?://)?[^\s<>'\"\[\]{}]+", re.IGNORECASE)
    _TRAILING_PUNCTUATION = ".,;:!?)]}»”"

    def __init__(self, opener=None):
        self._opener = opener or webbrowser.open

    def can_handle(self, query: str, context: dict = None) -> bool:
        text = query or ""
        return bool(
            self._INTENT_RE.search(text)
            or self._SEARCH_INTENT_RE.search(text)
            or self._DOWNLOAD_INTENT_RE.search(text)
        )

    def execute(self, query: str, context: dict = None, **kwargs) -> dict:
        started = time.perf_counter()

        context = dict(context or {})
        if context.get("capability_action") == "download_url" or self._DOWNLOAD_INTENT_RE.search(query or ""):
            return self._download(query, context, started)

        search_intent = self._SEARCH_INTENT_RE.search(query or "")
        search_query = None

        if search_intent:
            search_query = re.sub(
                r"^\s*(?:найди|найти|поищи|отыщи|отыскать|найдите|покажи)\s*",
                "",
                query or "",
                flags=re.IGNORECASE,
            ).strip()
            search_query = re.sub(
                r"\s+(?:и\s+)?(?:открой|открыть|покажи|перейди|перейти|зайди|зайти)(?:\s+его|\s+её|\s+это)?\s+(?:в\s+)?браузер\w*\.?\s*$",
                "",
                search_query,
                flags=re.IGNORECASE,
            ).strip()
            if not search_query:
                return self._result(
                    started,
                    ok=False,
                    text="Не удалось выполнить поиск: укажите поисковый запрос.",
                    error="BROWSER_SEARCH_QUERY_MISSING",
                    metadata={"opened": False, "open_attempted": False},
                )
            url = self._build_search_url(search_query)
        else:
            try:
                url = self._extract_and_validate_url(query)
            except ValueError as exc:
                return self._result(
                    started,
                    ok=False,
                    text="Не удалось открыть сайт: укажите допустимый адрес HTTP или HTTPS.",
                    error=str(exc),
                    metadata={"opened": False, "open_attempted": False},
                )

        operation_metadata = {}
        if search_query is not None:
            operation_metadata = {
                "operation": "web_search",
                "search_query": search_query,
                "search_engine": "Google",
            }

        try:
            accepted = bool(self._opener(url, new=2))
        except Exception as exc:
            return self._result(
                started,
                ok=False,
                text="Не удалось передать адрес системному браузеру.",
                error="BROWSER_OPEN_FAILED",
                metadata={
                    "url": url,
                    "opened": False,
                    "open_attempted": True,
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                },
            )

        if not accepted:
            return self._result(
                started,
                ok=False,
                text="Системный браузер не принял запрос на открытие адреса.",
                error="BROWSER_OPEN_REJECTED",
                metadata={
                    "url": url,
                    "opened": False,
                    "open_attempted": True,
                    **operation_metadata,
                },
            )

        confirmation = (
            f"Поисковый запрос передан системному браузеру: {search_query}"
            if search_query is not None
            else f"Адрес передан системному браузеру: {url}"
        )
        return self._result(
            started,
            ok=True,
            text=confirmation,
            error=None,
            metadata={
                "url": url,
                "opened": True,
                "open_attempted": True,
                "open_method": "Python.webbrowser.open",
                **operation_metadata,
            },
        )

    def _download(self, query, context, started):
        if not context.get("network_allowed") and "разрешаю" not in (query or "").casefold():
            return self._result(started, False,
                                "Для загрузки требуется явное разрешение владельца.",
                                "NETWORK_PERMISSION_REQUIRED",
                                {"downloaded": False, "source": None})
        match = re.search(r"https?://[^\s<>'\"\[\]{}]+", query or "", re.I)
        if not match:
            if not context.get("resolve_search"):
                return self._result(started, False, "Не указан HTTP(S) URL.",
                                    "BROWSER_URL_MISSING", {"downloaded": False})
            try:
                url = self._resolve_search_result(query)
            except Exception as exc:
                return self._result(started, False, "Не удалось найти документ для загрузки.",
                                    "BROWSER_SEARCH_RESOLVE_FAILED",
                                    {"downloaded": False, "exception_type": type(exc).__name__})
        else:
            url = match.group(0).rstrip(self._TRAILING_PUNCTUATION)
        parsed = urlsplit(url)
        if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
            return self._result(started, False, "Недопустимый URL.",
                                "BROWSER_URL_INVALID", {"downloaded": False, "source": url})
        target_dir = Path(context.get("download_dir") or
                          Path(__file__).resolve().parents[2] / "A_06_WORKSPACE" / "incoming")
        target_dir.mkdir(parents=True, exist_ok=True)
        filename = Path(parsed.path).name or "downloaded_document"
        filename = re.sub(r"[^A-Za-z0-9._-]+", "_", filename)
        try:
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()
            content_type = response.headers.get("content-type", "").casefold()
            if "text/html" in content_type:
                filename = (Path(filename).stem or "downloaded_document") + ".txt"
                target = target_dir / filename
                source = response.content.decode(response.encoding or "utf-8", errors="replace")
                source = re.sub(r"(?is)<(?:script|style).*?>.*?</(?:script|style)>", " ", source)
                source = html.unescape(re.sub(r"(?s)<[^>]+>", " ", source))
                target.write_text(re.sub(r"\s+", " ", source).strip(), encoding="utf-8")
            else:
                target = target_dir / filename
                with target.open("wb") as stream:
                    for chunk in response.iter_content(1024 * 64):
                        if chunk:
                            stream.write(chunk)
        except Exception as exc:
            return self._result(started, False, "Загрузка не выполнена.",
                                "BROWSER_DOWNLOAD_FAILED",
                                {"downloaded": False, "source": url,
                                 "exception_type": type(exc).__name__})
        return self._result(started, True, f"Файл загружен: {target}", None,
                            {"downloaded": True, "source": url, "output": str(target),
                             "path": str(target), "provenance": url})

    def _resolve_search_result(self, query):
        topic = re.sub(
            r"(?i)\b(?:найди|поищи|в интернете|в сети|скачай|загрузи|его|её|ее|файл)\b",
            " ", str(query or ""),
        )
        topic = re.sub(r"\s+", " ", topic).strip(" ,.;")
        if not topic:
            raise ValueError("EMPTY_SEARCH_TOPIC")
        # Prefer a verifiable official origin inferred from a named product.
        # This is generic entity/domain resolution, not a per-query URL table.
        ignored = {"word", "docx", "pdf", "http", "https"}
        entities = [item for item in re.findall(r"\b[A-Za-z][A-Za-z0-9_-]{2,}\b", topic)
                    if item.casefold() not in ignored]
        for entity in entities[:4]:
            for host in (f"www.{entity.casefold()}.org", f"{entity.casefold()}.org",
                         f"www.{entity.casefold()}.com", f"{entity.casefold()}.com"):
                candidate = f"https://{host}/"
                try:
                    probe = requests.get(candidate, timeout=12, allow_redirects=True,
                                         headers={"User-Agent": "ButlerOmegaSmart/1.0"})
                    final_host = (urlsplit(probe.url).hostname or "").casefold()
                    if probe.ok and entity.casefold() in final_host:
                        return probe.url
                except requests.RequestException:
                    continue
        response = requests.get(
            "https://html.duckduckgo.com/html/",
            params={"q": topic}, timeout=30,
            headers={"User-Agent": "ButlerOmegaSmart/1.0"},
        )
        response.raise_for_status()
        candidates = re.findall(r'class="result__a"[^>]+href="([^"]+)"', response.text, re.I)
        if not candidates:
            rss = requests.get(
                "https://www.bing.com/search",
                params={"q": topic, "format": "rss"}, timeout=30,
                headers={"User-Agent": "ButlerOmegaSmart/1.0"},
            )
            rss.raise_for_status()
            root = ET.fromstring(rss.content)
            candidates = [node.text for node in root.findall(".//item/link") if node.text]
        for candidate in candidates:
            value = html.unescape(candidate)
            parsed = urlsplit(value)
            if parsed.hostname and "duckduckgo.com" in parsed.hostname:
                value = unquote(parse_qs(parsed.query).get("uddg", [""])[0])
            target = urlsplit(value)
            blocked = ("porn", "adult", "casino", "betting")
            relevance = set(re.findall(r"[a-z0-9]{3,}", topic.casefold()))
            destination = f"{target.hostname or ''} {target.path}".casefold()
            if (target.scheme in {"http", "https"} and target.hostname
                    and not any(term in destination for term in blocked)
                    and any(term in destination for term in relevance)):
                return value
        raise LookupError("NO_SEARCH_RESULT")

    def _build_search_url(self, search_query: str) -> str:
        return f"{self._SEARCH_ENDPOINT}?{urlencode({'q': search_query})}"

    def _extract_and_validate_url(self, query: str) -> str:
        intent = self._INTENT_RE.search(query or "")
        if not intent:
            raise ValueError("BROWSER_INTENT_NOT_FOUND")

        tail = (query or "")[intent.end():].strip()
        match = self._URL_RE.search(tail)
        if not match:
            raise ValueError("BROWSER_URL_MISSING")

        candidate = match.group(0).rstrip(self._TRAILING_PUNCTUATION)
        if not re.match(r"^https?://", candidate, re.IGNORECASE):
            candidate = "https://" + candidate

        try:
            parsed = urlsplit(candidate)
            hostname = parsed.hostname
            port = parsed.port
        except ValueError as exc:
            raise ValueError("BROWSER_URL_INVALID") from exc

        if (
            parsed.scheme.lower() not in {"http", "https"}
            or not hostname
            or parsed.username is not None
            or parsed.password is not None
            or any(char.isspace() for char in candidate)
        ):
            raise ValueError("BROWSER_URL_INVALID")

        if "." not in hostname and hostname.lower() != "localhost":
            raise ValueError("BROWSER_URL_INVALID_HOST")

        try:
            ascii_host = hostname.encode("idna").decode("ascii")
        except UnicodeError as exc:
            raise ValueError("BROWSER_URL_INVALID_HOST") from exc

        host = f"[{ascii_host}]" if ":" in ascii_host else ascii_host
        if port is not None:
            host = f"{host}:{port}"

        return urlunsplit((parsed.scheme.lower(), host, parsed.path, parsed.query, parsed.fragment))

    def _result(self, started, ok, text, error, metadata):
        return {
            "ok": ok,
            "department": self.NAME,
            "model": "SystemBrowser",
            "latency_ms": max(0, int((time.perf_counter() - started) * 1000)),
            "text": text,
            "error": error,
            "metadata": metadata,
        }


