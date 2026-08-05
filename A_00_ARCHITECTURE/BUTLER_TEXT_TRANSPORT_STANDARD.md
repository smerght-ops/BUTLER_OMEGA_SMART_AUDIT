# Butler Omega Smart Text Transport Standard

Status: OFFICIAL
Version: BOS-TEXT-TRANSPORT-1.0
Date: 2026-07-10
Scope: safe transfer of large `.md`, `.py`, `.ps1`, `.json`, `.txt`, `.csv`, and other byte-preserved documents through ChatGPT into PowerShell.

## Purpose

Butler Omega Smart must never rely on direct large here-string pastes for important files. The official transport must preserve bytes exactly, including UTF-8, Markdown, Python, PowerShell, JSON, Russian text, `$`, backticks, braces, brackets, and Unicode.

## Research Basis

Research script: `A_00_UTILS/butler_transport_research.py`
Report: `A_06_WORKSPACE/AUDITS/BUTLER_TEXT_TRANSPORT_RESEARCH_20260710_112159.md`
Fixtures: real Butler PowerShell, Python, Markdown, and JSON mixed into 300, 500, and 1000 line test files.

Verification method:

- reconstruct through PowerShell;
- compare byte count;
- compare SHA256;
- reject any newline, encoding, or character change.

## Results

| Method | Reliability | Max experimentally verified size | UTF-8 | Speed | Automation | Recovery |
| --- | --- | --- | --- | --- | --- | --- |
| A. Short here-string + Set/Add-Content | Failed SHA256 on 300/500/1000 lines | 0 verified lines | Not byte-safe | Medium | Medium | Weak |
| B. Array of lines + Set-Content | Failed on 300/500/1000 lines | 0 verified lines | Not byte-safe | Fast | Medium | Weak |
| C. Base64 raw bytes | Passed 300/500/1000 lines | 1000 verified lines, 51,858 byte script | Byte-safe | Fast | High | Medium |
| D. GZip + Base64 raw bytes | Passed 300/500/1000 lines | 1000 verified lines, 14,788 byte script | Byte-safe | Medium | High | Medium |
| Official chunked GZip + Base64 | Passed real 92,612 byte Markdown and 784,094 byte Markdown | 784,094 bytes verified, multi-block tested | Byte-safe | Medium | Highest | Strong, resend one block |

## Official Standard

The official Butler transport is:

```text
original bytes
-> GZip
-> Base64
-> small PowerShell blocks
-> per-block SHA256
-> assemble.ps1
-> final SHA256
-> WriteAllBytes
```

Default block size: `8000` Base64 characters.
Reason: this is deliberately smaller than the larger locally verified block sizes and is safer for manual ChatGPT-to-PowerShell transfer.

## Rules

1. Do not paste large real documents as here-strings.
2. Do not use `Set-Content` or `Add-Content` for byte-critical reconstruction.
3. Use Base64 only as a byte transport, never as decoded text.
4. Use `WriteAllBytes` for final output.
5. Every block must have SHA256 verification.
6. Final assembled file must match original SHA256.
7. If one block is damaged, resend only that block.

## Implementation

Utility:

```text
A_00_UTILS/butler_transport.py
```

Package a file:

```powershell
$PY = Get-Content .\.butler_python_path
& $PY A_00_UTILS\butler_transport.py pack INSPECTOR_PIPELINE.md --out-dir A_06_WORKSPACE\TRANSPORT_OUT\INSPECTOR_PIPELINE
```

The generator creates:

```text
manifest.json
block_001.ps1
block_002.ps1
...
assemble.ps1
README.md
```

On the receiving side:

```powershell
powershell -ExecutionPolicy Bypass -File .\block_001.ps1
powershell -ExecutionPolicy Bypass -File .\block_002.ps1
powershell -ExecutionPolicy Bypass -File .\block_003.ps1
powershell -ExecutionPolicy Bypass -File .\assemble.ps1
```

Verify manually if needed:

```powershell
$PY = Get-Content .\.butler_python_path
& $PY A_00_UTILS\butler_transport.py verify ORIGINAL_FILE RESTORED_FILE
```

## Recovery

If a block is damaged, PowerShell stops with:

```text
Chunk SHA256 mismatch
```

Action:

1. Do not rerun previous accepted blocks.
2. Regenerate or resend only the damaged `block_NNN.ps1`.
3. Run that block again.
4. Run `assemble.ps1`.

## Final Decision

Butler Omega Smart standardizes on chunked `GZip + Base64 + SHA256 + WriteAllBytes`.

This is the only approved transport for large or critical files transferred through ChatGPT into PowerShell.
