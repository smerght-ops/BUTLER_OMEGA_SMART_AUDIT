import json
import time
import hashlib
from pathlib import Path


class SemanticMemory:

    def __init__(self):

        self.memory_dir = Path("A_07_MEMORY")
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        self.index_path = self.memory_dir / "MEMORY_INDEX.jsonl"

        if not self.index_path.exists():
            self.index_path.touch()

    def append(
        self,
        path,
        handler,
        summary="",
        entities=None,
        tags=None,
        engine="",
        doc_type="other",
        needs_review=False,
        source="pipeline",
        timestamp=None
    ):

        if entities is None:
            entities = []

        if tags is None:
            tags = []

        if timestamp is None:
            timestamp = int(time.time())

        record = {
            "path": str(path),
            "handler": handler,
            "type": doc_type,
            "summary": summary,
            "entities": entities,
            "tags": tags,
            "engine": engine,

            # v1.1 fields
            "timestamp": timestamp,
            "needs_review": bool(needs_review),
            "source": source
        }

        with self.index_path.open(
            "a",
            encoding="utf-8"
        ) as f:

            json.dump(
                record,
                f,
                ensure_ascii=False
            )

            f.write("\n")
    def search_by_tags(self, tags):

        if not self.index_path.exists():
            return []

        tags = {str(x).lower() for x in tags}
        results = []

        with self.index_path.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                try:
                    record = json.loads(line)

                    record_tags = {
                        str(x).lower()
                        for x in record.get("tags", [])
                    }

                    if tags & record_tags:
                        results.append(record)

                except Exception:
                    pass

        return results

    def search_by_text(self, query_text):

        if not self.index_path.exists():
            return []

        query_text = str(query_text).lower()

        for ch in ",.;:!?()[]{}'""":
            query_text = query_text.replace(ch, " ")

        query_words = set(query_text.split())

        results = []

        with self.index_path.open("r", encoding="utf-8", errors="ignore") as f:

            for line in f:
                try:
                    record = json.loads(line)

                    search_text = " ".join([
                        str(record.get("summary","")),
                        str(record.get("value","")),
                        str(record.get("key","")),
                        " ".join(record.get("tags",[])),
                        " ".join(record.get("entities",[]))
                    ]).lower()

                    for ch in ",.;:!?()[]{}'""":
                        search_text = search_text.replace(ch," ")

                    summary_words = set(search_text.split())

                    if record.get("type") == "skill":
                        summary_words.discard("создай")

                    score = len(
                        query_words & summary_words
                    )

                    if score > 0:
                        record["_score"] = score
                        results.append(record)

                except Exception:
                    pass

        results.sort(
            key=lambda r: r.get("_score", 0),
            reverse=True
        )

        return results

    def _records(self):
        records = []
        if not self.index_path.exists():
            return records
        with self.index_path.open("r", encoding="utf-8", errors="ignore") as stream:
            for line in stream:
                try:
                    value = json.loads(line)
                    if isinstance(value, dict):
                        records.append(value)
                except (ValueError, TypeError):
                    continue
        return records

    def _append_record(self, record):
        with self.index_path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")

    def skill_events(self):
        """Return skill lifecycle records from the canonical memory index."""
        return [row for row in self._records() if row.get("type") in {"skill", "skill_telemetry"}]

    def append_skill_event(self, record):
        """Append a SkillManager-owned lifecycle event without a second store."""
        if not isinstance(record, dict) or not str(record.get("event") or "").startswith("SKILL_"):
            raise ValueError("INVALID_SKILL_EVENT")
        self._append_record(record)
        return dict(record)

    @staticmethod
    def _knowledge_id(key):
        digest = hashlib.sha256(str(key).strip().casefold().encode("utf-8")).hexdigest()[:16]
        return f"knowledge:{digest}"

    def knowledge_state(self, key):
        """Return append-only versions and the selected active version."""
        knowledge_id = self._knowledge_id(key)
        events = [row for row in self._records() if row.get("knowledge_id") == knowledge_id]
        versions = [row for row in events if row.get("event") == "KNOWLEDGE_VERSION"]
        active_version = None
        for row in events:
            if row.get("event") in {"KNOWLEDGE_VERSION", "KNOWLEDGE_ROLLBACK"}:
                active_version = row.get("active_version") or row.get("version")
        active = next((row for row in reversed(versions) if row.get("version") == active_version), None)
        return {"knowledge_id": knowledge_id, "key": str(key), "active": active,
                "versions": versions, "events": events}

    def evolve_knowledge(self, key, value, provenance, related_media=None):
        """Compare and append a controlled version without deleting history."""
        state = self.knowledge_state(key)
        active = state.get("active")
        normalized = " ".join(str(value).casefold().split())
        previous = " ".join(str((active or {}).get("value", "")).casefold().split())
        if active is None:
            relation = "NEW"
        elif normalized == previous:
            relation = "DUPLICATE"
        elif normalized and previous and (normalized in previous or previous in normalized):
            relation = "SUPPORTS_EXISTING"
        else:
            relation = "CONFLICTS_WITH_EXISTING"
        version = len(state["versions"]) + 1
        activate = active is None or relation in {"DUPLICATE", "SUPPORTS_EXISTING"}
        active_version = version if activate else active.get("version")
        record = {
            "path": f"memory://knowledge/{state['knowledge_id'].split(':', 1)[1]}",
            "handler": "SemanticMemory", "type": "knowledge",
            "summary": f"{key} = {value}", "entities": [str(key), str(value)],
            "tags": ["knowledge", relation.casefold()], "engine": "controlled_evolution",
            "timestamp": int(time.time()), "needs_review": relation == "CONFLICTS_WITH_EXISTING",
            "source": str(provenance), "event": "KNOWLEDGE_VERSION",
            "knowledge_id": state["knowledge_id"], "key": str(key), "value": value,
            "version": version, "relation": relation, "active_version": active_version,
            "previous_version": (active or {}).get("version"),
            "related_media": list(related_media or []),
        }
        self._append_record(record)
        return dict(record)

    def rollback_knowledge(self, key, version):
        state = self.knowledge_state(key)
        target = next((row for row in state["versions"] if row.get("version") == int(version)), None)
        if target is None:
            return {"ok": False, "error": "KNOWLEDGE_VERSION_NOT_FOUND"}
        event = {
            "path": target.get("path"), "handler": "SemanticMemory", "type": "knowledge_event",
            "summary": f"rollback {key} -> v{version}", "entities": [str(key)],
            "tags": ["knowledge", "rollback"], "engine": "controlled_evolution",
            "timestamp": int(time.time()), "needs_review": False, "source": "rollback",
            "event": "KNOWLEDGE_ROLLBACK", "knowledge_id": state["knowledge_id"],
            "key": str(key), "active_version": int(version),
        }
        self._append_record(event)
        return {"ok": True, "active": target, "event": event}

    def link_media(self, key, media_type, path, source=None, fragment=None):
        state = self.knowledge_state(key)
        active = state.get("active")
        if active is None:
            return {"ok": False, "error": "KNOWLEDGE_NOT_FOUND"}
        link = {"type": str(media_type), "path": str(path),
                "source": str(source or path), "fragment": fragment}
        event = {
            "path": active.get("path"), "handler": "SemanticMemory", "type": "knowledge_event",
            "summary": f"media link for {key}: {path}", "entities": [str(key), str(path)],
            "tags": ["knowledge", "media", str(media_type)], "engine": "knowledge_linking",
            "timestamp": int(time.time()), "needs_review": False, "source": str(source or path),
            "event": "KNOWLEDGE_MEDIA_LINK", "knowledge_id": state["knowledge_id"],
            "key": str(key), "active_version": active.get("version"), "media": link,
        }
        self._append_record(event)
        return {"ok": True, "knowledge_id": state["knowledge_id"], "media": link}

    def knowledge_search(self, query):
        results, seen = [], set()
        stop = {"какой", "какая", "какое", "что", "это", "для", "или", "тебя", "меня", "просил", "покажи"}
        query_words = {word.strip(".,?!:;—-\"'") for word in
                       str(query).casefold().replace("/", " ").replace("_", " ").split()}
        query_words = {word for word in query_words if len(word) >= 3 and word not in stop}
        candidates = []
        for row in self._records():
            if not row.get("knowledge_id"):
                continue
            searchable = " ".join((str(row.get("key", "")), str(row.get("summary", "")),
                                   " ".join(map(str, row.get("tags", []))),
                                   " ".join(map(str, row.get("entities", []))))).casefold()
            normalized = searchable.replace("/", " ").replace("_", " ")
            record_words = {word.strip(".,?!:;—-\"'") for word in normalized.split()}
            overlap = query_words & record_words
            if overlap:
                candidates.append((len(overlap), int(row.get("timestamp") or 0), row))
        for _, _, row in sorted(candidates, key=lambda item: (item[0], item[1]), reverse=True):
            knowledge_id = row.get("knowledge_id")
            if not knowledge_id or knowledge_id in seen:
                continue
            seen.add(knowledge_id)
            state = self.knowledge_state(row.get("key"))
            active = state.get("active")
            if active is None:
                continue
            media = [event.get("media") for event in state["events"]
                     if event.get("event") == "KNOWLEDGE_MEDIA_LINK"
                     and event.get("active_version") == active.get("version")]
            results.append({"knowledge": active, "related_media": [item for item in media if item]})
        return results

    def media_links(self):
        """Return active knowledge/media relations with their provenance."""
        links = []
        for row in self._records():
            if row.get("event") != "KNOWLEDGE_MEDIA_LINK" or not row.get("media"):
                continue
            state = self.knowledge_state(row.get("key"))
            active = state.get("active")
            if active and row.get("active_version") == active.get("version"):
                links.append({"knowledge": active, "media": row.get("media")})
        return links

    def record_tested_skill(self, signature, trace, provenance):
        """Promote only a successful, contract-valid execution trace."""
        signature = [str(item) for item in signature if item]
        if not signature or not trace or not all(item.get("ok") for item in trace):
            return {"ok": False, "error": "SKILL_TRACE_NOT_SUCCESSFUL"}
        skill_id = "skill:" + hashlib.sha256("|".join(signature).encode("utf-8")).hexdigest()[:16]
        existing = next((row for row in reversed(self._records())
                         if row.get("skill_id") == skill_id and row.get("status") == "TESTED"), None)
        if existing:
            return {"ok": True, "created": False, "skill": existing}
        record = {
            "path": f"memory://skills/{skill_id.split(':', 1)[1]}",
            "handler": "TaskExecutor", "type": "skill",
            "summary": " -> ".join(signature), "entities": signature,
            "tags": ["skill", "tested", "execution_trace"], "engine": "procedural_learning",
            "timestamp": int(time.time()), "needs_review": False, "source": str(provenance),
            "event": "SKILL_PROMOTED", "skill_id": skill_id, "status": "TESTED",
            "signature": signature,
            "trace_contract": [{"capability_id": item.get("capability_id"),
                                "department": item.get("department"), "ok": item.get("ok")}
                               for item in trace],
        }
        self._append_record(record)
        return {"ok": True, "created": True, "skill": record}

    def match_tested_skill(self, signature):
        target = [str(item) for item in signature if item]
        return next((row for row in reversed(self._records())
                     if row.get("type") == "skill" and row.get("status") == "TESTED"
                     and row.get("signature") == target), None)

    def append_dki(
        self,
        id,
        type,
        content,
        status="",
        confidence=0.0,
        source_id="",
        source_path="",
        source_fragment="",
        derived_from="",
        entities=None,
        relations=None,
        lifecycle="ACTIVE",
        version=1,
        trust="HIGH",
        requires_confirmation=False
    ):
        """Append a DerivedKnowledgeItem (DKI v1.0) through existing _append_record().

        Accepts the full DKI contract fields and writes a single JSONL record
        to MEMORY_INDEX.jsonl via self._append_record().
        """
        # --- validation -------------------------------------------------------
        if not id or str(id).strip() == "":
            raise ValueError("DKI 'id' must not be empty")

        if not type or str(type).strip() == "":
            raise ValueError("DKI 'type' must not be empty")

        if not content or str(content).strip() == "":
            raise ValueError("DKI 'content' must not be empty")

        if entities is None:
            entities = []
        if not isinstance(entities, list):
            raise ValueError("DKI 'entities' must be a list")

        if relations is None:
            relations = []
        if not isinstance(relations, list):
            raise ValueError("DKI 'relations' must be a list")

        if not isinstance(requires_confirmation, bool):
            raise ValueError("DKI 'requires_confirmation' must be a bool")

        if not isinstance(version, int) or version <= 0:
            raise ValueError("DKI 'version' must be a positive integer")

        # --- build storage record ---------------------------------------------
        record = {
            "knowledge_id": str(id).strip(),
            "type": str(type).strip(),
            "value": content,
            "status": str(status),
            "confidence": float(confidence),
            "source": str(source_id),
            "source_path": str(source_path),
            "source_fragment": str(source_fragment),
            "derived_from": str(derived_from),
            "entities": list(entities),
            "relations": list(relations),
            "lifecycle": str(lifecycle),
            "version": int(version),
            "trust": str(trust),
            "needs_review": bool(requires_confirmation),
        }

        self._append_record(record)
        return dict(record)
