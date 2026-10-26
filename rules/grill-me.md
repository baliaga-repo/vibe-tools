# Rule: Super Grill-Me Workflow

Triggered when the user invokes `/grill-me` or requests an architectural interview before writing code.

## 1. Core Principles
- **Codebase Exploration First**: Inspect existing files, classes, and logic before asking questions that can be answered from code.
- **One Question at a Time**: Never overwhelm the user with multiple open questions in free text.
- **Structured Interactivity**: Use `ask_question` tool with compressed, technical options and always prefix the preferred choice with `(Recommended)`.
- **Token-Efficient Options**: Keep option descriptions dense and actionable. Format options as the user's direct response.
- **Strict Pre-Coding Gate**: Do not touch or modify production code until the interview terminates and explicit consensus is reached.

## 2. Interview Scope
Walk down each branch of the design tree, resolving dependencies one by one:
1. **Domain & Boundaries**: Identify entity definitions, data contracts, and scope edges.
2. **Architecture & Seams**: Determine module responsibilities, public interfaces, and coupling boundaries.
3. **Failure Modes & Edge Cases**: Clarify handling of timeouts, invalid inputs, backward compatibility, and error recovery.

## 3. Decision Handoff Gate
Upon reaching consensus at the end of the interview, the agent MUST trigger a final `ask_question` presenting exactly these choices:
1. `(Recommended) Simpan keputusan arsitektur ke docs/ (ADR & Glossary) dan langsung lanjut koding`
2. `Simpan keputusan arsitektur ke docs/ sebagai arsip perencanaan saja (tanpa koding)`
3. `Langsung eksekusi koding tanpa membuat file dokumentasi di docs/`

## 4. Documentation Specifications (When Saving to docs/)
If Option 1 or 2 is selected:
- **Architectural Decision Record (ADR)**:
  - Save to: `docs/adr/ADR-XXX_<short_title>.md` (increment sequence number based on existing ADRs or start with `ADR-001`).
  - Required sections: Context & Problem Statement, Considered Alternatives & Trade-offs, Decision Outcome, and Consequences.
- **Domain Glossary**:
  - Update or create: `docs/GLOSSARY.md`.
  - Add newly agreed domain terms, schemas, and ubiquitous language definitions.
