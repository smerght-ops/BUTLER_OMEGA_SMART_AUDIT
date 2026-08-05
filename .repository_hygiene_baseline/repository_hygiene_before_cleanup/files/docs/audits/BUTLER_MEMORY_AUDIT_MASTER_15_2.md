# CURRENT TRUTH — OVERRIDES EARLIER CONTRADICTORY AUDIT WORDING

## MEMORY LEVEL COUNT
LOGICAL_MEMORY_LEVEL_COUNT = 6.

L1-L6 are six logical Butler memory levels implemented through
MemoryFacadeV2. They MUST NOT be reduced to the number of sources
used by MemoryOrchestratorV2.build_memory_packet().

DIRECT_BUILD_MEMORY_PACKET_SOURCE_COUNT = 4:
1. Profile/User Facts
2. Semantic Index (L5)
3. Session Events (L2)
4. Graph Relations

Therefore:
"4 factual memory levels instead of 6" = REFUTED.
Correct statement:
"6 logical L1-L6 levels exist; the primary memory packet currently
uses 4 retrieval sources, only part of which map directly to L1-L6."

## BUILD_CONTEXT VS BUILD_MEMORY_PACKET
MemoryFacadeV2.build_context() exposes the L1-L6 architecture.
MemoryOrchestratorV2.build_memory_packet() is a separate,
token-budgeted retrieval path and does not currently include
L1/L3/L4/L6 directly.

## UNRESOLVED WIRING — PASS 1E REQUIRED
Recent audits conflict on dispatcher_bridge_v2 existence/path and
on the exact Agent Core memory boundary.

Do NOT treat either conflicting statement as final truth.
PASS 1E must resolve these from current ACTIVE production code.

## ROADMAP DECISION
Do not create a second Memory, Graph, Index, Orchestrator,
versioning system, rollback system, or knowledge store.

Target remains:
immutable RAW
-> compile/classify/trust
-> typed DerivedKnowledgeItem
-> existing SemanticMemory / MEMORY_INDEX
-> existing Butler retrieval.

PASS 1E is the final READ ONLY verification before freezing
MEMORY BASELINE 15.2 and the DKI contract.

---

BUTLER OMEGA SMART — MEMORY BASELINE 15.2 MASTER



Дата: 2026-07-27Статус: AUDIT BASELINE / READ ONLY CONSOLIDATIONОснование: ROADMAP 7.1 + Agent Core Experimental Roadmap §15.1–15.3Назначение: единая точка истины по аудитам PASS 1 / 1B / 1C / 1D перед продолжением ROADMAP 15.2.



1\. ЗАФИКСИРОВАННАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ ROADMAP



Agent Core Stage 6 — CLOSED / CERTIFIED.



Passport / Project State Synchronization — CLOSED / CERTIFIED.



Cross-Runtime Arbitration — CLOSED / CERTIFIED.



ROADMAP 15.1 Voice Inbox RAW stage:



audio → Whisper → AudioDepartment → ButlerHarness → SmartDispatcherV2 → FilesystemDepartment;



RAW transcript сохраняется в A\_06\_WORKSPACE/STAGE4\_OUTPUT/voice\_inbox/;



реальный E2E: RESULT\_OK=True, MEM\_EQ\_DISK=True, MOJIBAKE=False, FINAL=PASS.



Текущая работа: ROADMAP 15.2 COMPILED KNOWLEDGE / LLM WIKI.



После 15.2: ROADMAP 15.3 MEMORY LINT.



Критические правила:



RAW SOURCE != DERIVED KNOWLEDGE != USER COMMAND.



PERSIST != BELIEVE != EXECUTE.



RAW transcript неизменяем.



Новую параллельную Memory / Graph / Index / Orchestrator не создавать без доказанной необходимости.



2\. ЦЕЛЕВОЙ КОНТРАКТ DERIVED KNOWLEDGE ITEM — v0.1



Кандидатные semantic types:



FACT



PREFERENCE



IDEA



QUESTION



POSSIBLE\_TASK



DECISION



EXPLICIT\_COMMAND



Lifecycle candidate:



CANDIDATE



ACTIVE



CONFLICTED



SUPERSEDED



EXPIRED



REJECTED



Knowledge relations candidate:



NEW



SUPPORTS



CONFLICTS



DUPLICATE



SUPERSEDES



Целевой принцип 15.2C:Compiled Knowledge = Provenance-Backed Knowledge Network.



