# AgentRules.md - Global AI Agent Rules

These rules apply to all projects and all AI models. Any project-specific or model-specific AI rules override them only where they explicitly conflict.

The canonical source of this file is `~/bin/AgentRules.md`, version-controlled in the `~/bin/` repo (`github.com/BrianHoltz/scripts`). The following paths are symlinks to it:

- `~/.claude/CLAUDE.md` — read by Claude Code CLI and Wibey (VSCode extension)
- `~/.cursor/cursorrules` — read by Cursor

Other `~/bin/` files symlinked into `~/`:

- `~/.shellrc.common` → `~/bin/shellrc.common` — shared PATH/env for zsh + bash
- `~/.zprofile` → `~/bin/zprofile` — zsh login shell config
- `~/.zshrc` → `~/bin/zshrc` — zsh interactive shell config
- `~/.bash_profile` → `~/bin/bash_profile` — bash login/interactive shell config

To update these files, edit the `~/bin/` copies and commit in the `~/bin/` repo.

## Coding Workflow

See `shared/docs/WibeyAgentRef.md` § Coding Workflow (TDD) for the full TDD steps. In repos without a `shared/` symlink: pull main, create feature branch, write failing tests, implement, run tests, run full suite, run postman/newman if available, run coverage (100% of new flows/conditions).

## Communication Style

- Don't be sycophantic. Be the opposite of sycophantic. You are a valuable team member and we need your best unfiltered judgements.
- Be skeptical of existing code/docs and recent statements from both user and AI agents.
- Feel free to volunteer alternative ideas, and critique user suggestions.
- If you're not sure about user intent, ask clarifying questions before proceeding.
- Avoid tables and code blocks/text boxes in conversation output — the conversation window is kept narrow, and wide elements cause horizontal scrolling. Use bullet lists or plain prose instead. Tables and code blocks are fine in files, just not in chat replies.

## Documentation

See `shared/docs/WibeyProjectMgt.md` § Documentation Principles for the full rules (evidence patterns, styling discipline, task lists, ad hoc doc naming, DRY/history). In repos without a `shared/` symlink, the key rules are:

- Keep docs in sync with code. No redundant comments. No file line numbers in enduring docs. No numbered lists in version-controlled docs. Update TOC when updating a doc.
- Every verifiable empirical claim must cite its source. Collect in a `## Evidence` section with HTML anchors. Unsourced claims are assertions — label "Inference:" or "Unverified:".
- No revision history in docs (git provides it). No "End of document". No links from tracked files to aidocs/tmp/. docs/ never mentions dates except formal production events.
- Ad hoc docs: don't check into VCS. Place in aidocs/ in subfolder yyyy-mm-dd/. Name hhmm_CamelCase.md. Don't create for content <100 lines. Combine multiple docs into one with TOC.
- No all-caps for emphasis. No extraneous horizontal rules. Bold/italics sparingly. Informational glyphs: † ‡ ⁑ 📌. Problem glyphs: ⚠️ ❗ 📣 🔔. One glyph per cell, unambiguous within table/list.
- Table cell vocabulary — emdash (N/A), TBD (exists, needs lookup), TODO (work needed, blocks nothing), ? (uncertain), ⚠️ (alarming, footnote required), blank only for visual grouping.
- Future work appears only as task lists or TODOs. No "Critical/Important/urgent" labels — use order. Label sections "Tasks" not "Next Steps/To Do/Action Items/Plan". No future dates unless capturing a commitment.

## File Operations

- Always re-read a file immediately before editing it, even if you read it recently. The user or another agent may have modified it in parallel. This enables maximal concurrent work among agents and humans.
- Never use `rm` directly. Always use `trash` command or `mv` to `~/.Trash/`
- When duplicate/conflicting files exist, always ASK which version to keep before deleting either
- Do not make any VCS changes unless you're absolutely sure the user wants that.

### PR Diff Source of Truth

When reviewing a PR or describing what a branch/PR changes relative to its base:

- Use `gh pr diff <number>` (or `gh pr view <number> --json files`) as the **sole authoritative source** of what a PR changes. This is the merge diff — exactly what GitHub shows on the "Files changed" tab.
- **Never** use `git diff main..branch` or `git log main..branch` to determine a PR's changes. Branches accumulate merge commits, intermediate history, and ancestry artifacts that do not reflect the actual PR diff. Using them will cause you to hallucinate changes that aren't part of the PR.
- Commits are useful for understanding *how* the author arrived at the changes (intent, iteration history). But the diff — not the commits — defines *what* the PR changes.
- If `gh pr diff` and `git diff main..branch` disagree, `gh pr diff` is correct. Period.

## Terminals

<!-- Pager hangs, heredoc hangs, and terminal blindness guidance moved to git history — not seen recently. -->

## Dates and Times

**Always verify the current date before using it.** AI agents frequently hallucinate dates, confuse MM/DD with DD/MM, or use stale dates from context. Before creating date-stamped files or folders:

```bash
date "+%Y-%m-%d %H:%M %Z"
```

This is cheap (a few tokens for the command and output) and prevents embarrassing date hallucinations. Run this once per session or whenever you need to use the current date.

## Custom Commands

### convo

Park the current conversation for identification in Mac workspace/Mission Control switching.

Trigger: user says "convo [optional title]" or "Convo [optional title]"

Steps:
- If trigger is capitalized ("Convo"), emit 30 `&nbsp;` lines as raw markdown (not via bash — bash newlines don't render in chat)
- Run a single Bash command to get both the date and the repo emoji:
  ```bash
  date "+%Y-%m-%d %H:%M %Z"; ~/bin/repo-emoji <workspace-dir>
  ```
- If the user provided a title after "convo", use it verbatim. Otherwise, choose a terse title from the conversation context.
- Emit the date and title as two H1 bold lines, with HR rules above and below, and the emoji prepended to the title:

---
# **YYYY-MM-DD HH:MM TZ**
# **{emoji} Title**

---
