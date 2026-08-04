
# IMPLEMENTATION INSTRUCTIONS

Project Root

C:\Users\KOS\Desktop\Butler_Agent\BUTLER_OMEGA_SMART

---

## IMPLEMENTATION OBJECTIVE

Implement RepositoryKnowledgeDepartment as a permanent Butler Department.

The implementation shall follow this RFC completely.

The existing Butler architecture is authoritative.

RepositoryKnowledgeDepartment shall integrate into the current architecture rather than replacing it.

---

## ENGINEERING WORKFLOW

Before modifying production code:

1. Study the existing Butler implementation.

2. Identify the current Department registration mechanism.

3. Identify SmartDispatcherV2 integration points.

4. Identify DepartmentExecutionGateway execution flow.

5. Identify Permission Engine execution flow.

6. Reuse existing Butler architectural patterns.

7. Minimize production modifications.

8. Preserve backward compatibility.

9. Produce incremental implementation stages.

10. Validate every stage before continuing.

---

## IMPLEMENTATION RULES

Implementation shall:

Reuse existing Butler components.

Follow current Department conventions.

Preserve repository structure.

Preserve coding style.

Preserve runtime architecture.

Preserve dispatcher architecture.

Preserve gateway architecture.

Preserve permission architecture.

Preserve UTF-8 without BOM.

Produce deterministic behaviour.

---

## REQUIRED OUTPUT

At completion provide:

Implementation Summary

Modified Files

Architecture Summary

Integration Summary

Testing Summary

Engineering Audit

PASS / FAIL Report

Then continue with the RFC below.

---
# RepositoryKnowledgeDepartment RFC v1.0

> STATUS: DRAFT
> Project: BUTLER_OMEGA_SMART
> Purpose: Final engineering specification for Codex implementation.

---

# 1. PURPOSE

RepositoryKnowledgeDepartment is the single engineering knowledge service of Butler.

Its responsibility is to maintain a complete, queryable, structured understanding of the repository.

After implementation every engineering subsystem must obtain repository knowledge through this Department.

RepositoryKnowledgeDepartment becomes the canonical engineering knowledge provider.

---

# 2. DESIGN GOALS

The Department shall:

- understand repository structure;
- understand runtime architecture;
- understand registration chains;
- understand dependency chains;
- understand execution chains;
- understand project categories;
- answer engineering queries;
- build reusable repository indexes;
- eliminate repeated repository scanning.

---

# 3. NON GOALS

RepositoryKnowledgeDepartment is not:

- a file editor;
- a project formatter;
- a Git client;
- an architecture modifier;
- a code generator;
- a deployment system;
- a filesystem manager.

It never changes the repository.

It only observes, indexes and answers.

---

# 4. ARCHITECTURAL POSITION

User

↓

Coordinator

↓

Dispatcher

↓

ButlerHarness

↓

DepartmentExecutionGateway

↓

RepositoryKnowledgeDepartment

↓

Repository Index

↓

Engineering Queries

RepositoryKnowledgeDepartment never bypasses Butler architecture.

---

# 5. SINGLE SOURCE OF ENGINEERING KNOWLEDGE

After implementation no Butler subsystem may independently scan the repository when repository knowledge is required.

RepositoryKnowledgeDepartment becomes the only engineering knowledge provider.

All future engineering services consume RepositoryKnowledgeDepartment.

---

# 6. PRIMARY RESPONSIBILITIES

Repository scanning.

Repository indexing.

Repository graph construction.

Dependency analysis.

Runtime analysis.

Registration analysis.

Duplicate analysis.

Architecture reporting.

Engineering query processing.

Knowledge caching.

---

# 7. ENGINEERING PRINCIPLES

Read Only.

Deterministic.

Repeatable.

Observable.

Cacheable.

Thread Safe.

Architecture Neutral.

UTF-8 only.

No BOM.

No hidden mutations.

No side effects.

---

# END OF BLOCK 1

# 8. ENGINEERING DATA SOURCES

RepositoryKnowledgeDepartment shall build its knowledge only from approved engineering sources.

Primary sources:

PROJECT_SCOPE.yaml

system_manifest.json

A_00_ARCHITECTURE\RECONSTRUCTION_INVENTORY.json

Repository tree.

Python modules.

Runtime registrations.

Imports.

No external repositories.

No Internet.

No Git history.

No hidden metadata.

---

# 9. INTERNAL ARCHITECTURE

RepositoryKnowledgeDepartment shall consist of the following internal services.

RepositoryKnowledgeDepartment

