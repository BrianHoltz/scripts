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

The `~/bin/` repo also contains personal tool settings and reference docs (not symlinked):

- `~/bin/Tools.md` — IDE/editor comparison matrix, extension patches, keybinding customizations, and tool-specific configuration notes

To update these files, edit the `~/bin/` copies and commit in the `~/bin/` repo.

## ❗ Do Not Overwrite Other Writers

**Re-read every file immediately before every edit.** Other agents and humans are editing files concurrently. If you write based on stale content, you silently destroy their work. This has happened repeatedly and is the single most damaging mistake an agent can make. No edit is so urgent that it justifies skipping the re-read. If the content changed since you last saw it, stop and ask — do not overwrite.

## Coding Workflow

Use the `/tdd` command (`shared/.wibey/commands/tdd.md`) for the full TDD workflow. See `shared/docs/WibeyAgentRef.md` § Coding Workflow (TDD) for context and test execution mechanics. In repos without a `shared/` symlink: pull main, create feature branch, write failing tests, implement, run tests, run full suite, run postman/newman if available, run coverage (100% of new flows/conditions).

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

- Ad hoc docs should be created in the repo's aidocs/ folder in subfolder yyyy-mm-dd/.
- Use hhmm_CamelCase.md for naming, where hhmm is create time not modtime
- Do not use horizontal lines unless absolutely necessary
- Do not number list items unless absolutely necessary e.g. to refer to step numbers (and even then, better to have bolded step names)

### Evidence

In documents the user designates as requiring cited evidence for empirical claims, collect evidence in a dedicated `## Evidence` section placed near the bottom of the document, above any log or TODO sections. Link claims inline with the Unicode dagger character U+2020 (†), with no space before it: `claim text[†](#e-descriptive-slug)`. The `†` renders as a clickable link immediately after the supported text. Example: "Latency dropped 40% after the cache change[†](#e-latency-drop)."

Each evidence entry is a `###` heading followed by structured fields:

```
### <brief description of what is being evidenced>

<a id="e-descriptive-slug"></a>

- **Claim**: the specific assertion being backed
- **Source**: URL, file path, git commit SHA, dashboard name, or person name + role — include a locator within the source where applicable (line number, timestamp, query, panel ID, etc.)
- **Dates**: source vintage (when the source was authored/published/recorded) and date collected (ISO YYYY-MM-DD, when you retrieved or observed it)
- **Quote / data**: exact text excerpt, metric value, or command output that supports the claim
```

Omit any field that genuinely does not apply, but include as many as possible. The goal is that a skeptical reader could independently re-verify the claim from the entry alone, without asking anyone.

When a URL is available, prefer a Markdown link with descriptive anchor text over printing the raw URL — embed the locator (line number, timestamp, etc.) in the link target rather than repeating it in prose. For example, write `[AuthService:L42](https://github.com/…/auth.ts#L42)` instead of `https://github.com/…/auth.ts, line 42`.

The `[†](#e-slug)` / `<a id="…">` anchor convention works in both target environments: MD Wiki pages (GitHub/GitLab Wiki render fragment links natively) and Confluence (via the md2confluence pipeline in `~/src/relationship-shared/`).

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

When the user triggers a custom command, read the command definition file for full instructions before executing. Command files live in `~/.wibey/commands/` (user-level) and `<workspace>/.wibey/commands/` (project-level). Project-level commands override user-level.

User-level commands (personal, version-controlled in `~/bin/wibey/commands/`, symlinked from `~/.wibey/commands/`):

- **convo** — Park the current conversation with a visible title for Mac workspace/Mission Control switching. Definition: `~/.wibey/commands/convo.md`
- **commitz** — Cluster uncommitted diffs into themed buckets, draft a commit message per bucket, commit approved ones. Definition: `~/.wibey/commands/commitz.md`

Project-level commands (version-controlled in the project repo under `.wibey/commands/`):

- **plando** — Structured plan-and-execute workflow with aidocs task record. Definition: `<workspace>/shared/.wibey/commands/plando.md`. Every repo has a `shared/` symlink pointing to the shared repo; in the shared repo itself `shared/` is a self-referential symlink, so the path is consistent everywhere.
- **tdd** — TDD workflow enforcer: branch, baseline, red, green, verify, full suite, newman, coverage. Definition: `<workspace>/shared/.wibey/commands/tdd.md`.
