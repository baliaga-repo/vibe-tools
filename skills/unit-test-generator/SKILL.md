---
name: unit-test-generator
description: Automated guidelines for designing, scaffolding, and executing isolated Python unit tests using pytest and unittest.mock. Focuses on zero-regression verification, mocking heavy dependencies (DaVinci Resolve SDK, FFmpeg, yt-dlp), and token-efficient test creation.
---

# Skill: Unit Test Generator

Scaffold and execute fast, isolated Python unit tests for automation pipelines.

## Principles
1. **Strict Mocking**: Never require live internet, GUI, or external binaries. Mock heavy SDKs, subprocesses, and network APIs via `unittest.mock` (`MagicMock`, `patch`) or `pytest` fixtures (`tmp_path`, `monkeypatch`).
2. **Granular & Concise**: Scope tests to discrete functions (keep suites < 150 lines).
3. **Repository Rules**: Place tests in `tests/test_<module>.py`. Use Indonesian docstrings and comments.

## Workflow & Recipes
1. **Analyze**: Identify pure functions vs side-effect boundaries (I/O, subprocess, SDK).
2. **Scaffold**: Create `tests/test_<name>.py` covering happy paths, edge cases, and error fallback.
3. **Mocking Pattern**:
   - **DaVinci Resolve SDK**: Patch resolver function, mock `ProjectManager -> CurrentProject -> CurrentTimeline`.
   - **Subprocess / CLI**: Patch `subprocess.run` to return `MagicMock(returncode=0, stdout=...)`.
4. **Execution**: Run `pytest tests/test_<name>.py -v` (or `python -m unittest`).
