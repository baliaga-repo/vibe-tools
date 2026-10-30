---
name: to-spec
description: "Transform high-level feature requests and ideas into formal, token-efficient technical specifications with clear contracts, data structures, error handling, and test criteria."
---

# Skill: To Spec

Convert loose user requirements or concept notes into a hardened technical specification.

## Specification Checklist
1. **Overview & Objectives**: 2-3 sentence executive summary of the target functionality.
2. **Interface Contracts**: Precise function signatures, type annotations, and schemas (avoiding `Any`).
3. **Data Flow & State Transitions**: Step-by-step lifecycle of input to output.
4. **Boundary & Error Matrix**: Explicit behavior for edge cases (missing files, network timeouts, invalid inputs).
5. **Architectural Guardrails**: Hard constraints (Ponytail Decision Ladder check: YAGNI, codebase reuse, stdlib-first; file line limits < 300, no god objects, token budgets).
6. **Acceptance Criteria**: Verifiable assertions and test cases.

Output the specification directly into the planning artifact or `docs/specs/<feature>.md`.
