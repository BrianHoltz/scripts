---
name: continue
description: Checkpoint state into the active doc, then continue working. Commit, update work log, overwrite active work, append open questions, optionally compact.
---

> [!NOTE]
> **Mirror-safe command.** This file contains no Walmart-proprietary content and is
> designed to be manually mirrored to personal laptops. The canonical copy lives in
> [`relationship-shared/.wibey/commands/`](https://gecgithub01.walmart.com/CatalogRelationships/relationship-shared).
> **If you are reading this outside of Walmart GHE, do not edit it here** — make
> changes in relationship-shared and re-sync.

# Continue — Checkpoint and Resume

Distill current state into the active doc, commit it, then keep working. Default behavior: **write → commit → continue**. Pass `--compact` to run `/compact` after committing. Pass `--no-commit` to update the doc without committing (e.g. mid-task snapshot).

## When to self-invoke

Invoke `/continue` proactively — do not wait for the user to interrupt:

- Before calling `advisor`
- Before `/compact` — always write and commit the doc first, then compact
- Before any risky or irreversible operation (deploys, destructive commands, external writes)
- After each major milestone or phase transition
- Whenever context is getting large and you sense a compact may be needed soon

## Steps (execute in order — do not skip any step)

**1. Identify the active doc.**

Search in this priority order:
- `shared/aidocs/` — any open or recently-modified task record
- Currently open editor file that is an incident doc or project doc (`.md`)
- `/triage` incident doc for the current session
- If none found, or multiple ambiguous candidates: ask the user to identify the doc, then proceed

**2. Write the doc.** Update the following sections:

- **`## Work Log`** — *append* a new timestamped entry (ISO datetime, local timezone). 1–3 sentences: what was done, what was found, what changed. Do not edit previous entries.
- **`## Active Work`** — *overwrite entirely*. Current state plus what comes next: one sentence on what was just being done, then an ordered list of immediate next subtasks specific enough that a fresh agent with no prior context can resume without asking the user. If stopping, note "Handoff" and list pickup steps. Organize under `###` headings per in-progress task as the template requires.
- **`## Open Questions`** — *append* any new unresolved questions or blockers discovered since the last checkpoint. Do not remove existing items unless they are resolved (mark resolved items with ~~strikethrough~~ and a resolution note).

**Quality gate:** After writing, ask: "Could a fresh agent reading only this doc resume without asking the user anything?" If no, add what's missing before committing.

**3. Commit (unless `--no-commit` was passed).**

Follow AGENTS.md commit rules:
- `git add` and `git commit` from within `shared/` (relationship-shared commits directly to `main`, no branch/PR)
- Extract Jira ticket from branch name if applicable; otherwise use `docs:` prefix
- Commit message: `docs: /continue checkpoint — <one-line summary of Active Work>`
- Attribution footer: `🌀 Magic applied with Wibey JetBrains Plugin 🪄`

**4. Compact (only if `--compact` was passed, or context is >80% full and you judge it necessary).**

Run `/compact` now. The doc is committed — state is safe. After compacting, re-read `## Active Work` from the doc to restore orientation before continuing.

**5. Continue working.**

Resume from `## Active Work`, top subtask first. Do not ask for confirmation — just proceed.