↓

RepositoryScanner

↓

ScopeResolver

↓

ManifestLoader

↓

InventoryLoader

↓

RegistrationAnalyzer

↓

ImportAnalyzer

↓

RuntimeAnalyzer

↓

DependencyAnalyzer

↓

DuplicateDetector

↓

ProjectGraphBuilder

↓

IndexBuilder

↓

QueryEngine

↓

ArchitectureReporter

↓

KnowledgeCache

Each service has a single responsibility.

No service may duplicate another service's responsibility.

---

# 10. INTERNAL KNOWLEDGE MODEL

The Department maintains one engineering model.

The model contains:

Departments

Managers

Handlers

Engines

Coordinators

Gateways

Interfaces

Storage

Configuration

Runtime Nodes

Imports

Registrations

Dependencies

Ownership

Execution Chains

Permission Chains

Duplicate Groups

Project Categories

Documentation Nodes

Every object shall possess a stable internal identifier.

---

# 11. PROJECT GRAPH

RepositoryKnowledgeDepartment shall construct a directed graph.

Supported node types:

Department

Manager

Core

Gateway

Interface

Storage

Configuration

Documentation

Tests

Handlers

Supported edge types:

imports

uses

owns

calls

registers

creates

depends_on

inherits

executes

contains

runtime

permission

Every edge shall preserve source location.

---

# 12. INDEX

The Department builds one reusable repository index.

The index stores:

Node identifiers

Edge identifiers

File locations

Class locations

Function locations

Import map

Registration map

Execution map

Runtime map

Permission map

Category map

Duplicate map

The index is immutable between rebuild operations.

---

# 13. CACHE POLICY

Cold Build

↓

Repository Index

↓

Memory Cache

↓

Read Operations

↓

Explicit Refresh

↓

New Repository Index

No automatic rescanning during ordinary queries.

---

# 14. SOURCE LOADING

PROJECT_SCOPE.yaml

↓

ScopeResolver

system_manifest.json

↓

ManifestLoader

RECONSTRUCTION_INVENTORY.json

↓

InventoryLoader

Every loader returns structured data.

Every loader validates UTF-8.

Every loader reports diagnostics.

No loader modifies source files.

---

# END OF BLOCK 2


# 15. PUBLIC API

RepositoryKnowledgeDepartment shall expose the following public operations.

build_index()

refresh_index()

query()

find_department()

find_manager()

find_class()

find_function()

find_import()

find_registration()

find_runtime()

find_dependency()

find_duplicates()

find_execution_chain()

find_permission_chain()

build_project_graph()

build_dependency_graph()

build_runtime_graph()

build_architecture_report()

Every public operation returns structured data.

No public operation performs repository modification.

---

# 16. QUERY CONTRACT

Every engineering query shall execute against the internal index.

Supported engineering queries include:

Find Department

Find Manager

Find Registration

Find Import

Find Runtime

Find Dependency

Find Duplicate

Find Execution Chain

Find Permission Chain

Find Owner

Find Category

Find Entry Point

Find Gateway Usage

Find ButlerHarness Usage

Find Dispatcher Usage

Find Coordinator Usage

Repository traversal during ordinary query execution is prohibited.

---

# 17. DUPLICATE DETECTION

Duplicate detection shall identify:

Duplicate Departments

Duplicate Classes

Duplicate Functions

Duplicate Imports

Duplicate Registrations

Duplicate Runtime Paths

Duplicate Entry Points

Duplicate Execution Chains

Duplicate Permission Chains

Duplicate Managers

Each duplicate shall include:

Identifier

Location

Reason

Evidence

Confidence

---

# 18. DEPENDENCY ANALYSIS

Dependency analysis shall identify:

Imports

Inheritance

Composition

Runtime Calls

Registration Dependencies

Gateway Dependencies

Permission Dependencies

Storage Dependencies

Interface Dependencies

Circular Dependencies

Dead Dependencies

Broken Dependencies

Unused Dependencies

---

# 19. RUNTIME ANALYSIS

RepositoryKnowledgeDepartment shall reconstruct runtime execution.

Supported runtime nodes:

User

BUTLER_OS

Coordinator

Dispatcher

ButlerHarness

DepartmentExecutionGateway

Department

Internal Service

Result

Supported runtime edges:

Dispatch

Gateway

Permission

Execution

Return

Nested Execution

---

# 20. REGISTRATION ANALYSIS

RepositoryKnowledgeDepartment shall identify:

Registered Departments

Unregistered Departments

Duplicate Registrations

