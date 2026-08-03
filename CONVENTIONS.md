# CONVENTIONS.md

## 1. Formatting & Environment Standards
### Encoding
All project files must use:
- UTF-8
- No BOM

### Line Endings
All text files must use:
- LF (\n)

### Indentation Consistency
- A file must use one consistent indentation style.
- Automated patch systems must not assume a fixed number of spaces.
- Before any modification an Audit step must verify the actual structure of the target file.


## 2. Terminal Safety Gate
### Multi-Line Python Restriction
- Multi-line automation through `python -c` is prohibited for project modifications.

### Kalashnikov Rule
All automated modifications must follow:
1. Generate temporary isolated `.py` patch file
2. Execute patch
3. Verify result
4. Remove temporary file
- Direct complex inline modification is prohibited.


## 3. Change Management Protocol
Every modification must follow:
1. Audit
2. Contract
3. Rollback Point
4. Minimal Patch
5. `py_compile`
6. Integration Test
- No step may be skipped.

### Rollback Requirement
- Every modified system file must have a timestamped backup before modification.


## 4. Source of Truth
Project state must be determined only from physical project artifacts.
**Approved sources:**
- `project_passport.json`
- `PROJECT_MEMORY_INDEX.json`
- `ButlerOSAdapter`

**Forbidden sources:**
- LLM memory
- Chat history assumptions
- Model-generated project status


## 5. Frozen Core Policy
**Frozen modules:**
- `A_01_CORE`
- `A_03_ORCHESTRATION/chat_router.py`

- Direct modification is prohibited.
- New functionality must be implemented through: Adapters, Handlers, Plugins, Controllers, Harness components.
- Attempts to modify frozen modules must raise a security exception.


## 6. Verification Rule
- A modification is considered complete only after real execution verification.
- File save is not considered proof of success.
- Successful runtime validation is mandatory.


## 7. Harness Readiness Rules
Future Harness systems must not:
- modify Frozen Core
- bypass Rollback Point creation
- bypass `py_compile`
- bypass Integration Test
- rewrite project state without validation
- Harness execution must preserve project invariants at all times.
