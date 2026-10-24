---
name: implement
description: "Execute engineering tickets sequentially using strict Test-Driven Development (TDD) and localized edits. Prevents scope creep, regression, and token exhaustion."
---

# Skill: Implement

Execute specification tickets iteratively with zero regressions and tight scope control.

## Execution Rules
1. **One Ticket at a Time**: Complete, verify, and lock down a ticket before starting the next.
2. **Minimal Edit Footprint**: Strictly use targeted `replace_file_content` instead of whole-file overwrites.
3. **Verify As You Go**: Run discrete unit tests for the current ticket:
   ```powershell
   pytest tests/test_<module>.py -k "<test_case>" -q
   ```
4. **Indonesian Documentation**: All docstrings, inline comments, and technical log messages must be in Indonesian.
5. **No Monoliths**: Verify that no modified file exceeds 300 lines. If approaching the limit, extract helpers immediately.