Broken Registrations

Missing Registrations

Registration Source Files

Registration Locations

Registration Relationships

Registration Ownership

---

# 21. IMPORT ANALYSIS

RepositoryKnowledgeDepartment shall construct:

Complete Import Graph

Reverse Import Graph

Unused Imports

Broken Imports

Circular Imports

Import Owners

Import Sources

Import Targets

Import Statistics

---

# END OF BLOCK 3


# 22. ARCHITECTURE REPORTS

RepositoryKnowledgeDepartment shall generate structured engineering reports.

Supported reports:

Production Components

Engineering Components

Workspace Components

Laboratory Components

Archive Components

Generated Components

Ignored Components

Runtime Entry Points

Execution Chains

Permission Chains

Duplicate Components

Dependency Summary

Import Summary

Registration Summary

Architecture Health

Repository Statistics

Every report shall be generated from the repository index.

No report shall perform an independent repository scan.

---

# 23. ARCHITECTURE VALIDATION

RepositoryKnowledgeDepartment shall automatically validate:

Missing Departments

Missing Registrations

Broken Runtime Chains

Broken Gateway Usage

Broken Permission Paths

Broken Imports

Circular Imports

Circular Dependencies

Dead Components

Unreachable Components

Duplicate Components

Duplicate Registrations

Duplicate Runtime Paths

Missing Runtime Entry Points

Orphan Components

Every validation result shall include:

Severity

Evidence

Affected Components

Suggested Engineering Action

---

# 24. PERFORMANCE REQUIREMENTS

Repository scan shall occur only during:

Initial Index Build

Explicit Refresh

Repository Version Change

All engineering queries shall execute against the in-memory index.

Repeated project traversal is prohibited.

The Department shall minimize filesystem access after index creation.

---

# 25. FAULT TOLERANCE

RepositoryKnowledgeDepartment shall continue operating when one or more engineering sources are unavailable.

Supported degraded modes:

PROJECT_SCOPE unavailable

system_manifest unavailable

RECONSTRUCTION_INVENTORY unavailable

Partial repository scan

Empty index

Each degraded mode shall provide:

Status

Reason

Diagnostics

Unavailable functionality

Recovery recommendation

No unexpected exception shall terminate Department execution.

---

# 26. OBSERVABILITY

Every operation shall be observable through Butler's existing Observation Layer.

Operations to record:

Index Build

Index Refresh

Repository Scan

Query Execution

Report Generation

Duplicate Detection

Dependency Analysis

Runtime Analysis

Validation

No additional logging framework shall be introduced.

---

# 27. SECURITY

RepositoryKnowledgeDepartment operates in read-only mode.

It shall never:

Modify repository files

Execute Git operations

Rewrite YAML

Rewrite JSON

Rewrite Python

Delete files

Rename files

Move files

Create engineering decisions

Its responsibility ends with structured engineering knowledge.

---

# 28. VERSIONING

RepositoryKnowledgeDepartment maintains:

Schema Version

Index Version

Repository Version

Build Timestamp

Git Commit Identifier

PROJECT_SCOPE Version

RECONSTRUCTION_INVENTORY Version

system_manifest Version

Version information shall accompany every generated report.

---

# END OF BLOCK 4


# 29. INTEGRATION CONTRACT

RepositoryKnowledgeDepartment shall integrate into Butler only through existing production mechanisms.

Integration points:

Department Registry

SmartDispatcherV2

ButlerHarness

DepartmentExecutionGateway

Permission Engine

Observation Layer

No alternative execution paths shall be introduced.

No dedicated launcher shall be introduced.

No custom dispatcher shall be introduced.

No parallel routing system shall be introduced.

---

# 30. ENGINEERING INVARIANTS

The following rules are permanent architecture invariants.

RepositoryKnowledgeDepartment is the only engineering knowledge provider.

Repository scanning belongs exclusively to RepositoryKnowledgeDepartment.

Engineering knowledge shall never be duplicated.

Project classification shall originate only from PROJECT_SCOPE.yaml.

Runtime knowledge shall originate only from repository analysis.

Every engineering consumer shall consume structured knowledge instead of performing repository traversal.

Architecture shall remain deterministic.

Every engineering result shall be reproducible.

---

# 31. FUTURE CONSUMERS

RepositoryKnowledgeDepartment is the canonical provider for:

Architecture Inspector

Repository Audit

Architecture Guardian

Permission Guardian

Project Reconstruction

Project Indexer

Repository Explorer

Future AI Architect

Future Butler Departments

