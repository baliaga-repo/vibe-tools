---
name: modular-refactor
description: Step-by-step procedure and strategies for incremental Python refactoring to break monolithic scripts into clean, modular, token-efficient, and backwards-compatible (zero-regression) architectures. Activate when handling long files (>300 lines) or upon refactoring requests.
---

# Skill: Modular Refactor

Decompose monolithic Python scripts into clean, modular, and token-efficient architectures.

## Core Principles
1. **Zero Regression**: Preserve original entry points (batch scripts, CLI, Resolve shortcuts).
2. **Facade Pattern**: Re-export relocated functions/classes in the legacy file (`from module import symbol`) for backwards compatibility.
3. **Incremental**: Migrate one boundary/domain at a time.

## Workflow
1. **Dependency Mapping**: Check call graphs using `graphify query "function dependencies in <file>"`. Identify constants, pure utilities, side-effects, and entry points.
2. **Package Scaffolding**: Create package folder with `__init__.py` and dedicated submodules (`config.py`, `bridge.py`, `processor.py`, `handlers.py`).
3. **Extract & Facade**: Move logic to submodules, add Indonesian docstrings/type hints, and re-export symbols in legacy file.
4. **Graphify Refresh**: Run `graphify extract . --code-only` and notify user.
