# AgentRules.md - Global AI Agent Rules

Personal global rules for the user. The rules in this file apply to all repos, all AI models, all hosts. Any project-specific or model-specific AI rules override them only where they explicitly conflict.

**AgentRules.md vs AGENTS.md:** These are two different layers of agent instruction:

- **AgentRules.md** (this file) — global, cross-laptop, cross-repo, cross-model. Personal rules that always apply. Lives in `~/bin/`, synced to both laptops via git. Not team-visible; not project-specific.
- **AGENTS.md** — project/team-level supplement. Lives at the repo root (or symlinked from the team's shared repo). Adds team context: domain terminology, shared tooling, team workflows, file layout conventions. Supplements this file; does not override it.

When both apply, read both. If they conflict, AgentRules.md loses to AGENTS.md only where AGENTS.md explicitly says so. AGENTS.md can safely skip any rule already in AgentRules.md — agents will have both in context.

## Table of Contents

- [The Four Commandments](#the-four-commandments)
- [~/bin/ structure](#bin-structure)
  - [~/bin/ vs relationship-shared/](#bin-vs-relationship-shared)
- [Write Rules](#write-rules)
  - [Inode preservation](#inode-preservation)
  - [safewrite CAS pattern](#safewrite-cas-pattern)
  - [Other file operation rules](#other-file-operation-rules)
- [Communication Style](#communication-style)
- [Browser Automation](#browser-automation)
- [Inferring Intended Files](#inferring-intended-files)
- [Dates and Times](#dates-and-times)
  - [Always verify the current date](#always-verify-the-current-date)
  - [Use EDTF for all dates](#use-edtf-for-all-dates)
- [Documentation](#documentation)
- [Rules For Personal Laptop](#rules-for-personal-laptop)
  - [Family Reference Documents](#family-reference-documents)
- [Rules For Work Laptop](#rules-for-work-laptop)
  - [Coding Workflow](#coding-workflow)
  - [PR Diff Source of Truth](#pr-diff-source-of-truth)
  - [Custom Commands](#custom-commands)
    - [Project-Level Commands](#project-level-commands)

## The Four Commandments

- Be terse: from chapters to words, omit or condense until meaning changes.
- Every file write must follow the [Write Rules](#write-rules).
- Ask permission before communicating with other humans, e.g. via Slack, Jira, email, or Github comments/approvals. But just use normal caution when doing git or Confluence operations.
- Ask permission before touching >10 files. This count includes all writes, moves, renames, and deletions, across all directories. **Exception — no permission needed, ever, for any operation (including bulk deletes) on anything inside these folders at any depth:**
  - `tmp/` — scratch space; treat entire subtree as freely disposable
  - `target/classes/` — build output

## ~/bin/ structure

The canonical source of this file is `~/bin/docs/AgentRules.md`, version-controlled in the `~/bin/` repo (`github.com/BrianHoltz/scripts`). **`~/bin/` is the cross-laptop sync mechanism** — push on work laptop, pull on personal laptop. No symlinks across machines; just git. The following paths are symlinks to this file:

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

### ~/bin/ vs relationship-shared/

Two completely separate repos serve different scopes:


|                           | `~/bin/`                                     | `relationship-shared/`       |
| --------------------------- | ---------------------------------------------- | ------------------------------ |
| Git host                  | GitHub (personal, public)                    | Walmart GHE (team, internal) |
| Available on              | both laptops                                 | work laptop only             |
| Contains                  | personal tools, rules, cross-platform skills | team skills, docs, commands  |
| Access on personal laptop | always (`git pull`)                          | never (no VPN/auth)          |

**Skills by laptop:**

- **Work laptop**: team skills from `shared/.wibey/skills/` (relationship-shared); personal skills from `~/bin/wibey/skills/`
- **Personal laptop**: only `~/bin/wibey/skills/`, exposed per-workspace via `.wibey/skills/` symlinks

Skills useful on both laptops live canonically in relationship-shared (team owns them) and are manually copied to `~/bin/wibey/skills/` + committed when updated.

**When resolving a skill on personal laptop**: look in `~/bin/wibey/skills/<name>/SKILL.md`. Do not attempt to read `shared/` — the symlink doesn't exist.

**When resolving a skill on work laptop**: check `shared/.wibey/skills/` first (team version may be newer than `~/bin/` copy).

## Write Rules

**Write as you go.** After each logical unit of work, write immediately — don't accumulate. Sessions die without warning; unwritten work is lost.

**Re-read immediately before each write.** The file may have changed. In permit mode, `safewrite` exit 3 enforces this. In reviewed mode, re-read right before each Edit/Write call.

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

**Symlinks:** Before using Write on any file, check whether it is a symlink (`ls -la`). The Write tool may sever the symlink by creating a new regular file at the path rather than writing through to the target. Use Edit instead — Edit patches the existing bytes and preserves the symlink. If you must use Write (e.g. full-file rewrite), do it from the directory where the file is real, not from the symlinked path.

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

## Communication Style

- **Getting the user's attention:** use the `ailerts` skill (if available) when blocked and the user has likely switched away. Not for routine status — only when stopped and user likely doesn't know.

## Browser Automation

- When an agent needs to inspect a live page, take screenshots, or read DOM content, prefer a terminal-launched Chrome with `--remote-debugging-port` (CDP) over VS Code browser tabs.
- Default pattern on personal laptop: launch Google Chrome from the terminal with CDP enabled, then drive it via the DevTools protocol using a single shared agent profile directory, not the user's personal profile.
- Agents must NEVER point CDP Chrome at the user's personal Chrome profile, and must NEVER copy cookies or other session state out of the personal profile into an agent profile.
- Use one stable shared agent profile path for browser automation work, for example `--user-data-dir=/tmp/agent-chrome-profile`, so all agents converge on the same non-personal session state instead of creating ad hoc profiles.
- For bot-protected government sites, assume direct `curl`/`fetch_webpage` may be blocked even when an interactive browser succeeds. Treat CDP browser context as the source of truth.
- Prefer direct, parameterized page URLs when available (for example `view=electronic`) instead of brittle click navigation.
- For protected downloads, retrieve artifacts within the browser session context (request with browser credentials) rather than unauthenticated terminal HTTP calls.
- Capture evidence in a reusable triad: 1) page text extract, 2) full-page screenshot, 3) source artifact download when available.
- After recovering a missing artifact, store it in the canonical local archive path immediately and verify the file content before concluding.
- Avoid opening VS Code integrated browser tabs for agent work unless the user explicitly wants a human-view-only tab. Those tabs clutter the IDE and may not expose screenshot or DOM access to the agent.
- If a VS Code browser tab was opened only for agent investigation and a CDP-capable browser is available, switch to CDP and stop adding more IDE tabs.

## Inferring Intended Files

Resolve ambiguous file references before asking. Priority order:

**IDE (Wibey):** active tab → dirty tabs → other open tabs → workspace search → ask user. Use `getDiagnostics` scope `open-editors`. Active tab = strongest signal; dirty tab = recently edited.

**CLI:** use `git diff`, `git log -1`, shell history, or cwd to infer the most recently touched file.

**Name without path:** check `~/bin/` first, then workspace search. On work laptop also check `~/src/relationship-shared/` (symlinked as `shared`). On personal laptop also check `~/Documents/Google Drive/FamilyDocuments/`.

## Dates and Times

### Always verify the current date

Before using the current date for anything, run `date "+%Y-%m-%d %H:%M %Z"`. Run once per session or whenever needed.

### Use EDTF for all dates

With these modifications:

- Use **periods** as date component separators instead of hyphens (e.g. `2026.03.27` not `2026-03-27`). Periods prevent unwanted line breaks in cramped table layouts, are analogous to decimal points, save space in variable-width fonts, and cannot be confused with ranges.
- Use hyphens as range indicators instead of slashes (e.g. `2026.03.01-2026.03.27` not `2026-03-01/2026-03-27`). Slashes read like ratios or alternatives, not ranges.
- Use &gt;yyyy or &lt;yyyy instead of aft/bef if space is tight or you want to prevent line wraps in Markdown prose. Use >yyyy and <yyyy in data values.

## Documentation

For documentation authoring, planning docs, status/task/work-log hygiene, evidence conventions, and doc audits, use [wibey/skills/doc-audit.md](wibey/skills/doc-audit.md) as the shared reference available on both Walmart and personal laptops.

## Rules For Personal Laptop

### Family Reference Documents

For any question about family members, genealogy, life events, relationships, DNA, or the Holtz/Lusin family tree: consult `~/Documents/Google Drive/FamilyDocuments/FamilyEncyclopedia.md` first. It is the authoritative human-readable reference. `FamilyDocuments/Genealogy/FamilyTree.md` has the tree structure. Fall back to the GED file only for low-level GEDCOM detail not covered in either file.

## Rules For Work Laptop

### Coding Workflow

Use `/tdd` for the full TDD workflow: pull main, branch, failing tests, implement, run tests, full suite, coverage (100% new flows/conditions). In agent-toolkit repos (`shared/` symlink), see `shared/docs/WibeyAgentRef.md` § Coding Workflow (TDD). Run postman/newman if available.

### PR Diff Source of Truth

When reviewing a PR or describing what a branch/PR changes relative to its base:

- Use `gh pr diff <number>` (or `gh pr view <number> --json files`) as the **sole authoritative source** — this is the merge diff GitHub shows on "Files changed".
- **Never** use `git diff main..branch` — branches accumulate merge commits and ancestry artifacts that don't reflect the PR diff.
- Commits show *how* changes were made; the diff defines *what* the PR changes.
- If `gh pr diff` and `git diff main..branch` disagree, `gh pr diff` is correct. Period.

### Custom Commands

Commands source from `~/bin/wibey/commands/` and are exposed via symlinks in `~/Library/Application Support/Code/User/prompts/*.prompt.md`. When triggered, read the source file before executing.

User-level commands:

- **convo** — park conversation with visible title for Mission Control. Definition: `~/.wibey/commands/convo.md`
- **commitz** — cluster diffs into commit buckets. Definition: `~/.wibey/commands/commitz.md`

Install paths:

- Source commands: `~/bin/wibey/commands/*.md`
- Copilot symlinks: `~/Library/Application Support/Code/User/prompts/*.prompt.md`
- Source skills: `~/bin/wibey/skills/<name>/SKILL.md`
- Skill symlinks per workspace: `<workspace>/.wibey/skills/<name>/SKILL.md`

Skills are **not** supported as user-level Copilot customizations. On the personal laptop, expose skills per workspace via `.github/skills/` symlinks.

Maintenance/debug checklist:

- If `/convo` or `/commitz` is missing, verify the symlink exists in `~/Library/Application Support/Code/User/prompts/` with a `*.prompt.md` name.
- If a skill is not discovered, verify `<workspace>/.github/skills/<name>/SKILL.md` exists and points at `~/bin/wibey/skills/<name>/SKILL.md`.
- After adding or changing symlinks, reload the VS Code window.
- Keep the source files in `~/bin/wibey/`; do not rename or move them just to satisfy Copilot discovery.
- If discovery still fails, check YAML frontmatter first: `description` must be present and valid.

Project-level commands for Walmart/Wibey still live under `.wibey/commands/` or `shared/.wibey/commands/` as described below.

### Project-Level Commands

In teams using the agent-toolkit shared repo pattern, commands live at `<workspace>/shared/.wibey/commands/` and are consistent across all repos via the `shared/` symlink:

- **plando** — Structured plan-and-execute workflow with aidocs task record.
- **tdd** — TDD workflow enforcer: branch, baseline, red, green, verify, full suite, newman, coverage.
