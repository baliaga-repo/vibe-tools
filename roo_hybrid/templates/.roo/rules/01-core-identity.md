# Core Identity & Communication Rules (Hybrid Dual-Cockpit)

- **Single Source of Truth**: Always treat `.agents/AGENTS.md` and `.agents/MAP.md` as the primary workspace foundation shared between Antigravity IDE and VS Code Roo Code.
- **Indonesian Communication**: ALWAYS communicate with the user in **Indonesian** during chatting, vibe coding, and architectural interviews.
- **Indonesian Code Documentation**: All Python comments, module/class/function docstrings, and user-facing log messages MUST be written in **Indonesian**.
- **Model Transparency**: Explicitly state the active model and execution method at the beginning of your response before editing files.
- **Direct Unicode Symbols**: Never use LaTeX math notation in responses or comments; use direct Unicode symbols (`->`, `•`, `~`).
- **Execution Telemetry Badge**: At the end of every coding or exploration task, include a concise telemetry block:
  ```markdown
  ---
  ⏱️ **Telemetry Eksekusi**:
  • **Metode Aktif**: [🚀 Kombo Local RAG + Cloud | 🏎️ Local Scout 3B + Cloud | 🚜 Local Scout 7B + Cloud]
  • **Kerja Kasar Lokal ($0)**: [Jumlah & jenis aksi lokal di RTX 3060]
  • **Eksekusi Cloud**: [Jumlah & jenis aksi model Cloud]
  • **Status VRAM RTX 3060**: [Estimasi VRAM & Auto-Unload 5m]
  ```

