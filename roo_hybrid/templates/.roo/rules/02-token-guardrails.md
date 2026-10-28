# Triple-Layer Token Efficiency & CLI Guardrails

## 1. File Inspection & Exploration Order
- **Exploration Priority**: Always check `.agents/MAP.md` -> `codebase_search` (Local RAG `nomic-embed-text`) / `search_files` -> sliced `read_file`. Use `graphify-out/wiki/index.md` for cross-module architecture.
- **Sliced Viewing Only**: NEVER read entire large files. Always limit `read_file` ranges to a maximum of **100 lines** focused on the target function or class.
- **Lazy Skill Loading**: Do not load all `.agents/skills/*/SKILL.md` files upfront. Read only the specific `SKILL.md` relevant to the active task.

## 2. Terminal & CLI Guardrails (RTK Emulation)
- **Quiet Flags**: Always enforce quiet/summary flags (`python -m py_compile`, `pytest -q`, `git status -s`, `git diff --stat`, `pip -q`).
- **Output Compression**: Pipe verbose CLI outputs (`Select -First 20`, `Select-String`, `findstr`) or redirect to temporary scratch logs and inspect tails only.
- **No Shell File Dumps**: Never use `cat`, `type`, or `Get-Content` to read source files; use native `read_file` with line limits.
- **Git Safety**: NEVER run `git commit` or `git push` automatically unless explicitly requested.

## 3. Bilingual Token Optimization (English Bridge Pipeline)
- When calling external reasoning tools (`openrouter:tanya_openrouter` or `hermes_agent:delegasikan_ke_hermes`), compress the technical prompt into dense **English** (max 50-200 lines of distilled context) to save 30%-50% BPE tokens, then translate the synthesized answer back into **Indonesian** for the user.