При этом это НЕ разрешение создавать второй graph engine.Сначала переиспользуется существующая production Memory Butler.



3\. PASS 1 — EXISTING MEMORY / GRAPH INVENTORY



Что было найдено



L1–L6 MemoryFacadeV2.



SemanticMemory / DK02.



MEMORY\_INDEX.jsonl.



SemanticReasoningEngineV2.



SemanticRelationsEngine.



SemanticCore.



semantic\_graph.json.



Architectural Knowledge Graph.



knowledge versioning.



NEW / DUPLICATE / SUPPORTS\_EXISTING / CONFLICTS\_WITH\_EXISTING.



source, entities, tags, media linking.



Ошибка PASS 1



PASS 1 сделал слишком ранний вывод, что graph components не имеют production caller и retrieval фактически только WORD\_OVERLAP.



Этот вывод впоследствии ЧАСТИЧНО ОПРОВЕРГНУТ PASS 1C:SemanticCore / SemanticReasoningEngineV2 вызываются через MemoryOrchestratorV2.graph.analyze().



PASS 1 сохраняется как историческое доказательство, но его final production wiring НЕ является текущей точкой истины.



4\. PASS 1B — HIDDEN / INDIRECT MEMORY DISCOVERY



Были обнаружены дополнительные memory-like механизмы:



AttentionMemory



ContextBudgetManager



SemanticCompressor



MemoryOrchestrator v1



ProjectContextBuilder



CatalogSearchBridge



SelfHealingMemory



MemoryLayer



PASS 1B ошибочно классифицировал AttentionMemory, ContextBudgetManager и SemanticCompressor как DEAD из-за поиска преимущественно прямых callers.



Эта классификация ОПРОВЕРГНУТА PASS 1C.



Полезные находки PASS 1B, которые сохранились:



strong provenance / chain-of-custody отсутствует;



generic trust boundary для внешнего knowledge отсутствует;



source→file linking существует частично через link\_media;



rollback/versioning реально существует внутри SemanticMemory;



ProjectContextBuilder / SelfHealingMemory / MemoryLayer требуют отдельного отношения и не должны автоматически считаться частью активной memory pipeline.



5\. PASS 1C — PRODUCTION WIRING VERIFICATION



ТЕКУЩАЯ ТОЧКА ИСТИНЫ ДЛЯ WIRING



Основной production route



BUTLER\_OS

&#x20; -> AgentCoreCoordinator (primary decision layer)

&#x20;    -> tool call when required

&#x20;       -> dispatcher\_bridge\_v2.dispatch

&#x20;          -> SmartDispatcherV2.dispatch

&#x20;             -> MemoryOrchestratorV2.build\_memory\_packet

&#x20;                -> SemanticMemory.search\_by\_text

&#x20;                -> SemanticSearchEngine.search

&#x20;                -> SemanticMemory.knowledge\_search

&#x20;                -> AttentionMemory.rank\_records

&#x20;                -> SemanticCompressor.compress\_records

&#x20;                -> ContextBudgetManager.fit\_text

&#x20;                -> SemanticCore.analyze

&#x20;             -> context\["memory\_packet"]

&#x20;             -> Department / CHAT

&#x20;                -> memory\_packet\["budget\_context"]

&#x20;                -> LLM prompt



Fallback без Agent Core также приходит в SmartDispatcherV2 и использует тот же memory pipeline.



Финальный статус механизмов после PASS 1C



ACTIVE / INDIRECTLY ACTIVE:



MemoryOrchestratorV2 — ACTIVE, основной memory orchestrator.



AttentionMemory — INDIRECTLY ACTIVE.



ContextBudgetManager — INDIRECTLY ACTIVE.



SemanticCompressor — INDIRECTLY ACTIVE.



SemanticSearchEngine — ACTIVE.



SemanticMemory — ACTIVE.



SemanticCore / SemanticReasoningEngineV2 — ACTIVE, но graph result используется ограниченно.



UNREACHABLE / DEAD по текущему production call graph:



ProjectContextBuilder.



CatalogSearchBridge.



SelfHealingMemory.



MemoryLayer.



MemoryOrchestrator v1.



Важные partial / broken wiring



L1 Passport реализован, но не входит напрямую в MemoryOrchestratorV2.build\_memory\_packet().



Graph traversal реально выполняется, но structured graph result не используется полноценно для ranking/routing; graph relations попадают ограниченно.



