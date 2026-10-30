---
name: ponytail
description: "Prevent AI over-engineering using the 7-Rung Decision Ladder (YAGNI, codebase reuse, Python stdlib-first, minimal code) and deep module principles. Supports lite, full (default), and ultra intensity modes."
---

# Skill: Ponytail (Anti-Over-Engineering & Deep Modules)

Think like the laziest senior engineer in the room: the best code is the code you never wrote.

## 1. The 7-Rung Decision Ladder
Evaluate every requirement from top to bottom and stop at the first rung that solves the problem:
1. **YAGNI**: Does this code/feature actually need to exist? If not, skip it.
2. **Codebase Reuse**: Does an existing function/module in the repository already solve this? Reuse it.
3. **Standard Library First**: Can Python's native stdlib (`pathlib`, `itertools`, `functools`, `collections`, `sqlite3`, `urllib`, `json`, `re`) handle it?
4. **Native Platform / CLI**: Can native OS or existing CLI flags (`ffmpeg`, `yt-dlp`) handle it directly?
5. **Installed Dependencies**: Can an already-installed dependency solve it without adding new packages?
6. **Plain Function / One-Liner**: Can a simple function or comprehension replace a new class or wrapper?
7. **Minimum Viable Implementation**: Write the smallest, cleanest, most readable code that satisfies the requirement.

## 2. Intensity Modes
- `/ponytail lite`: Enforce Rungs 3–5 only (prevent unnecessary external libraries and prefer stdlib).
- `/ponytail full` *(Default)*: Enforce all 7 rungs + keep code in the existing file while file size is `< 250 lines`.
- `/ponytail ultra`: Aggressive simplification—collapse single-use wrappers, inline trivial helpers, and minimize line count.

## 3. Deep Modules & Clean Architecture Seam
- **Simple Interface, Deep Functionality**: Expose narrow public functions with explicit type hints while hiding internal complexity.
- **250-Line Threshold**: Never create new files, classes, or abstraction layers for small utilities while the target file is `< 250 lines`. Only trigger modular splitting (`/modular-refactor` with Facade re-exports) when a file approaches `250–300 lines`.

## 4. Safety Boundaries (Never Be Lazy Here)
Never skip or weaken:
- Input validation at trust boundaries and specific exception handling (no bare `except:`).
- Credential isolation, API token scrubbing, and cookie protection.
- Indonesian docstrings/comments and `python -m py_compile` verification.

