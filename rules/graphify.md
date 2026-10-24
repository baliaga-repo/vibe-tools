---
trigger: always_on
description: Consult the graphify knowledge graph at graphify-out/ for codebase and architecture questions.
---

## graphify

- Query graph first when `graphify-out/graph.json` exists: `graphify query "<question>"`, `graphify path "<A>" "<B>"`, or `graphify explain "<concept>"`.
- Navigate `graphify-out/wiki/index.md` instead of reading raw files if present.
- Read `graphify-out/GRAPH_REPORT.md` only for high-level review when scoped queries are insufficient.
- After code modifications, run `graphify update .` to keep graph current (AST-only).
- Prune old archive directories in `graphify-out/`, keeping at most 2 most recent dates (`YYYY-MM-DD`).
