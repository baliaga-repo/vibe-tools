---
name: codebase-design
description: "Apply software design principles to combat code entropy: deep modules, clean seams, narrow interfaces, and god-object eradication."
---

# Skill: Codebase Design

Prevent architectural degradation and maintain lean, deep modules across the repository.

## Principles of Deep Modules
1. **Simple Interface, Deep Functionality**: Hide internal implementation complexity behind simple, declarative public functions.
2. **Find Natural Seams**: Split logic where dependencies naturally diverge (e.g. pure data transformation vs I/O side-effects).
3. **No God Objects**: Never allow a class or file to know everything, manage everything, or exceed 300 lines.
4. **Configuration Decoupling**: Static lists, regexes, and file paths belong in dedicated configuration modules or JSON definitions.
5. **Facade Preservation**: When splitting a legacy module, preserve backwards-compatibility by re-exporting relocated symbols.
