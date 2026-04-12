---
description: Build deterministic pending-commit UI from commitz_ui, then cluster changes into commit buckets and commit selected buckets.
allowed-tools: Bash(git *), Read, Grep, Glob
---

## Context

- Deterministic commit UI source: !`commitz_ui`
- Current git status (debug): !`git status`
- Current git diff (staged and unstaged): !`git diff HEAD`
- Recent commit messages (style reference): !`git log --oneline -10`

Do not treat conversation context as source-of-truth for changed files. The inventory from `commitz_ui` is authoritative.

## Your task

First, show the `commitz_ui` output exactly as the top section of your response (heading, numbered lines, unpushed line if present, CTA). Do not rewrite file inventory freehand.

Then, if there are uncommitted changes, cluster files into logically coherent commit buckets.

For each bucket, show:

- **Bucket number**
- **Short title** describing the theme
- **Files** included (must be a subset of `commitz_ui` inventory)
- **Draft commit message** — multi-line, following repo style. The first line is terse. Add detail only when nontrivial. End with: `🌀 Magic applied with Wibey VSCode Extension 🪄`

Clustering rules:

- Prefer fewer coherent buckets over many tiny ones
- Every file from `commitz_ui` appears in exactly one bucket
- Never introduce files absent from `commitz_ui`
- If a change spans doc + code for one feature, keep together
- If all changes are tightly related, one bucket is acceptable
- Extract Jira ticket from branch name when present; otherwise use conventional prefixes (`docs:`, `fix:`, `refactor:`, `chore:`, `feat:`, `test:`)

If `commitz_ui` reports **unpushed-only mode** (no pending commits, only `P:`), do not produce buckets; just report that push-only action is available and wait for user confirmation.

**STOP HERE after presenting UI + buckets.** Do not commit until user explicitly selects buckets/tokens.

User responses may include:

- Bucket numbers (e.g., `1,3,5`)
- `all`
- `C`, `C1,3-5`, `P`, or `P2-4`
- Edits to bucket grouping/messages
- `skip N`

When committing:

- Stage only files in the selected bucket(s)
- Commit selected buckets in sequence
- Keep commit messages based on approved drafts
- Show `git log --oneline` for new commits and `git status` afterward

Do not push unless user explicitly asks for `P` or otherwise requests push.
