---
name: to-tickets
description: "Decompose a technical specification into discrete, dependency-ordered, and self-contained engineering tickets. Ensures small, testable, and parallelizable increments."
---

# Skill: To Tickets

Decompose a complex specification into actionable, bite-sized engineering tickets.

## Ticket Structure
Each ticket must adhere to the following schema:
- **Ticket ID & Title**: e.g. `[TICKET-01] Scaffold Config and Data Models`
- **Dependency**: Explicit prerequisites (`Blocked by: [TICKET-00]` or `None`).
- **Files Modified / Created**: Concrete file paths to touch.
- **Scope of Changes**: Bullet points of precise logic to implement.
- **Verification Criterion**: Specific unit test or CLI command to validate completion.
- **Token Budget**: Estimated scope (< 100 lines changed per ticket).

## Execution Ordering
Order tickets sequentially from core foundations (models/configs) -> domain logic -> external bridges -> orchestrators/UI.
