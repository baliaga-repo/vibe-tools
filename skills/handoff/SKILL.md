---
name: handoff
description: "Compact the current conversation state, decisions made, and pending tasks into a dense, token-efficient handoff document for transitioning between chat sessions or AI models."
---

# Skill: Handoff

Compress ongoing work into an unambiguous handoff document for seamless context switching.

## Handoff Template
Generate a concise markdown artifact with the following sections:
1. **Current Objective**: 1-2 sentences summarizing what was being accomplished.
2. **Completed Milestones**: Bullet points of finished file edits and tests passed.
3. **Active Work & Immediate Next Step**: The exact line, function, or command currently being worked on.
4. **Key Decisions & Constraints**: Architectural choices made during this session.
5. **Known Blockers / Edge Cases**: In-flight issues or assumptions that require caution.
6. **Commands to Resume**: Exact terminal command to continue testing or running the task.
