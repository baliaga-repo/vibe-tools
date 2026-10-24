---
trigger: always_on
description: Python clean architecture standards, file length constraints, and token efficiency guidelines.
globs: "*.py"
---

# Python Clean Architecture & Token Efficiency Standards

This guide establishes coding standards for Python files within the workspace to ensure code remains tidy, maintainable, modular, and token-efficient for AI pair programming.

## 1. File Size Constraints & Modularity
- **Maximum File Limit (Soft Limit 250 - 300 Lines)**: 
  A single Python module file should not exceed 300 lines. As code approaches this threshold, separate helper functions or domain sub-logic into dedicated sub-modules within a sub-package.
- **Avoid God Files**:
  Never accumulate all concerns (UI, video processing, APIs, text utilities, and DaVinci automation) inside a single gigantic script.
- **Separation of Static Data**:
  Do not hardcode massive dictionaries or configuration lists directly inside logic files. Move them to configuration files (`.json`) or separate configuration modules.

## 2. Single Responsibility Principle (Layering)
Structure code across distinct layers:
- **Configuration (`config`)**: Stores constants, file path resolutions, and environment parameters without execution side-effects.
- **Domain / Core Logic (`core`)**: Pure processing functions (e.g., SRT parsing, SFX timing calculations) without heavy external dependencies.
- **External Integration / Bridge (`bridge` / `adapters`)**: Modules interacting with third-party APIs, DaVinci Resolve Fusion, FFmpeg subprocesses, or Windows ctypes APIs.
- **Entry Point / Orchestrator (`main.py` / `runner.py`)**: Coordinates high-level execution pipelines only.

## 3. Documentation, Type Hinting, and Language
- **Comments & Docstrings**: All code comments, function/class docstrings, and technical log messages MUST be written in **Indonesian**.
- **Type Hinting**: Provide explicit type hints for public function parameters and return values to clarify inter-module interfaces.
- **Naming Conventions**:
  - Functions and variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`

## 4. Token Efficiency During Code Modifications
- **Targeted Edits**: Use localized line replacements (`replace_file_content` / inline edits) rather than rewriting entire files.
- **Focused Context**: When modifying a feature, open and reference only the specific files directly relevant to that task.
