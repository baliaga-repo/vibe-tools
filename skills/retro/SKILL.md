---
name: retro
description: "Post-implementation engineering retrospective. Evaluates agent performance, detects friction points, and refines repository rules and guardrails in AGENTS.md."
---

# Skill: Retrospective (Retro)

Evaluate an completed feature or refactoring milestone to continuously harden agent guardrails.

## Retrospective Questions
1. **Friction Points**: Where did the agent get stuck, loop, or write unnecessary boilerplate?
2. **Token Efficiency**: Was context wasted on large file dumps or uncompressed CLI logs?
3. **Spec Alignment**: Did any unnoticed regressions occur during the work?
4. **Action Items**: Concrete updates to apply to `.agents/AGENTS.md` or `vibe_tools/rules/` to prevent similar issues in future runs.
