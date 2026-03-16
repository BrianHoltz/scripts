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

## ❗ Do Not Overwrite Other Writers

**Re-read every file immediately before every edit.** Other agents and humans are editing files concurrently. If you write based on stale content, you silently destroy their work. This has happened repeatedly and is the single most damaging mistake an agent can make. No edit is so urgent that it justifies skipping the re-read. If the content changed since you last saw it, stop and ask — do not overwrite.

## Coding Workflow

See `shared/docs/WibeyAgentRef.md` § Coding Workflow (TDD) for the full TDD steps. In repos without a `shared/` symlink: pull main, create feature branch, write failing tests, implement, run tests, run full suite, run postman/newman if available, run coverage (100% of new flows/conditions).

## Communication Style

- Don't be sycophantic. Be the opposite of sycophantic. You are a valuable team member and we need your best unfiltered judgements.
- Be skeptical of existing code/docs and recent statements from both user and AI agents.
- Feel free to volunteer alternative ideas, and critique user suggestions.
- If you're not sure about user intent, ask clarifying questions before proceeding.
- Avoid tables and code blocks/text boxes in conversation output — the conversation window is kept narrow, and wide elements cause horizontal scrolling. Use bullet lists or plain prose instead. Tables and code blocks are fine in files, just not in chat replies.

## Inferring User Intent from Open Editors

When the user references a file ambiguously (e.g., "this file", "that doc", "the config", or just describes content without naming a file), use the IDE's open editor tabs to resolve the reference before asking clarifying questions.

- In Wibey/VSCode, use `getDiagnostics` with scope `open-editors` to list all open tabs. The **active tab** (marked Active) is the strongest signal — it's what the user is looking at right now.
- Use filenames to decide relevance. If the user says "the test file" and one open tab is `foo.test.ts`, that's almost certainly it. Read the file only if the name alone is ambiguous.
- If the active tab's filename doesn't match the user's reference, check the remaining open tabs before falling back to workspace-wide search or asking the user.
- A **dirty** (unsaved) tab indicates recent editing — weight it higher than clean tabs when multiple tabs could match.
- Prioritization order: active tab → dirty tabs → remaining open tabs → workspace search → ask user.

In CLI agents or other environments without editor tab access, use whatever information is immediately and efficiently available — recent git activity (`git diff`, `git log -1`), shell history, or the current working directory — to infer which file the user most recently accessed.

This is cheaper and faster than asking "which file do you mean?" and almost always resolves the reference correctly.

## Documentation

See `shared/docs/WibeyProjectMgt.md` § Documentation Principles for the full rules (evidence patterns, styling discipline, task lists, ad hoc doc naming, DRY/history). In repos without a `shared/` symlink, the key rules are:

- Keep docs in sync with code. No redundant comments. No file line numbers in enduring docs. No numbered lists in version-controlled docs. Update TOC when updating a doc.
- Every verifiable empirical claim must cite its source. Collect in a `## Evidence` section with HTML anchors. Unsourced claims are assertions — label "Inference:" or "Unverified:".
- No revision history in docs (git provides it). No "End of document". No links from tracked files to aidocs/tmp/. docs/ never mentions dates except formal production events.
- Ad hoc docs: don't check into VCS. Place in aidocs/ in subfolder yyyy-mm-dd/. Name hhmm_CamelCase.md. Don't create for content <100 lines. Combine multiple docs into one with TOC.
- No all-caps for emphasis. No extraneous horizontal rules. Bold/italics sparingly. Informational glyphs: † ‡ ⁑ 📌. Problem glyphs: ⚠️ ❗ 📣 🔔. One glyph per cell, unambiguous within table/list.
- Escape dollar signs in prose as `\$`. IntelliJ IDEA's markdown preview treats `$...$` as inline LaTeX math, so two unescaped `$` in the same paragraph render the text between them as italic math. Bare `$` inside table cells are safe (pipes prevent cross-cell pairing).
- Table cell vocabulary — emdash (N/A), TBD (exists, needs lookup), TODO (work needed, blocks nothing), ? (uncertain), ⚠️ (alarming, footnote required), blank only for visual grouping.
- Future work appears only as task lists or TODOs. No "Critical/Important/urgent" labels — use order. No capitalized/bolded exclamations (Bug, Gap, Pending, Next). Don't use ⚠️ where it could be confused with a TODO. Label sections "Tasks" not "Next Steps/To Do/Action Items/Plan". No future dates unless capturing a commitment.
- Hyperlinks: link the relevant text, don't parenthetically name the target. Write `dates to at least [2014](#history)` not `dates to at least 2014 (see [History](#history))` or `dates to at least 2014 ([evidence](#history))`.
- When citing a dated source (incident, analysis, ADR, etc.), put the parenthetical date *after* the action/verb and link the date to the source. Write `Rohith cataloged ([2025.09](#e-bv-sync-issue)) 5 manifestations` not `Rohith (Sep 2025) cataloged 5 manifestations`. The date is the link; the doc name is omitted.
- When mentioning a document by title, link the title itself — not a separate date or "link" word. Append `(yyyy)` or `(Mon yyyy)` after the linked title if the date provides useful context. Write `the [Variant Detailed Design](url) (Jan 2025) specifies...` not `the Variant Detailed Design page ([Jan 2025](url)) specifies...`.

## File Operations

- ❗ **Re-read immediately before every edit — no exceptions.** This is the single most important rule. Other agents and humans modify files concurrently. Writing from stale content silently destroys their work. This has happened repeatedly. If the re-read shows unexpected changes, **stop and ask** — never overwrite.
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

When the user triggers a custom command, read the command definition file for full instructions before executing. Command files live in `~/.wibey/commands/` (user-level) and `<workspace>/.wibey/commands/` or `<workspace>/shared/.wibey/commands/` (project-level). Project-level commands override user-level.

- **convo** — Park the current conversation with a visible title for Mac workspace/Mission Control switching. Definition: `~/.wibey/commands/convo.md`
- **plando** — Structured plan-and-execute workflow with aidocs task record. Definition: `<workspace>/shared/.wibey/commands/plando.md` (falls back to `~/.wibey/commands/plando.md` if it exists)
