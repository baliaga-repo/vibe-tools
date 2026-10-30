---
name: implement
description: "Execute engineering tickets sequentially using strict Test-Driven Development (TDD), localized edits, and Ponytail anti-over-engineering defaults. Prevents scope creep, regression, and token exhaustion."
---

# Skill: Implement

Execute specification tickets iteratively with zero regressions and tight scope control.

## Execution Rules
1. **One Ticket at a Time**: Complete, verify, and lock down a ticket before starting the next.
2. **Minimal Edit Footprint**: Strictly use targeted `replace_file_content` instead of whole-file overwrites.
3. **Ponytail Full Default**: Strictly apply `/ponytail full`—prefer Python standard library, plain functions, and existing code. Keep code in the existing file while file size is `< 250 lines`.
4. **Verify As You Go**: Run discrete unit tests for the current ticket:
   ```powershell
   pytest tests/test_<module>.py -k "<test_case>" -q
   ```
5. **Indonesian Documentation**: All docstrings, inline comments, and technical log messages must be in Indonesian.
6. **No Monoliths**: Verify that no modified file exceeds 300 lines. If approaching the limit (250–300 lines), extract helpers via `/modular-refactor` using the Facade Pattern.
