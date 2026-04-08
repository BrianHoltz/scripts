---
description: Cluster uncommitted git diffs into themed buckets, draft a commit message for each, and commit the ones the user approves.
allowed-tools: Bash(git *), Read, Grep, Glob
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged): !`git diff HEAD`
- Recent commit messages (for style): !`git log --oneline -10`

Do not assume the conversation context is the authority for what has changed — the git output above is the source of truth.

## Your task

Cluster all uncommitted changes (staged, unstaged, and untracked) into logically coherent numbered buckets. Each bucket should group files that belong to the same theme (e.g., a feature, a doc section, a refactor, a fix).

For each bucket, show:

- **Bucket number**
- **Short title** describing the theme
- **Files** included
- **Draft commit message** — multi-line, following the repo's existing commit style. The first line is a terse summary. Subsequent lines add detail only if the change is nontrivial. Don't document trivial changes a future developer or agent would not search for. End with: `🌀 Magic applied with Wibey VSCode Extension 🪄`

Guidelines for clustering:

- Prefer fewer, coherent buckets over many tiny ones
- A single file should appear in exactly one bucket
- If a change spans doc + code for the same feature, keep them together
- Untracked files that logically belong with modified files go in the same bucket
- If all changes are tightly related, a single bucket is fine — say so
- Extract Jira ticket ID from branch name if present (e.g., CATGTRLSHP-123) and prefix the commit summary. If no ticket, use conventional prefixes (docs:, fix:, refactor:, chore:, feat:, test:)

**STOP HERE. Present the buckets and wait for the user to respond. Do NOT commit anything until the user explicitly picks buckets.** The user may:

- Pick buckets by number (e.g., "1, 3, 5") to commit in sequence
- Say "all" to commit all in sequence
- Request edits to messages or bucket groupings before committing
- Say "skip N" to skip a bucket

When committing, stage only the files for that bucket and commit. After all requested commits, show `git log --oneline` for the new commits and `git status` to confirm the working tree state.

Do NOT push unless the user explicitly asks.
