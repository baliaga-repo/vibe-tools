---
trigger: always_on
description: Universal token efficiency guardrails, sliced viewing policies, and terminal command compression standards.
---

# Universal Token Efficiency & CLI Guardrails

This guide defines strict standards to prevent token bloat across all AI pair programming sessions.

## 1. File Inspection & Context Limits
- **Sliced Viewing Only**: Never load entire large files. Strictly use sliced `view_file` with `StartLine`/`EndLine` ranges limited to maximum 100 lines focused on the target function.
- **Minimal Context**: Focus strictly on target files; avoid scanning unrelated directories.
- **Exploration Order**: Prioritize `.agents/MAP.md` -> `grep_search` -> sliced `view_file`. Use `graphify-out/wiki/` only for cross-module relationships.

## 2. Terminal & CLI Guardrails (RTK Emulation)
- **Compress Terminal Outputs**: Pipe command outputs to prevent terminal stdout noise (e.g. `Select -First 20`, `Select-String`, or `findstr`).
- **Enforce Quiet Flags**: Always include quiet or summary flags for commands (`pip -q`, `git status -s`, `git diff --stat`, `pytest -q`).
- **Redirect Verbose Logs**: Redirect large outputs to temporary logs in scratch directories and inspect only tails (`> scratch/tmp.log 2>&1; Get-Content ... -Tail 10`).
- **Sentinel Checks**: Prefer boolean checks (`Test-Path`, `(Get-ChildItem).Count`, exit codes) over dumping large directory or object listings.
- **No Command File Dumps**: Never dump file contents using shell commands (`cat`, `type`, `Get-Content`). Strictly use native `view_file`.

## 3. Formatting & Communication
- **Direct Unicode Symbols**: Never use LaTeX math notation in responses or code comments. Use direct Unicode symbols (e.g. `->`, `*`, `•`).
- **Concise Summaries**: Deliver direct, actionable technical summaries without redundant conversational filler.