Engineering Dashboard

Knowledge Console

Engineering Reports

Any future engineering subsystem requiring repository knowledge.

---

# 32. EXTENSIBILITY

Future extensions shall be implemented by introducing internal services.

The public Department interface shall remain stable.

New functionality shall not require architectural redesign.

RepositoryKnowledgeDepartment shall remain backwards compatible whenever possible.

---

# 33. TEST REQUIREMENTS

Mandatory tests:

Load PROJECT_SCOPE.yaml

Load system_manifest.json

Load RECONSTRUCTION_INVENTORY.json

Repository Scan

Index Build

Index Refresh

Query Execution

Project Graph

Dependency Graph

Runtime Graph

Duplicate Detection

Registration Analysis

Import Analysis

Architecture Report

Gateway Execution

Permission Execution

Dispatcher Integration

Observation Integration

UTF-8 Validation

PyCompile Validation

All tests shall execute successfully before PASS.

---

# 34. ACCEPTANCE CRITERIA

PASS is possible only when:

RepositoryKnowledgeDepartment is implemented.

Department is registered.

Dispatcher routes requests correctly.

Gateway executes correctly.

Permission Engine participates correctly.

Observation Layer records execution.

Repository index builds successfully.

Repeated queries reuse the index.

Repository graph is generated.

Dependency graph is generated.

Runtime graph is generated.

Duplicate detection operates.

Architecture reports operate.

Query API operates.

No production architecture regression is introduced.

All modified Python files pass py_compile.

All text files are UTF-8 without BOM.

---

# 35. FINAL ARCHITECTURE AUDIT

Before completion perform a complete engineering audit.

The audit shall verify:

Architecture Integrity

Registration Integrity

Gateway Integrity

Permission Integrity

Dispatcher Integrity

Runtime Integrity

Dependency Integrity

Import Integrity

Duplicate Integrity

Repository Index Integrity

Engineering Knowledge Integrity

Project Graph Integrity

Execution Chain Integrity

UTF-8 Integrity

PyCompile Integrity

Test Integrity

The implementation is accepted only after the complete audit reports PASS.

---

# END OF RFC

RepositoryKnowledgeDepartment RFC v1.0

FINAL SPECIFICATION


# 36. INTERNAL INDEX SPECIFICATION

RepositoryKnowledgeDepartment shall maintain a single in-memory engineering index.

The index is the canonical engineering representation of the repository.

The index shall contain independent collections.

Departments

Managers

Handlers

Engines

Gateways

Interfaces

Storage

Configuration

Runtime Nodes

Documentation

Tests

Classes

Functions

Imports

Registrations

Dependencies

Execution Chains

Permission Chains

Categories

Duplicate Groups

Every indexed object shall contain:

Unique Identifier

Name

Type

Category

Source File

Source Line

Owner

Runtime Status

Registration Status

Dependencies

Reverse Dependencies

Metadata

Every object shall be addressable through its unique identifier.

---

# 37. INDEX LIFECYCLE

RepositoryKnowledgeDepartment shall support the following lifecycle.

Repository Scan

↓

Raw Repository Model

↓

Normalized Repository Model

↓

Knowledge Index

↓

Validation

↓

Published Index

↓

Query Operations

↓

Explicit Refresh

Index publication shall be atomic.

A partially built index shall never become visible.

---

# 38. REPOSITORY SCANNER

RepositoryScanner is responsible only for repository discovery.

Responsibilities:

Directory Traversal

Python Discovery

YAML Discovery

JSON Discovery

Markdown Discovery

Runtime Metadata Discovery

Scanner never performs:

Classification

Dependency Analysis

Duplicate Detection

Report Generation

Scanner output becomes input for IndexBuilder.

---

# 39. SCOPE RESOLVER

ScopeResolver shall interpret PROJECT_SCOPE.yaml.

Responsibilities:

Resolve Categories

Resolve Ignore Rules

Resolve Generated Rules

Resolve Archive Rules

Resolve Production Rules

Resolve Workspace Rules

Resolve Laboratory Rules

Resolve Engineering Rules

Every classification decision shall preserve its source.

No inferred classification may overwrite an explicit PROJECT_SCOPE rule.

---

# 40. MANIFEST LOADER

ManifestLoader shall load:

system_manifest.json

Responsibilities:

Validate structure

Validate encoding

Load active paths

Load path aliases

Load runtime directories

Expose normalized manifest model

No modification is permitted.

---

# 41. INVENTORY LOADER

InventoryLoader shall load:

