---
description: Cluster uncommitted changes into themed buckets with per-file summaries, using commitz_ui for deterministic file inventory.
allowed-tools: Bash(git *), Read, Grep, Glob
---

## Context

- Canonical file inventory: !`commitz_ui`
- Current git diff (for understanding changes): !`git diff HEAD`
- Recent commit style reference: !`git log --oneline -10`

The file list from `commitz_ui` is the source of truth for which files changed and their +/-stats. Do not invent files or stats not present in commitz_ui output.

## Your task

1. Run `commitz_ui` to get the canonical file inventory, counts, and CTA chrome.
2. Read `git diff HEAD` to understand what actually changed in each file.
3. Cluster the files into logical commit buckets.
4. Present the result as a single block combining commitz_ui chrome with your bucketed items.

### Output format

Emit a horizontal line, then use the heading, untracked line, unpushed line, and CTA from `commitz_ui` verbatim. Replace its numbered file list with your bucketed version.

Single-file bucket — the bucket line IS the file line:

    N. filename +A/-D: <=30-char summary

Multi-file bucket — a short title line, then indented file sub-items:

    N. short bucket title
      - filename +A/-D: <=30-char summary
      - filename +A/-D: <=30-char summary

### Example output

```
3 files to commit. Select buckets with e.g. 1,3-7 or omit for all.
1. commitz_ui output improvements
  - commitz_ui +40/-11: count heading, untracked line
  - commitz_ui_test.py +28/-5: update count assertions
2. commitz.md +16/-4: restore bucketing rules

6 commits already in next push.
C: commit. P: commit+push. Or ignore & keep prompting.
```

### Key rules

- The <=30-char label per file is a **display summary only**, not the commit message.
- Every file from `commitz_ui` appears in exactly one bucket.
- Never invent files absent from `commitz_ui`.
- Prefer fewer coherent buckets. One bucket is fine if all changes are related.
- Keep code + its tests/docs together in the same bucket.
- Use basenames only — no directory paths.

**STOP after presenting buckets. Do not commit until the user sends a C or P token.**

## `yours` mode

Invoked as `/commitz yours`.

1. **Identify agent-touched files**: review this conversation's history to determine which files you (the agent) created or modified via Edit, Write, or equivalent file-writing tools. These are "your files."
2. **Run `commitz_ui`** to get the canonical file inventory.
3. **Filter**: keep only commitz_ui entries matching your files. If a file you touched is absent from commitz_ui (already committed or untracked), note it but don't block.
4. **Bucket** the filtered files using the normal bucketing rules above.
5. **Show the buckets** briefly for visibility, then immediately — without waiting for a C/P token:
   - Commit each bucket (autonomous commit messages, repo style, one per bucket).
   - Push all commits.
   - For any `.md` files in the committed buckets: if the `md2confluence` skill is available and the file has a Confluence front-matter marker, invoke `md2confluence` to mirror it. Skip silently otherwise.
6. Show final `git log --oneline` for new commits and `git status`.

## Token handling

- `C` or `C.`: commit all buckets.
- `C1,3-5` or `C1,3-5.`: commit only selected bucket numbers.
- `P` or `P.`: commit all, then push. If nothing to commit, push only.
- `P1,3-5` or `P1,3-5.`: commit selected buckets, then push.

Period separates token from rest of prompt: `C1,3. and also fix the tests`

**Nothing to commit:** if `commitz_ui` shows no uncommitted files but there are unpushed commits, skip bucket presentation. Show only the unpushed count line and the P CTA.

## Commit behavior

- Bucket numbers from the most recent bucketed block are the reference.
- Stage only files in selected buckets.
- Write good commit messages autonomously (repo style). Do not draft or ask.
- One commit per bucket unless user says otherwise.
- After commits, show `git log --oneline` for new commits and `git status`.
- Push only on explicit `P` token.
