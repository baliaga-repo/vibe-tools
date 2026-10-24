---
name: grill-me
description: "Interview the user relentlessly about every aspect of a plan, feature, or design tree until all dependencies, edge cases, and failure modes are resolved. Use ask_question with compressed options and recommended defaults before writing code."
---

# Skill: Grill Me

Interview the user systematically to resolve design uncertainties, edge cases, and technical assumptions before writing or refactoring code.

## Core Rules
1. **One Question at a Time**: Never overwhelm the user with multiple open questions in free text.
2. **Use `ask_question`**: Formulate interactive multiple-choice options with a clear recommended option prefixed by `(Recommended)`.
3. **Explore First**: If a question can be answered by inspecting the codebase or files, explore the code first instead of asking.
4. **Token-Efficient Options**: Keep option descriptions dense and technical. Format options as the user's direct response.
5. **Resolve Dependencies**: Walk down each branch of the architectural decision tree step-by-step.
6. **No Phantom Code**: Do not touch code until the interview terminates with a clear, approved consensus.