RECONSTRUCTION_INVENTORY.json

Responsibilities:

Load discovered files

Load discovered components

Load discovered relationships

Load duplicate information

Load reconstruction metadata

Normalize inventory model

Inventory shall remain read-only.

---

# 42. INDEX BUILDER

IndexBuilder receives normalized models.

Responsibilities:

Merge sources

Assign identifiers

Resolve references

Resolve ownership

Resolve registrations

Resolve imports

Resolve runtime nodes

Resolve dependency nodes

Produce immutable repository index.

---

# END OF BLOCK 5


# 43. QUERY ENGINE

QueryEngine is responsible for all engineering queries.

Supported operations:

find_department(name)

find_manager(name)

find_handler(name)

find_engine(name)

find_class(name)

find_function(name)

find_import(name)

find_registration(name)

find_runtime(name)

find_dependency(name)

find_duplicates(name)

find_owner(name)

find_category(name)

find_execution_chain(name)

find_permission_chain(name)

find_entry_point(name)

All queries execute exclusively against the published index.

---

# 44. QUERY RESULT CONTRACT

Every query returns a structured response.

Mandatory fields:

success

query

timestamp

index_version

matches

diagnostics

Each match shall contain:

identifier

name

type

category

file

line

owner

confidence

related_nodes

related_edges

---

# 45. PROJECT GRAPH CONTRACT

ProjectGraph shall expose:

Nodes

Edges

Adjacency Map

Reverse Adjacency Map

Connected Components

Root Nodes

Leaf Nodes

Node Types

Edge Types

Traversal API

Every node shall be uniquely addressable.

---

# 46. DEPENDENCY GRAPH CONTRACT

DependencyGraph shall include:

Import Dependencies

Runtime Dependencies

Registration Dependencies

Ownership Dependencies

Permission Dependencies

Inheritance Dependencies

Composition Dependencies

Reverse Dependencies

Circular Dependency Detection

Unused Dependency Detection

Broken Dependency Detection

---

# 47. RUNTIME GRAPH CONTRACT

RuntimeGraph shall reconstruct execution paths.

Supported runtime nodes:

User

ButlerOS

Coordinator

Dispatcher

Harness

DepartmentExecutionGateway

Department

Internal Service

External Service

Result

Supported runtime edges:

dispatch

execute

permission

return

nested_call

ownership

---

# 48. DUPLICATE DETECTOR

DuplicateDetector shall detect:

Duplicate Departments

Duplicate Managers

Duplicate Classes

Duplicate Functions

Duplicate Imports

Duplicate Registrations

Duplicate Runtime Chains

Duplicate Entry Points

Duplicate Configuration

Duplicate Documentation

Every duplicate shall contain evidence.

---

# 49. ARCHITECTURE HEALTH

RepositoryKnowledgeDepartment shall calculate:

Repository Health Score

Registration Health

Dependency Health

Runtime Health

Import Health

Permission Health

Architecture Stability

Duplicate Density

Index Freshness

Repository Completeness

Health reports shall be reproducible.

---

# 50. ENGINEERING DIAGNOSTICS

Every operation shall produce diagnostics.

Diagnostics include:

Operation

Duration

Input

Output

Warnings

Errors

Statistics

Index Version

Repository Version

Diagnostics shall never interrupt execution.

---

# END OF BLOCK 6


# 51. ENGINEERING API CONTRACT

RepositoryKnowledgeDepartment shall expose a stable engineering API.

Every public method shall:

Validate input

Use published repository index

Return structured result

Never mutate repository

Never rebuild index unless explicitly requested

Every public method shall be deterministic.

---

# 52. ENGINEERING RESULT MODEL

Every engineering operation returns:

success

operation

timestamp

repository_version

index_version

execution_time_ms

data

diagnostics

warnings

errors

No operation shall return anonymous structures.

---

# 53. REPOSITORY MODEL

RepositoryKnowledgeDepartment shall internally model:

Repository

↓

Categories

↓

Directories

↓

Files

↓

Modules

↓

Classes

↓

Functions

↓

Registrations

↓

Runtime Objects

↓

Execution Graph

↓

Dependency Graph

↓

Knowledge Index

Every layer shall preserve traceability to original source files.

---

# 54. COMPONENT IDENTIFIERS

Every discovered engineering component shall possess:

Component ID

Component Type

Component Name

Repository Path

Relative Path

Module

Owner

Category

Registration Status

Runtime Status

Source Hash

Discovery Timestamp

These identifiers remain stable until explicit index rebuild.

---

