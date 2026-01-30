# aidocs - Ephemeral Agent Artifacts

This directory contains documentation generated during AI-assisted development sessions for tools in this repository.

## Documentation Organization Principles

### aidocs/ vs. docs/

**aidocs/ (this directory)** - Ephemeral session narratives and implementation details
- "How we got here" stories
- Session-specific status updates
- Detailed implementation pseudocode
- Step-by-step guides for specific tasks
- Historical context and decision rationale
- Agent-to-agent handoff documentation

**docs/** - Authoritative current-state reference documentation
- Current strategy and architecture
- Current status (test counts, feature status)
- Next steps and priorities
- Minimal historical narrative
- Living documents that get updated as system evolves

### DRY Principle

**AVOID:**
- ❌ Duplicating strategy documentation between aidocs/ and docs/
- ❌ Copying implementation details into docs/ that belong in aidocs/
- ❌ Historical narratives in docs/ about "what we did"
- ❌ Detailed pseudocode in docs/ when it's session-specific

**DO:**
- ✅ Keep current status in docs/, detailed how-to in aidocs/
- ✅ Reference aidocs/ from docs/ for implementation details
- ✅ Update docs/ when strategy changes, add aidocs/ entry for history
- ✅ Use aidocs/ for agent handoffs with step-by-step plans
- ✅ Use docs/ for long-term reference and current state

### Example: Testing Documentation

**docs/Testing.md** (authoritative reference):
- Current test status: 67 tests, 64 passing
- Testing strategy and principles
- Next priorities (with links to aidocs/ for details)
- Minimal "how we got here"

**aidocs/2025-11-30/1220_TestingStatus.md** (session narrative):
- Detailed test breakdown by category
- Step-by-step implementation plan for --preset flag
- Historical context: which tests were fixed when
- Agent-specific guidance (terminal workarounds, etc.)
- Full pseudocode for history mining script

## Organization

Documents are organized by date in `yyyy-mm-dd/` folders:

```
aidocs/
├── README.md              # This file
├── 2025-11-16/           # Nov 16, 2025 sessions (Locale feature)
├── 2025-11-25/           # Nov 25, 2025 sessions (Git workflow)
├── 2025-11-27/           # Nov 27, 2025 sessions (Branch switching)
├── 2025-11-28/           # Nov 28, 2025 sessions (Help text)
├── 2025-11-29/           # Nov 29, 2025 sessions (Testing & migration)
└── 2025-11-30/           # Nov 30, 2025 sessions (Testing status updates)
```

## Naming Convention

- **hhmm_DescriptiveTitle.md** - Session summaries and feature docs (timestamped)
- **DescriptiveTitle.md** - Reference documents and guides (no timestamp)

## Purpose

These documents serve as:
- Development history and rationale
- Architecture and design decisions
- Implementation guides
- Migration and setup procedures
- Testing strategies

## Notes

- Documents are preserved as-is from development sessions
- Contains both high-level summaries and detailed technical docs
- Useful for understanding tool evolution and design choices
- Not end-user documentation (see tool-specific README files)

