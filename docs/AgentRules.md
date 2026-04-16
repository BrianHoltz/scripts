# AgentRules.md - Global AI Agent Rules

Personal global rules for the user. The rules in this file apply to all repos, all AI models, all hosts. Any project-specific or model-specific AI rules override them only where they explicitly conflict.

## The Three Commandments

- Be terse: from chapters to words, omit or condense until meaning changes.
- Every file write must follow the [Write Rules](#write-rules).
- Ask permission before touching >10 files. This count includes all writes, moves, renames, and deletions, across all directories. **Exception — no permission needed, ever, for any operation (including bulk deletes) on anything inside these folders at any depth:**
  - `tmp/` — scratch space; treat entire subtree as freely disposable
  - `target/classes/` — build output

## ~/bin/ structure

The canonical source of this file is `~/bin/docs/AgentRules.md`, version-controlled in the `~/bin/` repo (`github.com/BrianHoltz/scripts`). The following paths are symlinks to it:

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

## Communication Style TODO ailerts work v. home

- Avoid tables and code blocks in chat replies — the window is narrow; they cause scrolling. Use bullet lists or plain prose. Fine in files.
- **Getting the user's attention:** use the `ailerts` skill (if available) when blocked and the user has likely switched away. Not for routine status — only when stopped and user likely doesn't know.

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

- Ad hoc docs should be created in the repo's aidocs/ folder in subfolder yyyy-mm-dd/.
- Use hhmm_CamelCase.md for naming, where hhmm is create time not modtime
- Do not use horizontal lines unless absolutely necessary
- Do not number list items unless absolutely necessary e.g. to refer to step numbers (and even then, better to have bolded step names)
- For documentation authoring, planning docs, status/task/work-log hygiene, evidence conventions, and doc audits, use [wibey/skills/doc-audit.md](wibey/skills/doc-audit.md) as the shared reference available on both Walmart and personal laptops.

### Evidence TODO doc-audit should handle this

In designated evidence docs, collect evidence in a `## Evidence` section (near the bottom, above logs/TODOs). Link claims inline with `†` (U+2020, no space before): `claim text[†](#e-slug)`. Example: "Latency dropped 40%[†](#e-latency-drop)."

Each evidence entry is a `###` heading followed by structured fields:

```
### <brief description of what is being evidenced>

<a id="e-descriptive-slug"></a>

- **Claim**: the specific assertion being backed
- **Source**: URL, file path, git commit SHA, dashboard name, or person name + role — include a locator within the source where applicable (line number, timestamp, query, panel ID, etc.)
- **Dates**: source vintage (when the source was authored/published/recorded) and date collected (ISO YYYY-MM-DD, when you retrieved or observed it)
- **Quote / data**: exact text excerpt, metric value, or command output that supports the claim
```

Omit fields that don't apply; include as many as possible so a skeptical reader can re-verify independently.

Prefer Markdown links with locators in the target: `[AuthService:L42](https://github.com/…/auth.ts#L42)` not raw URLs.

The `[†](#e-slug)` / `<a id="…">` convention works in GitHub/GitLab MD Wiki pages and Confluence (via md2confluence).

## Rules For Personal Laptop

### Family Reference Documents

For any question about family members, genealogy, life events, relationships, DNA, or the Holtz/Lusin family tree: consult `~/Documents/Google Drive/FamilyDocuments/FamilyEncyclopedia.md` first. It is the authoritative human-readable reference. `FamilyDocuments/Genealogy/FamilyTree.md` has the tree structure. Fall back to the GED file only for low-level GEDCOM detail not covered in either file.

## Rules For Work Laptop

### Coding Workflow TODO DRY work vs home

Use `/tdd` for the full TDD workflow: pull main, branch, failing tests, implement, run tests, full suite, coverage (100% new flows/conditions). In agent-toolkit repos (`shared/` symlink), see `shared/docs/WibeyAgentRef.md` § Coding Workflow (TDD). Run postman/newman if available.

### PR Diff Source of Truth

When reviewing a PR or describing what a branch/PR changes relative to its base:

- Use `gh pr diff <number>` (or `gh pr view <number> --json files`) as the **sole authoritative source** — this is the merge diff GitHub shows on "Files changed".
- **Never** use `git diff main..branch` — branches accumulate merge commits and ancestry artifacts that don't reflect the PR diff.
- Commits show *how* changes were made; the diff defines *what* the PR changes.
- If `gh pr diff` and `git diff main..branch` disagree, `gh pr diff` is correct. Period.

### Custom Commands

Commands source from `~/bin/wibey/commands/` and are exposed via symlinks in `~/Library/Application Support/Code/User/prompts/*.prompt.md`. When triggered, read the source file before executing.

User-level commands TODO doesn't scaffolding make this WET?:

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
