---
trigger: always_on
description: Concise universal vibe-coding rules, /swarm auto-model orchestration, Claude budget guardrails, Ponytail 250-line threshold, vibe_tools hygiene, and YAML frontmatter guardrails.
---

# Universal Self-Learning Core Rules (Lightweight Always-On)

> **Deep Bug Archive (28 Patterns, On-Demand)**: Never paste domain bug notes here. Grep & read only the needed slice in `vibe_tools/references/self-learning-patterns.md` (SQLite ETL, CUDA DLLs, Qt6/QMovie, NLE SDK, ASR/24-bit PCM, scrapers).

***

## 1. Golden 2-Prompt Feature Flow (`/swarm` Dual-Orchestrator)
1. **Stage 1 — Consultation & `/grill-me` (Read-Only, Anti-Sycophancy)**: Coordinator (`Gemini 4 Neon High` / `Orchestrator Neon` or `Orchestrator Argon` / `Argon High`) scouts slices, fires **Brain Shot #1** (blindspots + sharpest questions, auto-`kill`), runs `ask_question` one-by-one, writes draft `.md`, and prints raw-link auto-reminder prompts. **No `.py` edits**.
2. **Stage 2+3 Combined (Default 1-Shot)**: On approval, Coordinator fires **Brain Shot #2** (contract, callers, & test oracle, auto-`kill`), writes `docs/specs/0XX_*.md`, updates `docs/INDEX.md`, generates `docs/tickets/0XX_*/`, and executes all tickets sequentially with Triple-Gate (`Zero-Omission` + `py_compile`/`pyflakes` + smoke test) via Gemini (`Neon` / `Argon` for `> 250 lines`). *(Allow Stage 2-only split when requested.)*

## 2. `/swarm` Dual-Orchestrator & 3-Pool Quota Guardrails
- **3 Quota Pools**: **Pool 1 (Daily):** `Orchestrator (Neon)` / `Gemini 4 Neon (High)` (default Coordinator); **Pool 2 (Weekly 7d):** `Orchestrator (Argon)` / `Gemini 4 Argon (High)` (heavy-refactor Coordinator & Claude-saving fallback); **Pool 3 (Premium):** `Claude Sonnet/Opus 5.5` (**NEVER** park `Claude Opus` as Coordinator; spawn 1-turn worker only).
- **Autonomous 3-Tier Escalation**: (1) Clear 1–2 file bugs/edits -> Coordinator solves directly (`0` workers, `0%` Claude); (2) Multi-file/logic/architecture -> spawn **max 1** `Claude Sonnet (Low)` worker (`starts fresh`); (3) Deadlocked/extreme -> escalate to `Claude Sonnet (Medium)` or `Claude Opus (High)` 1-turn worker.
- **Strict Worker Diet & Auto-Kill**: Send `< 60 lines` telegraphic English `brief`; cap worker output at `<= 35 lines` English (bullets + CLI check + diff/pseudocode only — never rewrite full files); **call `swarm(action="kill")` immediately** after 1 reply. Coordinator writes full code & summarizes in Indonesian.
- **Claude Low-Quota (`<= 15%`) / Limit Fallback**: Auto-switch/spawn `#1` `Gemini 4 Argon (High)` / `Orchestrator (Argon)` or `Hydrogen (High/XHigh)` (`0%` Claude burn), or `#2` `openrouter:tanya_openrouter(model="r1"|"claude")`.
- **Scout Hygiene**: Never `read_file` raw dumps (`> 5 KB`); pre-aggregate via 1-liner Python. Open a New Conversation (or `/compact`) only when switching to an unrelated feature/topic.

## 3. Ponytail 250-Line Threshold & Clean Architecture
- **< 250 lines**: No premature splitting, single-use classes, or wrapper bloat; prefer Python stdlib and plain functions.
- **250–300+ lines**: Split sub-logic via **Facade Pattern** (re-export legacy symbols for zero regression).
- **Language**: Code comments, docstrings, and user explanations in **Indonesian**; rules/skills in concise **English**.

## 4. Shared `vibe_tools` Hygiene & Multi-Device Sync
- `vibe_tools/` is public & cross-project: **NEVER** add local paths, tokens, private project names, or domain-specific modules.
- **Pre-Addition Gate**: Ask confirmation via `ask_question` before adding/moving any file into `vibe_tools/`.
- **Sync**: Push via `python vibe_tools/push_vibe_tools.py`; pull with `git -C vibe_tools pull --rebase --autostash origin main`.

## 5. Antigravity YAML Frontmatter Guardrails
- `globs` MUST be a scalar string (`globs: "*.py"`), **NEVER** a YAML sequence (`["*.py"]`).
- Start line 1 with `---` frontmatter (`trigger` + `description`); use `***` (not `---`) for horizontal rules in body text; keep `.agents/rules/` deduplicated with `vibe_tools/rules/`.