BUTLER\_MEMORY\_CONNECTED=YES.



AGENT\_CORE\_MEMORY\_CONNECTED=PARTIAL: Agent Core не имеет собственной memory retrieval до первого tool decision; полная Butler Memory включается после делегирования в SmartDispatcherV2.



memory\_packet



Producer:MemoryOrchestratorV2.build\_memory\_packet().



Содержит:



semantic\_context



profile\_context



knowledge\_context



attention\_context



raw\_context



budget\_context



retrieval.lexical



retrieval.weighted\_semantic



retrieval.graph



retrieval.knowledge



provenance



used\_tokens



user\_input



Final LLM consumer:SmartDispatcherV2.\_execute\_chat() → budget\_context вставляется как РЕЛЕВАНТНАЯ ПАМЯТЬ.



6\. L1–L6 — FINAL CURRENT MAP



L1 — Passport



Storage: A\_07\_CONFIG/project\_passport.json.Implemented.Доступен через MemoryFacadeV2.Не включён напрямую в основной MOv2 memory\_packet.Статус: PARTIAL IN PRIMARY MEMORY PIPELINE.



L2 — Session



ButlerSessionManager / session events.Используется через MemoryFacadeV2/history path.Статус: ACTIVE.



L3 — Tasks



AgentPlannerV2 / plans + project state.Статус: ACTIVE.



L4 — Project History



ProjectHistory / closed milestones + session-history aggregation.Статус: ACTIVE.



L5 — Semantic



SemanticMemory / MEMORY\_INDEX.jsonl.Primary persistent knowledge store.Статус: ACTIVE.



L6 — Strategy



AgentPlannerV2 strategy + execution state.Статус: ACTIVE, через MemoryFacadeV2 paths.



7\. PASS 1D — STORAGE + GRAPH + DKI COMPATIBILITY



ТЕКУЩАЯ ТОЧКА ИСТИНЫ ДЛЯ DATA CONTRACTS



MEMORY\_INDEX.jsonl



Один append-only store с несколькими типами records.



Base semantic record содержит:



path



handler



type



summary



entities\[]



tags\[]



engine



timestamp



needs\_review



source



Knowledge Version record дополнительно содержит:



knowledge\_id



key



value



version



relation



active\_version



previous\_version



related\_media\[]



event=KNOWLEDGE\_VERSION



Media link event:



knowledge\_id



key



active\_version



media.type



media.path



media.source



media.fragment



event=KNOWLEDGE\_MEDIA\_LINK



Rollback event:



knowledge\_id



key



active\_version



event=KNOWLEDGE\_ROLLBACK



Existing lifecycle



NEW



DUPLICATE



SUPPORTS\_EXISTING



CONFLICTS\_WITH\_EXISTING



Version history:



append-only;



previous records do not disappear;



conflict does not automatically replace active version;



needs\_review=True on conflict;



rollback exists.



No explicit:



SUPERSEDED



EXPIRED



REJECTED



Existing provenance



PARTIAL:



source: string exists.



media file path exists through media link.



media.fragment structurally exists.



dedicated source\_path on knowledge item does not exist.



derived\_from does not exist.



chain-of-custody from derived fact back to RAW transcript is not guaranteed.



Existing graph



Storage:A\_07\_MEMORY/semantic\_graph.json.



Node:plain string label.



Edge:{source, relation, target, weight}.



Missing from graph:



stable node ID;



link to knowledge\_id;



source/evidence;



timestamp;



version history.



Graph and MEMORY\_INDEX were created as separate data models.



8\. DKI COMPATIBILITY — FINAL BASELINE



Already reusable:



DKI id -> existing knowledge\_id.



content -> existing value / summary.



append-only persistence.



version history.



NEW / DUPLICATE / SUPPORTS / CONFLICTS lifecycle.



needs\_review -> confirmation/review semantics.



entities\[] exists as strings.



media linking exists.



rollback exists.



Partial:



type semantics: current storage type is record/document type, not the future semantic DKI type FACT/IDEA/etc.



status: relation + needs\_review covers only part.



provenance: source exists but is unstructured.



source fragment: schema exists but currently not proven in active use.



relations: lifecycle relation is not general semantic relation.



graph: exists and is called, but is disconnected from knowledge IDs.



Truly missing for the target DKI:



persistent semantic DKI type (FACT/PREFERENCE/...);



structured source\_path / source reference;



reliable derived\_from;



persistent factual confidence (NOT attention score);