# 55. CLASSIFICATION MODEL

Classification sources in descending priority:

PROJECT_SCOPE.yaml

↓

system_manifest.json

↓

Repository Structure

↓

Python Metadata

↓

Engineering Heuristics

Explicit classifications always override inferred classifications.

Inference shall never overwrite explicit engineering metadata.

---

# 56. ENGINEERING RELATIONSHIPS

RepositoryKnowledgeDepartment shall maintain:

Imports

Imported By

Calls

Called By

Creates

Created By

Registers

Registered By

Owns

Owned By

Depends On

Required By

Permission Flow

Execution Flow

Runtime Flow

Every relationship shall reference both endpoints.

---

# 57. ENGINEERING SEARCH

Supported searches:

Exact Match

Prefix Match

Suffix Match

Contains

Regular Expression

Type Filter

Category Filter

Owner Filter

Registration Filter

Runtime Filter

Dependency Filter

Results shall be ranked by engineering relevance.

---

# 58. ENGINEERING STATISTICS

RepositoryKnowledgeDepartment shall calculate:

Department Count

Manager Count

Gateway Count

Handler Count

Core Count

Engine Count

Configuration Count

Documentation Count

Runtime Count

Dependency Count

Import Count

Registration Count

Duplicate Count

Repository Size

Statistics shall be generated from the published index.

---

# END OF BLOCK 7


# 59. IMPLEMENTATION STAGES

Implementation shall be performed in sequential stages.

Stage 1

Department Skeleton

↓

Stage 2

Source Loaders

↓

Stage 3

Repository Scanner

↓

Stage 4

Normalized Repository Model

↓

Stage 5

Index Builder

↓

Stage 6

Query Engine

↓

Stage 7

Project Graph

↓

Stage 8

Dependency Graph

↓

Stage 9

Runtime Graph

↓

Stage 10

Duplicate Detection

↓

Stage 11

Architecture Reports

↓

Stage 12

Dispatcher Integration

↓

Stage 13

Gateway Validation

↓

Stage 14

Observation Validation

↓

Stage 15

Engineering Audit

Every stage shall finish with PASS before the next stage begins.

---

# 60. MODIFICATION POLICY

RepositoryKnowledgeDepartment implementation shall minimize production changes.

Priority:

1. New Department implementation.

2. Registration.

3. Dispatcher integration.

4. Gateway integration.

5. Tests.

No unrelated production files shall be modified.

Every modification shall have a documented engineering reason.

---

# 61. FILE MODIFICATION MATRIX

Primary implementation files:

A_04_AGENTS/RepositoryKnowledgeDepartment/*

Integration files:

department_registry.py

smart_dispatcher_v2.py

DepartmentExecutionGateway integration (only if required by existing architecture)

Test files:

A_09_TESTS/*

Documentation:

PROJECT_SCOPE.yaml shall remain read-only.

system_manifest.json shall remain read-only.

RECONSTRUCTION_INVENTORY.json shall remain read-only.

---

# 62. ENGINEERING COMPLIANCE

Implementation shall comply with:

Existing Butler architecture

Existing Department lifecycle

Existing Dispatcher lifecycle

Existing Permission lifecycle

Existing Observation lifecycle

Existing PowerShell engineering policy

UTF-8 without BOM

RepositoryKnowledgeDepartment shall integrate into Butler rather than introducing a parallel architecture.

---

# 63. FINAL DELIVERABLES

Implementation shall provide:

RepositoryKnowledgeDepartment

Repository Scanner

Index Builder

Query Engine

Project Graph

Dependency Graph

Runtime Graph

Duplicate Detector

Architecture Reporter

Integration

Tests

Engineering Documentation

Audit Report

PASS Report

RepositoryKnowledgeDepartment shall become a permanent Butler subsystem.

---

# 64. CODEX EXECUTION REQUIREMENTS

Before modifying production code, inspect the current implementation and identify the existing registration, dispatch, gateway, and permission patterns.

Reuse existing Butler mechanisms wherever applicable.

Maintain architectural consistency with existing Departments.

After each production-file modification:

- create a point backup;
- verify syntax with py_compile;
- validate runtime integration;
- automatically restore from backup if verification fails;
- provide a manual rollback command.

At completion, produce:

- list of modified files;
- implementation summary;
- integration summary;
- test summary;
- architecture audit summary;
- PASS / FAIL conclusion.

# END OF BLOCK 8

RepositoryKnowledgeDepartment RFC v1.1
FINAL IMPLEMENTATION SPECIFICATION


