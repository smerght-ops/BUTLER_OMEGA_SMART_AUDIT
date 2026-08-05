# A_07_MEMORY/search_engine.py
import json
import re
import time
from pathlib import Path

try:
    import pymorphy3
except Exception:
    pymorphy3 = None


class SemanticSearchEngine:
    SUMMARY_WEIGHT = 5
    TAG_WEIGHT = 4
    ENTITY_WEIGHT = 4
    PATH_WEIGHT = 3
    TEXT_WEIGHT = 2
    PHRASE_BONUS = 6
    MULTI_TOKEN_BONUS = 2
    SYNONYM_WEIGHT = 3

    def __init__(
        self,
        index_path="A_07_MEMORY/MEMORY_INDEX.jsonl",
        synonyms_path="A_07_MEMORY/search_synonyms.json"
    ):
        self.index_path = Path(index_path)
        self.synonyms_path = Path(synonyms_path)
        self.synonyms = self._load_synonyms()

        # ---------------- Cache ----------------
        self._cache = {}
        self._cache_ttl = 300
        self._cache_max_size = 256
        self._cache_hits = 0
        self._cache_misses = 0


    def _cache_key(self, query, limit):
        return (self._normalize(query), int(limit))

    def _cache_get(self, query, limit):
        key = self._cache_key(query, limit)
        item = self._cache.get(key)

        if item is None:
            self._cache_misses += 1
            return None

        ts, value = item

        if (time.time() - ts) > self._cache_ttl:
            self._cache.pop(key, None)
            self._cache_misses += 1
            return None

        self._cache_hits += 1
        return value

    def _cache_put(self, query, limit, value):
        key = self._cache_key(query, limit)
        self._cache[key] = (
            time.time(),
            value
        )

        # CACHE_EVICT
        while len(self._cache) > self._cache_max_size:
            oldest_key = min(
                self._cache.items(),
                key=lambda kv: kv[1][0]
            )[0]
            self._cache.pop(oldest_key, None)
    def _load_synonyms(self):
        if not self.synonyms_path.exists():
            return {}

        try:
            with self.synonyms_path.open("r", encoding="utf-8") as f:
                raw = json.load(f)
        except Exception:
            return {}

        normalized = {}
        for key, values in raw.items():
            k = self._normalize(key)
            normalized[k] = [self._normalize(v) for v in values]
        return normalized

    def _load_all(self):
        records = []

        if not self.index_path.exists():
            return records

        with self.index_path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        return records

    def _normalize(self, text):
        text = str(text).lower().replace("ё", "е").strip()
        text = re.sub(r"\s+", " ", text)
        return text

    def _simple_ru_stem(self, token):
        token = self._normalize(token)

        endings = [
            "ами", "ями", "ого", "ему", "ыми", "ими",
            "ой", "ей", "ью", "ия", "иям", "иях",
            "ах", "ях", "ом", "ем", "ам", "ям",
            "ы", "и", "а", "я", "у", "ю", "е", "о"
        ]

        for ending in endings:
            if len(token) > 5 and token.endswith(ending):
                return token[: -len(ending)]

        return token

    def _parse_query(self, query):
        query = self._normalize(query)

        phrases = re.findall(r'"([^"]+)"', query)
        query_without_phrases = re.sub(r'"[^"]+"', " ", query)

        raw_tokens = [
            t for t in re.split(r"\W+", query_without_phrases, flags=re.UNICODE)
            if t.strip()
        ]

        tokens = []
        for token in raw_tokens:
            normalized = self._normalize(token)
            stem = self._simple_ru_stem(normalized)
            tokens.append(stem)

        phrases = [self._normalize(p) for p in phrases if p.strip()]

        return phrases, tokens

    def _expand_tokens(self, tokens):
        expanded = set(tokens)

        for token in tokens:
            for key, values in self.synonyms.items():
                key_stem = self._simple_ru_stem(key)

                if token == key_stem or token == key:
                    expanded.update(values)
                    expanded.update(self._simple_ru_stem(v) for v in values)

        return list(expanded)

    def _record_text_fields(self, rec):
        summary = self._normalize(rec.get("summary", ""))
        path = self._normalize(rec.get("path", ""))
        text = self._normalize(rec.get("text") or rec.get("value", ""))

        tags = [
            self._normalize(t)
            for t in rec.get("tags", [])
        ]

        entities = [
            self._normalize(e if not isinstance(e, dict) else e.get("text", ""))
            for e in rec.get("entities", [])
        ]

        return summary, path, text, tags, entities

    def search(self, query: str, limit: int = 10):

        # CACHE_READ
        cached = self._cache_get(query, limit)
        if cached is not None:
            return cached

        phrases, tokens = self._parse_query(query)

        if not phrases and not tokens:
            return []

        expanded_tokens = self._expand_tokens(tokens)
        records = self._load_all()
        scored_results = []

        for rec in records:
            score = 0
            matched_units = set()

            summary, path, text, tags, entities = self._record_text_fields(rec)

            searchable_blob = " ".join(
                [summary, path, text] + tags + entities
            )

            for phrase in phrases:
                if phrase in searchable_blob:
                    score += self.PHRASE_BONUS
                    matched_units.add(phrase)

                if phrase in summary:
                    score += self.SUMMARY_WEIGHT

                if phrase in text:
                    score += self.TEXT_WEIGHT

            for token in expanded_tokens:
                token_hit = False
                token_stem = self._simple_ru_stem(token)

                if token in summary or token_stem in self._simple_ru_stem(summary):
                    score += self.SUMMARY_WEIGHT
                    token_hit = True

                if token in path:
                    score += self.PATH_WEIGHT
                    token_hit = True

                if any(token in tag or token_stem in self._simple_ru_stem(tag) for tag in tags):
                    score += self.TAG_WEIGHT
                    token_hit = True

                if any(token in entity or token_stem in self._simple_ru_stem(entity) for entity in entities):
                    score += self.ENTITY_WEIGHT
                    token_hit = True

                if token in text:
                    score += self.TEXT_WEIGHT
                    token_hit = True

                if token_hit:
                    matched_units.add(token)

                    if token not in tokens:
                        score += self.SYNONYM_WEIGHT

            if len(matched_units) > 1:
                score += self.MULTI_TOKEN_BONUS * (len(matched_units) - 1)

            if score > 0:
                scored_results.append((score, rec))

        scored_results.sort(
            key=lambda item: (
                -item[0],
                item[1].get("path", "").lower()
            )
        )

        result = scored_results[:limit]

        # CACHE_WRITE
        self._cache_put(query, limit, result)

        return result


    def cache_stats(self):
        return {
            "hits": self._cache_hits,
            "misses": self._cache_misses,
            "entries": len(self._cache),
        }
    def search_by_tag(self, tag: str):
        tag = self._normalize(tag)
        records = self._load_all()

        return [
            rec for rec in records
            if any(tag in self._normalize(t) for t in rec.get("tags", []))
        ]

    def search_by_entity(self, entity: str):
        entity = self._normalize(entity)
        records = self._load_all()

        return [
            rec for rec in records
            if any(
                entity in self._normalize(e if not isinstance(e, dict) else e.get("text", ""))
                for e in rec.get("entities", [])
            )
        ]

    def search_by_path(self, substring: str):
        substring = self._normalize(substring)
        records = self._load_all()

        return [
            rec for rec in records
            if substring in self._normalize(rec.get("path", ""))
        ]







    def memory_stats(self):
        records = self._load_all()

        hits = self._cache_hits
        misses = self._cache_misses
        total = hits + misses

        ratio = 0.0
        if total > 0:
            ratio = round((hits / total) * 100.0, 2)

        return {
            "documents": len(records),
            "cache_entries": len(self._cache),
            "cache_hits": hits,
            "cache_misses": misses,
            "cache_hit_ratio": ratio,
            "synonyms": len(self.synonyms),
            "index_exists": self.index_path.exists(),
        }

