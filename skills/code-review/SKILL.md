---
name: code-review
description: "Rigorous two-axis code review checking code smells, architectural compliance (clean architecture, <300 line limit, type hinting, Indonesian docstrings), and specification alignment."
---

# Skill: Code Review

Perform a strict two-axis code review on recent modifications and pull requests.

## Two-Axis Review Matrix

### Axis 1: Architectural Compliance & Code Smells
- **File Length**: Does any file exceed 300 lines? Flag for modularization if so.
- **Layering & SRP**: Is UI, business logic, or external SDK mixing across module boundaries?
- **Type Annotations**: Are public interfaces explicitly typed?
- **Documentation**: Are comments and docstrings written in Indonesian?
- **Error Handling**: Are exceptions caught specifically without bare `except:` blocks?

### Axis 2: Ticket & Spec Alignment
- **Scope Verification**: Did the changes alter functionality outside the ticket scope?
- **Regressions**: Are existing unit tests passing without modifications to test assertions?
- **Token Efficiency**: Were diffs localized and clean without large whitespace churn?

Output review findings grouped by: `[CRITICAL / BLOCKING]`, `[WARNING]`, and `[SUGGESTION]`.
