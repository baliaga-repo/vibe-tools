# Python Clean Architecture & Modularity Standards

## 1. File Size, Ponytail Threshold & Modularity
- **Under 250 Lines (Ponytail Anti-Over-Engineering Zone)**: Never prematurely split files, create single-use classes, or introduce wrapper layers for small features while the target file is under 250 lines. Prefer Python's standard library and plain functions inside the existing module.
- **Approaching 250 - 300 Lines (Modular Refactor Zone)**: No single Python module (`.py`) should exceed **300 lines**. Split growing logic (250–300 lines) into focused sub-modules using the **Facade Pattern** (re-exporting relocated symbols in the legacy file for backwards compatibility).
- **Separation of Concerns**:
  - `config`: Constants, paths, and environment settings without side effects.
  - `core`: Pure domain logic and calculations.
  - `bridge` / `adapters`: External integrations (FFmpeg, DaVinci Resolve, MCP, APIs, subprocesses).
  - `main` / `runner`: Slim entry-point orchestrators.

## 2. Code Quality & Zero-Syntax-Error Gate
- **Type Hinting**: Provide explicit Python type hints for public function arguments and return values.
- **Targeted Diffs**: Always apply localized edits (`apply_diff`) rather than rewriting entire files.
- **Silent Syntax Gate**: Immediately after editing any `.py` file, run `python -m py_compile <modified_files>` and fix any syntax or indentation errors in the same turn before completing the task.
