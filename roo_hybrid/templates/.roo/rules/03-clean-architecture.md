# Python Clean Architecture & Modularity Standards

## 1. File Size & Modularity
- **300-Line Soft/Hard Limit**: No single Python module (`.py`) should exceed **300 lines**. Split growing logic into focused sub-modules or packages.
- **Separation of Concerns**:
  - `config`: Constants, paths, and environment settings without side effects.
  - `core`: Pure domain logic and calculations.
  - `bridge` / `adapters`: External integrations (FFmpeg, DaVinci Resolve, MCP, APIs, subprocesses).
  - `main` / `runner`: Slim entry-point orchestrators.

## 2. Code Quality & Zero-Syntax-Error Gate
- **Type Hinting**: Provide explicit Python type hints for public function arguments and return values.
- **Targeted Diffs**: Always apply localized edits (`apply_diff`) rather than rewriting entire files.
- **Silent Syntax Gate**: Immediately after editing any `.py` file, run `python -m py_compile <modified_files>` and fix any syntax or indentation errors in the same turn before completing the task.