multi-relation/evidence model if required by final frozen DKI;



explicit SUPERSEDED lifecycle if retained in final contract;



stable mapping knowledge item <-> graph node/entity if graph-backed DKI is retained;



memory security/trust boundary for external/untrusted sources;



RAW transcript compiler/reader.



Important:attention.score MUST NOT be reused as factual confidence.It is retrieval relevance, not truth confidence.



9\. WHAT WE MUST NOT BUILD AGAIN



NO second:



memory store;



MEMORY\_INDEX;



semantic index;



MemoryOrchestrator;



attention scorer;



context budget manager;



semantic compressor;



knowledge versioning engine;



knowledge ID generator;



rollback system.



SECOND\_GRAPH\_REQUIRED=NO at this stage.Existing graph must first be evaluated/extended or deliberately retired; a parallel graph is forbidden without explicit architecture decision.



10\. REAL CURRENT GAPS FOR ROADMAP 15.2



The key feature gap remains:



RAW voice transcript .md

&#x20;  -> \[MISSING COMPILE / CLASSIFY / TRUST STEP]

&#x20;  -> DerivedKnowledgeItem

&#x20;  -> existing SemanticMemory / MEMORY\_INDEX

&#x20;  -> MemoryOrchestratorV2

&#x20;  -> relevant context

&#x20;  -> Butler / LLM



Missing production capabilities:



RAW transcript reader/ingest trigger.



LLM compiler from raw free text to typed DKI candidates.



Semantic type distinction:FACT / PREFERENCE / IDEA / QUESTION / POSSIBLE\_TASK / DECISION / EXPLICIT\_COMMAND.



Strong source link from DKI to immutable RAW.



Trust/security policy:external text != trusted memory;detected command inside RAW != permission to execute.



Final mapping between DKI relations/entities and existing graph.



Agent Core pre-tool memory continuity remains PARTIAL and is NOT part of the first RAW→DKI implementation unless explicitly approved.



11\. CONTRADICTIONS RESOLVED



PASS 1 / PASS 1B:AttentionMemory / ContextBudget / SemanticCompressor / graph = DEAD or unused



PASS 1C:OPROVERGНУТО.



Final:



AttentionMemory = ACTIVE indirectly.



ContextBudgetManager = ACTIVE indirectly.



SemanticCompressor = ACTIVE indirectly.



SemanticCore / graph traversal = ACTIVE but limited.



MemoryOrchestrator v1 = unused.



MemoryOrchestratorV2 = ACTIVE.



ProjectContextBuilder = DEAD/unreachable.



CatalogSearchBridge = ACTIVE via SearchDepartment; separate path; NOT part of primary memory_packet.



SelfHealingMemory = DEAD/unreachable.



MemoryLayer = DEAD/unreachable.



When later audits conflict with earlier passes, the newer pass only supersedes the earlier claim when it contains a stronger production call-graph/data-contract proof.



12\. CURRENT ARCHITECTURAL VERDICT



MEMORY MAP FREEZE: READY, subject to one adversarial verification pass.



DKI CONTRACT FREEZE: READY FOR REVIEW, not implementation.



READY\_FOR\_IMPLEMENTATION: NO.



Current architecture should be treated as:



strong existing storage/evolution/retrieval pipeline;



active relevance ranking/compression/budget pipeline;



partially integrated graph;



weak provenance;



no RAW→typed-derived compiler;



no memory trust boundary.


# PASS 1E — FINAL ADVERSARIAL VERIFICATION

STATUS = COMPLETE / VERIFIED

A = CONFIRMED
MemoryOrchestratorV2 — основной production memory orchestrator.
Узкий direct semantic_memory.search_by_text fallback не является вторым orchestrator.

B = CONFIRMED
AttentionMemory → SemanticCompressor → ContextBudgetManager
реально формируют budget_context, который доходит до LLM.

C = CONFIRMED_WITH_LIMITED_IMPACT
SemanticCore.analyze() выполняется production-маршрутом.
Graph relations попадают в budget_context как контекст,
но не управляют ranking/routing.

D = CONFIRMED
L1 Passport существует, но напрямую не входит
в MemoryOrchestratorV2.build_memory_packet().

E = PARTIALLY_REFUTED
CatalogSearchBridge НЕ DEAD.
Он ACTIVE через SearchDepartment отдельным search path,
но НЕ является частью primary memory_packet pipeline.

