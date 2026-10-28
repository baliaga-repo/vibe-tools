# Interactive Execution Method Selector (Orchestrator Rules)

Whenever the user submits a coding, bug-fixing, or codebase exploration prompt in `orchestrator` mode:

## 1. Check for Explicit Shortcut Prefix
If the user's prompt starts with or contains an explicit method shortcut:
- `/pakai-rag`: Immediately execute **Method 1 (Local RAG `nomic-embed-text` + Cloud `vibe-coder`)** without asking.
- `/pakai-3b`: Immediately execute **Method 2 (`local-scout-3b` explore -> `vibe-coder` edit -> `local-scout-3b` verify)** without asking.
- `/pakai-7b`: Immediately execute **Method 3 (`local-scout-7b` explore -> `vibe-coder` edit -> `local-scout-7b` verify)** without asking.
- `/adu-metode`: Run the isolated exploration benchmark across all 3 methods and present a comparison table of speed, accuracy, and token usage.

## 2. Pre-Flight Interactive Modal (When No Shortcut Is Provided)
If the user did NOT specify which execution method to use, call `ask_followup_question` BEFORE delegating subtasks:

- **Question**: `"Pilih Metode Eksekusi Kerja Kasar untuk tugas ini:"`
- **Options**:
  1. `(Recommended) 🚀 Kombo Local RAG (nomic-embed) + Gemini Flash / DeepSeek-V3 (~4-6 dtk | Vektor Lokal 0,2 dtk + Cloud Instan)`
  2. `🏎️ Local Scout 3B (qwen2.5-coder:3b) + Cloud Edit (~13-16 dtk | Kerja Kasar Explore & Test Rp 0 — Ringan 2,2 GB VRAM)`
  3. `🚜 Local Scout 7B (qwen2.5-coder:7b) + Cloud Edit (~24-28 dtk | Kerja Kasar Explore & Test Rp 0 — Akurasi Tinggi 4,8 GB VRAM)`
  4. `🏆 Mode Benchmark / Adu Cepat (Uji & bandingkan waktu nyata ke-3 metode untuk tugas ini)`

## 3. Boomerang Fallback Handling
If `local-scout-3b` or `local-scout-7b` returns `[FALLBACK_TO_CLOUD]`, immediately switch to **Method 1 (Local RAG + `vibe-coder`)** without failing the user's request.

