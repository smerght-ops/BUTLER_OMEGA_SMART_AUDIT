# BUTLER STRICT MODULE PIPELINE

Status: MANDATORY
Scope: every new module, every module update, every integration.

## Golden Rule

No module is allowed into the project tree until it passes the full strict pipeline.

## Mandatory Pipeline

1. Create or update module only in laboratory:
   - `A_00_AVARIYKA`

2. Run laboratory syntax check:
   - `python -m py_compile <LAB_FILE>`

3. Run laboratory execution test:
   - `python <LAB_FILE>`

4. Stop immediately on any error:
   - no continuation
   - no fake green `[OK]`
   - no integration

5. Integrate into project tree only after LAB success.

6. Run project syntax check:
   - `python -m py_compile <PROJECT_FILE>`

7. Run import test:
   - `python -c "from <PROJECT_MODULE> import <CLASS>; print('IMPORT OK')"`

8. Run Guardian:
   - `python RUN_PIPELINE_V12.py --self-test`

9. Print final `[OK]` only after every previous step succeeded.

## Forbidden

- No naked Python pasted into PowerShell.
- No manual file edits during integration.
- No fake modules just to fill wave numbers.
- No multiple new modules inside one construction block.
- No final `[OK]` after any previous failure.
- No assumptions about paths.
- No integration from outside project root unless block auto-detects root.

## Required PowerShell Pattern

Every construction block must be self-contained:

- auto-root to `BUTLER_OMEGA`;
- create/update LAB file;
- compile LAB file;
- execute LAB file;
- copy to project;
- compile project file;
- import project module;
- run Guardian;
- only then print `[OK]`.

## Current Proven Components

The strict pipeline has successfully handled:

- AutonomousLoop
- MemoryLoop
- demo cleanup after 3L / 3M
- Guardian validation after integration

## Rule

If a module does not pass this pipeline, it does not exist as a valid Butler Omega component.
