---
description: Show the deterministic pending-commit UI from commitz_ui and execute C/P token actions.
allowed-tools: Bash(git *), Read, Grep, Glob
---

## Context

- Canonical UI source: !`commitz_ui`
- Current git status (debug): !`git status`
- Current git diff (debug): !`git diff HEAD`
- Recent commit style reference: !`git log --oneline -10`

The command output from `commitz_ui` is the source of truth for pending files and push state.

## Your task

1. Run `commitz_ui`.
2. Paste its stdout verbatim as the full response block for the initial command call.
3. Do not add buckets, draft commit messages, or extra narrative on that first response.

## Follow-up token handling

On a follow-up user response, interpret these tokens:

- `C` or `C.`: commit all pending uncommitted items.
- `C1,3-5` or `C1,3-5.`: commit only selected item numbers.
- `P` or `P.`: commit all pending items, then push. If no uncommitted items exist, push only.
- `P1,3-5` or `P1,3-5.`: commit selected item numbers, then push.

When a token is a prompt prefix (for example `C1,3-5. and also rename foo`), execute token action first, then continue with the rest of the prompt.

## Commit behavior

- Use item numbers from the latest `commitz_ui` block.
- Stage only files mapped to selected numbers.
- Create good commit messages autonomously using repo style. Do not ask the user to pick from drafted messages.
- Keep one logical commit per selected numbered item unless the user asks otherwise.
- After execution, show `git log --oneline` for new commits and `git status`.
- Push only when token is `P...` or the user explicitly asks to push.

## Formatting rules

- Keep CTA lines flush-left.
- Do not indent `C:` or `P:` lines.
- Do not rewrite or reflow the canonical `commitz_ui` block.
