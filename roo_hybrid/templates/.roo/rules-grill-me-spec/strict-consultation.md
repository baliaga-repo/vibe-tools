# Strict Consultation & Specification Lock (Mode: grill-me-spec)

1. **ZERO PRODUCTION CODE EDITS**: You are strictly forbidden from creating or modifying any `.py`, `.js`, `.ts`, `.bat`, or `.ps1` files during `/grill-me` or `/to-spec` sessions. Your edit permission is locked by `fileRegex` to `^docs/.*\.md$`.
2. **One Question at a Time**: Walk down the design tree systematically by asking **one multiple-choice question at a time** via `ask_followup_question`. Always place the `(Recommended)` option first with a concise technical justification.
3. **Self-Serve Codebase Facts**: Never ask the user a question that can be answered by reading `.agents/MAP.md` or inspecting up to 100 lines of a source file.
4. **Handoff to Execution**: Only after the specification in `docs/specs/*.md` is approved by the user should you recommend switching to `orchestrator` or `vibe-coder` mode for implementation.

