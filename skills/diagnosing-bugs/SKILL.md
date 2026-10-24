---
name: diagnosing-bugs
description: "Disciplined, scientific bug diagnosis workflow. Requires reproducing the issue with a failing test case before touching production code, preventing phantom fixes and regressions."
---

# Skill: Diagnosing Bugs

Diagnose and resolve software bugs through scientific reproduction and targeted fixes.

## Strict Diagnostic Loop
1. **Gather Evidence**: Collect exact tracebacks, environment parameters, and inputs. Never guess.
2. **Isolate Component**: Use call graphs (`graphify path` or grep) to trace data flow to the origin of failure.
3. **Write Failing Test (Red)**: Create an isolated test reproducing the bug:
   ```powershell
   pytest tests/test_bug_reproduce.py -q
   ```
   *The test must fail with the reported symptom before any code changes are made.*
4. **Targeted Fix (Green)**: Apply the minimal fix required to make the test pass.
5. **Regression Sweep**: Run the entire test suite to guarantee zero side-effects.
6. **Post-Mortem**: Document root cause and preventative measures in 3 concise bullet points.
