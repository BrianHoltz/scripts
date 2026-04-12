# AgentRules.md - Global AI Agent Rules

> ❗ **If an agent is about to modify or delete more than 5 files, it MUST stop and ask the user for explicit permission before proceeding.** Count includes all writes, moves, renames, and deletions across all directories. No exceptions, even for seemingly mechanical or safe changes.
>
> **Be terse: from chapters to words, omit or condense until meaning changes.**
>
> **Every file write must follow the Write Protocol. See [§ Write Rules](#write-rules).**
>

These rules apply to all projects and all AI models. Any project-specific or model-specific AI rules override them only where they explicitly conflict.

## ~/bin/ structure

The canonical source of this file is `~/bin/AgentRules.md`, version-controlled in the `~/bin/` repo (`github.com/BrianHoltz/scripts`). The following paths are symlinks to it:

- `~/.claude/CLAUDE.md` — read by Claude Code CLI (and Wibey at Walmart)
- `~/.cursor/cursorrules` — read by Cursor
- `.github/copilot-instructions.md` symlink in each repo root — read by GitHub Copilot (VS Code). GitHub Copilot does NOT read `~/.claude/CLAUDE.md`; it only reads this file from the open repo root.

Other `~/bin/` files symlinked into `~/`:

- `~/.shellrc.common` → `~/bin/shellrc/shellrc.common` — shared PATH/env for zsh + bash
- `~/.zprofile` → `~/bin/shellrc/zprofile` — zsh login shell config
- `~/.zshrc` → `~/bin/shellrc/zshrc` — zsh interactive shell config
- `~/.bash_profile` → `~/bin/shellrc/bash_profile` — bash login/interactive shell config
- `~/.bashrc` → `~/bin/shellrc/bashrc` — bash interactive shell config

The `~/bin/` repo also contains personal tool settings and reference docs (not symlinked):

- `~/bin/Tools.md` — IDE/editor comparison matrix, extension patches, keybinding customizations, and tool-specific configuration notes

To update the above files, edit the `~/bin/` copies and commit in the `~/bin/` repo.

When the user mentions a file by name without a path, check under `~/bin/`.

## Write Rules

**Write as you go.** After each logical unit of work — one function, one config change, one table row — write it immediately. Don't accumulate. Sessions die without warning; unwritten work is lost. Applies to project state too: update Active Work and Work Log entries incrementally, not at the end.

**Re-read immediately before each write.** The file may have changed since you last read it — user edits, another agent, your own previous write. In permit mode, `safewrite` exit 3 enforces this mechanically. In reviewed mode, it's your responsibility: re-read right before each Edit/Write call.

Three rules for how to write:

Files requiring the fhold protocol (expand this list as the protocol matures):
- Git-tracked markdown files (`*.md`)

**Rule 1 — Files in the list above:** use `fhold` to coordinate, then write.
- Before every write: `fhold status FILE`
- **Reviewed mode** (default — no permit holds): `fhold review register FILE --agent $AGENT` (exit 0 → proceed; exit 2 → show user the MENU from `fhold -H` and wait for their choice). Write with an **inode-preserving method** (IDE Edit/Write tools, vim). The IDE shows your changes as a diff for user review. `fhold review release FILE` when you know you're done, or just let 30min TTL lapse.
- **Permit mode** (any permit holds exist): `fhold permit register FILE --agent $AGENT` if not already registered. Write with **`safewrite`**. `fhold permit release FILE --agent $AGENT` when you know you're done, or just let the 30min TTL lapse.
- **IDE diff in permit mode = violation.** If an Accept/Reject diff button appears while you're in permit mode, you used Edit/Write tools when you should have used `safewrite`. That write will race with other agents working on the file.

**Rule 2 — All other files:** use inode-preserving Edit/Write tools. IDE diff shows your changes; observer buffers stay live. No fhold needed because these other files are not expected to get concurrent edits.

**Rule 3 — Write directly** (exceptions to Rules 1–2):
- Agent-owned ephemeral temp files
- Newly-created files of any type — nothing exists yet to race against

### Inode preservation

Never update a file by creating a new one in its place. `sed -i ''` on macOS, `mv tmpfile original`, and `echo > file` all change the inode. File watchers (e.g. Typedown) watch the original inode and go blind after the swap. Safe methods: `safewrite` (truncate+rewrite), IDE Edit/Write tools, vim. In Python: `open(path, 'w').write(content)`.

### safewrite CAS pattern

```sh
HASH=$(shasum -a 256 FILE | awk '{print $1}')
python3 my_transform.py > /tmp/new_out
~/bin/safewrite FILE \
  --from /tmp/new_out \
  --expect-sha256 "$HASH" \
  --max-shrink-pct 20 \
  --sentinel-regex "^# " \
  --note "agent=claude, task=abc123"
# If output looks truncated or wrong, inspect /tmp/new_out before retrying.
```

On exit 3 (CAS mismatch): file changed since you read it. Re-read, rebuild from new state, retry. Never reuse stale content.

Run `safewrite -h` for full options. Run `fhold -h` for the fhold MENU and full protocol.

### Other file operation rules

- Never `rm` directly — use `trash` or `mv ~/.Trash/`
- Duplicate/conflicting files: ASK which to keep before deleting either
- No VCS changes unless you're certain the user wants them
- Commit granularity: independent changes → separate commits; interdependent → one commit
- **Two-tier commit policy**: mechanical changes (artifacts, formatting) → commit directly; substantive changes (logic, data, content) → `git add` and summarize for user review. User can override with "just commit it".
- TODO Agents should know when (not) to (ask to) commit/push/mirror

### PR Diff Source of Truth

When reviewing a PR or describing what a branch/PR changes relative to its base:

- Use `gh pr diff <number>` (or `gh pr view <number> --json files`) as the **sole authoritative source** of what a PR changes. This is the merge diff — exactly what GitHub shows on the "Files changed" tab.
- **Never** use `git diff main..branch` or `git log main..branch` to determine a PR's changes. Branches accumulate merge commits, intermediate history, and ancestry artifacts that do not reflect the actual PR diff. Using them will cause you to hallucinate changes that aren't part of the PR.
- Commits are useful for understanding *how* the author arrived at the changes (intent, iteration history). But the diff — not the commits — defines *what* the PR changes.
- If `gh pr diff` and `git diff main..branch` disagree, `gh pr diff` is correct. Period.

## Shared Skills

- For documentation authoring, planning docs, status/task/work-log hygiene, evidence conventions, and doc audits, use [wibey/skills/doc-audit.md](wibey/skills/doc-audit.md) as the shared reference available on both laptops.
- Keep this as a pointer-only section; the full guidance remains in the skill file.

## Coding Workflow

Use the relationship-shared project's `/tdd` command for the full TDD workflow: pull main, create feature branch, write failing tests, implement, run tests, run full suite, run coverage (100% of new flows/conditions). See also [§ Work Environment (Walmart)](#work-environment-walmart) for additional workflow details used at work.

## Communication Style

- Don't be sycophantic. Be the opposite of sycophantic. You are a valuable team member and we need your best unfiltered judgements.
- Be skeptical of existing code/docs and recent statements from both user and AI agents.
- Feel free to volunteer alternative ideas, and critique user suggestions.
- If you're not sure about user intent, ask clarifying questions before proceeding.
- Avoid tables and code blocks/text boxes in conversation output — the conversation window is kept narrow, and wide elements cause horizontal scrolling. Use bullet lists or plain prose instead. Tables and code blocks are fine in files, just not in chat replies.
- **Getting the user's attention:** If you're blocked (need input, hit an unexpected error, must confirm a destructive action) and suspect the user has switched to another window expecting you to be making progress, use the `ailerts` skill (if available) to notify them. Don't use it for routine status — only when you're stopped and the user likely doesn't know.

## Inferring User Intent from Open Editors

When the user references a file ambiguously (e.g., "this file", "that doc", "the config", or just describes content without naming a file), use the IDE's open editor tabs to resolve the reference before asking clarifying questions.

- In Wibey (Walmart only), use `getDiagnostics` with scope `open-editors` to list all open tabs. The **active tab** (marked Active) is the strongest signal — it's what the user is looking at right now.
- Use filenames to decide relevance. If the user says "the test file" and one open tab is `foo.test.ts`, that's almost certainly it. Read the file only if the name alone is ambiguous.
- If the active tab's filename doesn't match the user's reference, check the remaining open tabs before falling back to workspace-wide search or asking the user.
- A **dirty** (unsaved) tab indicates recent editing — weight it higher than clean tabs when multiple tabs could match.
- Prioritization order: active tab → dirty tabs → remaining open tabs → workspace search → ask user.

In CLI agents or other environments without editor tab access, use whatever information is immediately and efficiently available — recent git activity (`git diff`, `git log -1`), shell history, or the current working directory — to infer which file the user most recently accessed.

This is cheaper and faster than asking "which file do you mean?" and almost always resolves the reference correctly.


## README Navigation

When starting work in any directory, walk upward through parent directories looking for `README.md` files and read them for repo/folder context before proceeding. Stop at `$HOME`. Read the nearest one first (most specific), then parent ones if useful.

## Dates and Times

**Always verify the current date before using it.** AI agents frequently hallucinate dates, confuse MM/DD with DD/MM, or use stale dates from context. Before creating date-stamped files or folders:

```bash
date "+%Y-%m-%d %H:%M %Z"
```

This is cheap (a few tokens for the command and output) and prevents embarrassing date hallucinations. Run this once per session or whenever you need to use the current date.

**Use EDTF (Extended Date/Time Format) for all dates**, with these modifications:

- Use **periods** as date component separators instead of hyphens (e.g. `2026.03.27` not `2026-03-27`). Periods prevent unwanted line breaks in cramped table layouts, are analogous to decimal points, save space in variable-width fonts, and cannot be confused with ranges.
- Use hyphens as range indicators instead of slashes (e.g. `2026.03.01-2026.03.27` not `2026-03-01/2026-03-27`). Slashes read like ratios or alternatives, not ranges.
- Use &gt;yyyy or &lt;yyyy instead of aft/bef if space is tight or you want to prevent line wraps in Markdown prose. Use >yyyy and <yyyy in data values.

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

The `[†](#e-slug)` / `<a id="…">` anchor convention works in both target environments: MD Wiki pages (GitHub/GitLab Wiki render fragment links natively) and Confluence (via any md2confluence pipeline).


## Family Reference Documents

When the user asks a question about family members, genealogy, life events, relationships, DNA, or any person in the Holtz/Lusin family tree, **first consult `~/Documents/Google Drive/FamilyDocuments/FamilyEncyclopedia.md`** before asking the user or searching the GED. The encyclopedia is the authoritative, human-readable reference designed specifically so agents can answer family questions without bothering the user. Only fall back to the GED (`Holtz Lusin.ged`) for low-level GEDCOM detail not covered there.

## Custom Commands

> **Wibey only (Walmart).** Skip this section if Wibey is not available.

When the user triggers a custom command, read the command definition file for full instructions before executing. Command files live in `~/.wibey/commands/` (user-level) and `<workspace>/.wibey/commands/` (project-level). Project-level commands override user-level.

User-level commands (personal, version-controlled in `~/bin/wibey/commands/`, symlinked from `~/.wibey/commands/`):

- **convo** — Park the current conversation with a visible title for Mac workspace/Mission Control switching. Definition: `~/.wibey/commands/convo.md`
- **commitz** — Cluster uncommitted diffs into themed buckets, draft a commit message per bucket, commit approved ones. Definition: `~/.wibey/commands/commitz.md`

Project-level commands are version-controlled in the project repo under `.wibey/commands/`. See [§ Work Environment (Walmart)](#work-environment-walmart) for project-level commands used at work.

## Work Environment (Walmart)

> **Skip this section if `~/src/relationship-shared/` does not exist.**

When the user mentions a file by name without a path, also check under `~/src/relationship-shared/`.

### Coding Workflow (Work)

In repos using the agent-toolkit pattern (with a `shared/` symlink), see `shared/docs/WibeyAgentRef.md` § Coding Workflow (TDD) for test execution mechanics. Run postman/newman if available.

### Project-Level Commands (Work)

In teams using the agent-toolkit shared repo pattern, commands live at `<workspace>/shared/.wibey/commands/` and are consistent across all repos via the `shared/` symlink:

- **plando** — Structured plan-and-execute workflow with aidocs task record.
- **tdd** — TDD workflow enforcer: branch, baseline, red, green, verify, full suite, newman, coverage.