F = NO
Сильного provenance / chain-of-custody до immutable RAW нет.
Нет source_path, derived_from и reader цепочки происхождения.

G = NO
Typed DKI, factual confidence, trust/quarantine,
source_path и derived_from в production не реализованы.

H = NO
media.fragment записывается, но production consumer не найден.

I = NO
Единственный физический writer MEMORY_INDEX.jsonl:
SemanticMemory._append_record().

J = NO
Agent Core не получает independent persistent Butler Memory
до первого tool call.

FINAL BASELINE:

LOGICAL_MEMORY_LEVEL_COUNT = 6
DIRECT_BUILD_MEMORY_PACKET_SOURCE_COUNT = 4

MEMORY_BASELINE_15_2_STATUS = FROZEN / VERIFIED
SAFE_TO_FREEZE_MEMORY_BASELINE_15_2 = YES

SECOND_MEMORY_REQUIRED = NO
SECOND_INDEX_REQUIRED = NO
SECOND_GRAPH_REQUIRED = NO
SECOND_ORCHESTRATOR_REQUIRED = NO

FIRST_REAL_MISSING_LINK:

immutable RAW
-> compile / classify / trust
-> typed DerivedKnowledgeItem
-> existing SemanticMemory / MEMORY_INDEX
-> existing Butler retrieval

NEXT STEP:
Freeze final DerivedKnowledgeItem contract.
После этого — минимальное ТЗ RAW Voice Inbox -> DKI -> existing SemanticMemory.

PASS 1 / 1B / 1C / 1D / 1E больше не повторять,
если production-код памяти существенно не изменился.

---

# DKI CONTRACT v1.0 — FROZEN

STATUS=APPROVED
DATE=2026-07-27

PURPOSE:
DerivedKnowledgeItem (DKI) is the typed, provenance-backed derived
knowledge representation for Butler Memory 15.2.

DKI does NOT create a second memory, index, graph, or storage.
Persistence target remains:
SemanticMemory -> MEMORY_INDEX.jsonl

CONTRACT:

IDENTITY
- knowledge_id: existing stable knowledge identifier.

KNOWLEDGE
- type: FACT | PREFERENCE | IDEA | DECISION | QUESTION |
        TASK_CANDIDATE | PROJECT_FACT | other approved semantic types.
- value: derived knowledge content.
- entities: existing entities[].
- version: existing version mechanism.

PROVENANCE
- source: source/provenance identifier.
- source_path: immutable RAW source path.
- source_fragment: exact relevant fragment of RAW source.
- derived_from: immediate source identifier(s).

RELATIONS
- relations[]:
    - type
    - target
    - evidence
- evidence in v1 references source + source_fragment.

SAFETY / LIFECYCLE
- confidence: factual extraction confidence 0..1.
  MUST NOT reuse attention.score.
- trust: trust classification of derived knowledge/source.
- needs_review: existing review mechanism is reused.
- lifecycle: ACTIVE | SUPERSEDED | REJECTED | CONFLICTED.

RULES:
1. RAW SOURCE is immutable.
2. DKI never replaces or modifies RAW SOURCE.
3. DKI is stored through existing SemanticMemory.
4. MEMORY_INDEX.jsonl remains the single DKI persistence target.
5. No second memory store.
6. No second index.
7. No second graph.
8. Relation and lifecycle are different concepts.
9. needs_review is reused; do not create duplicate confirmation fields.
10. IDEA and TASK_CANDIDATE are NOT execution authorization.
11. Extracted commands from RAW speech are NOT automatically executable.
12. Agent Core remains responsible for execution decisions and authorization.

V1 DECISIONS:
- confidence is produced by the compiler and represents extraction confidence.
- source_path is supplied by the RAW -> DKI bridge/compiler.
- derived_from uses immediate source identifier(s); no complex provenance chain in v1.
- relation evidence uses source + source_fragment; no separate evidence engine in v1.

DKI_CAN_LIVE_IN_MEMORY_INDEX=YES
REQUIRES_SECOND_STORAGE=NO
REQUIRES_SECOND_INDEX=NO
REQUIRES_SECOND_GRAPH=NO
BACKWARD_COMPATIBLE_EXTENSION_POSSIBLE=YES

NEXT_STEP:
READ ONLY design of the minimal:
Voice Inbox RAW -> DKI -> existing SemanticMemory -> MEMORY_INDEX.jsonl bridge.

END DKI CONTRACT v1.0
