# Documentation Style Guide

Reference principles from relationship-shared `doc-audit` (Walmart-internal) adapted for personal projects.

## Core Principles

### Timelessness
Documents should read as true today, next month, and next year. Avoid present-time editorializing or language that suggests temporary states.

### Confidence Calibration
Never embed confidence claims in the documentation itself. Let facts speak; avoid adverbs and qualifiers that override reader judgment.

## Specific Rules

### Headings
- ❌ **Never use parenthetical editorializing** in headings
  - Bad: `## Requirements (Confirmed)`
  - Bad: `## Snapshot (2026.05.02 final)`
  - Good: `## Requirements`
  - Good: `## Snapshot` (date may appear in body)

### Forbidden Terms
- ❌ **TL;DR** — implies reader can't find key info themselves
- ❌ **Executive Summary** — condescending layer over actual content
- Use instead: "Overview", "Quick Reference", "Summary"

### Discouraged Terms
- ⚠️ **"Current"** — brittle marker of time. What is "current" today is stale tomorrow.
  - Bad: `## Current Configuration`
  - Bad: `## Current State`
  - Good: `## Configuration`
  - Good: `## Repo Census`
  - Exception: "Current working directory" (technical term with unambiguous meaning)

- ⚠️ **"Confirmed"** — editorial claim; let facts establish truth
  - Bad: `## Requirements (Confirmed)`
  - Good: `## Requirements`

- ⚠️ **"Final"** — implies finality; systems evolve
  - Bad: `## Snapshot (2026.05.02 final)`
  - Good: `## Snapshot — 2026.05.02` or just `## Snapshot`

### Dates and Versions
- Use ISO 8601 (2026.07.01 format per EDTF personal variant) in body text
- Don't burden headings with dates unless the heading's meaning depends on the date (rare)
- Dates usually belong in context: "As of 2026.07.01:" or a metadata table

### Confidence Language
Replace these:
- "confirmed" → remove (show evidence instead)
- "should" → "must" (if mandatory) or describe the actual behavior
- "hopefully" → remove
- "essentially" → remove; be precise
- "basically" → remove

## Examples

### Before (violates rules)
```markdown
## TL;DR — Current Configuration (Confirmed)

Final snapshot (2026.05.02):
- ...

## Requirements (Confirmed)
- ...

## Session Update — Final Status
```

### After (follows rules)
```markdown
## Overview

Configuration as of 2026.05.02:
- ...

## Requirements

- ...

## Session Update
```

## Applying This Guide

1. **Personal laptop** (`~/bin/`): apply immediately
2. **Work laptop** (when on-site): integrate with relationship-shared `doc-audit` guidance; record any conflicts
3. **New documents**: use these rules from the start
4. **Existing documents**: refactor opportunistically (when editing for other reasons) rather than in one bulk pass
