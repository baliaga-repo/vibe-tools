---
name: tdd
description: "Enforce strict Test-Driven Development (Red-Green-Refactor) using pytest and isolated mock fixtures. Write test first, implement minimally, and refactor cleanly."
---

# Skill: Test-Driven Development (TDD)

Build robust Python software following the disciplined Red-Green-Refactor cycle.

## The Tri-Phase Cycle

### 1. Red (Test First)
- Write a unit test asserting the intended contract.
- Run `pytest tests/test_<module>.py -q`.
- Verify the test **fails** for the expected reason (e.g. `AssertionError` or `NotImplementedError`).

### 2. Green (Make it Pass)
- Write the minimal code necessary to satisfy the test.
- Resist premature optimization or implementing speculative features.
- Run `pytest tests/test_<module>.py -q` and verify it passes.

### 3. Refactor (Clean Architecture)
- Clean up duplication, enforce type hinting, and add Indonesian docstrings.
- Ensure the module stays strictly under 300 lines.
- Run `pytest tests/test_<module>.py -q` to guarantee behavior remains intact.
