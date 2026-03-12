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

When implementing a change on checked-in production code with tests, use TDD:

1. Pull main (`git pull origin main` on `main` branch), then create (or switch to) the feature branch from main. If there are uncommitted code (not docs) changes, stop and ask the user to ensure the repo is in an intended committed known-good state.
2. Run all unit tests and verify any failures are expected.
3. Write test(s) that fail on the behavior being changed/added, and verify they fail.
4. Implement the required changes.
5. Run the new tests and related tests; if any fail, return to step 4.
6. Run the entire test suite; if any unexpected failures, return to step 4.
7. If local postman/newman tests exist for the system, ask the user to run the local server. When the server is running, run the postman tests and update any related test-status doc.
8. Run coverage analysis (e.g. mvn test jacoco:report) and add tests until 100% of new flows/conditions are covered.
   - If any flows/conditions are too difficult to test, ask for guidance.

## Communication Style

- Don't be sycophantic. Be the opposite of sycophantic. You are a valuable team member and we need your best unfiltered judgements.
- Be skeptical of existing code/docs and recent statements from both user and AI agents.
- Feel free to volunteer alternative ideas, and critique user suggestions.
- If you're not sure about user intent, ask clarifying questions before proceeding.
- Avoid tables and code blocks/text boxes in conversation output — the conversation window is kept narrow, and wide elements cause horizontal scrolling. Use bullet lists or plain prose instead. Tables and code blocks are fine in files, just not in chat replies.

## Documentation

### Content Brittleness

- Keep documentation and any comments in sync with code.
- Code should tend to be self-documenting through naming, so avoid comments that are redundant with a plain reading of the code.
- Use comments mainly for documenting interfaces (e.g. JavaDoc) and for highlighting important considerations that are not obvious to the average human/agent reader.
- Never reference explicit file line numbers in enduring tech docs or code comments, because such brittle references too easily go stale. Instead reference filenames and class/method names. There is almost never a need to quote code in docs, because code will change and the docs won't be updated.
  - Exception: Evidence sections (see Evidence below) may and should cite line numbers when they anchor a specific empirical claim to a specific code snapshot. Evidence entries are inherently point-in-time; staleness is expected and acceptable.
- Never use numbered lists in version-controlled docs, as it forces excessive renumbering updates. Use headers or bullets instead, and name an item if you need to reference it.
- When updating a document that has a TOC, always check if the TOC needs updating.

### Evidence

- Every verifiable empirical claim in a document (e.g. "the code does X", "there are N rows", "the query returns Y") must cite its source — typically a file path and method reference, a git commit, an OLS/GCP query, a dashboard panel, or a person+date confirmation.
- Collect evidence in an `## Appendix: Evidence` section (or `## Appendix A: Evidence` when multiple appendices exist). Use inline markdown links to anchored entries: `([evidence](#e-descriptive-slug))`.
- Each evidence entry needs:
  - An HTML anchor: `<a id="e-descriptive-slug"></a>`
  - A heading: `### Brief description of what's being evidenced`
  - **Claim**: the specific assertion being backed
  - **Evidence**: the source of truth (query, log output, API response, etc.)
  - **Screenshot**: relative path to screenshot file (when visual evidence is relevant)
  - **Caveat**: limitations of the evidence (optional)
- For documents with many evidence items, letter-number prefixes (A1, A2, ...) are acceptable: `([evidence A1](#a1-slug))`.
- Unsourced empirical claims are assertions, not findings — label them "Inference:" or "Unverified:" until evidence is added.
- Footnote glyphs (see Over-Styling) are for table cell annotations; `([evidence](#anchor))` links are for sourcing claims in prose. Don't conflate the two.

### Over-Styling

- Avoid extraneous "---" horizontal markdown lines. Trust the headings to render appropriately.
- Never use all-caps to steal attention. Only use all-caps when quoting an all-caps string literal.
- Use bold/italics sparingly. Don't cry wolf.
  - Bold is fine when acting as a title, e.g. for the first words of a list item or first cell of a row.
- Informational footnote glyphs (in order): † (dagger), ‡ (double dagger), ⁑ (double asterisk), 📌 (pushpin). Use for neutral explanations that need no action.
- Problem footnote glyphs (in order): ⚠️ (yellow triangle), ❗ (red exclamation), 📣 (megaphone), 🔔 (bell). Use for items that need remediation or investigation.
- A cell should contain at most one footnote glyph. The glyph *is* the cell content when there's no data value; otherwise it's appended to the value (e.g. `sync commit†`).
- Within a given table or list, each footnote glyph must map to exactly one note — no ambiguity. Glyphs may be freely reused across different tables, lists, or documents.

### Table Cell Vocabulary

Standard special values for table cells, in order of increasing concern:

- **— (emdash)**: not applicable. The column's concept doesn't apply to this row.
- **TBD**: the value exists or will arrive naturally; just needs to be filled in at the appropriate time. No action required beyond looking it up.
- **TODO**: a piece of work is needed to produce the value. Blocks nothing, is blocked by nothing, so usually isn't worthy of a task or ticket.
- **?**: unknown whether the value can, should, or does exist. Signals genuine uncertainty, not just missing data.
- **⚠️**: an alarming situation — something that needs remediation or investigation. Should be linked to a footnote (see Problem footnote glyphs above) that explains the problem and says TODO if action is needed.
- **blank cell**: acceptable only for visual grouping (e.g. sub-rows inheriting a parent row's value in column 1). Otherwise use one of the above values. If you mean "not applicable", use emdash. If you mean "unknown", use ?.

### Planning

- Readers should encounter calls for future work only in two forms: task lists and TODOs.
- Task Lists
  - All plans should have a single unified tasks list. Acceptable columns:
    - Task: a terse title/description, designed not to ever need changing
    - LOE: prior estimated person days. Only needed temporarily for planning Jira ticket sizes, then remove after tickets created. Never for logging effort after the fact.
    - Jira: terse anchor text linked to the task ticket. Optional.
    - Status: no space between glyph and date. Dates are always MM.DD (never DD.MM).
      - blank: not blocked, not started
      - ▶️MM.DD: started (date started)
      - ⏳MM.DD: waiting on external (date blocked)
      - 👀MM.DD: under review (date submitted)
      - 🔍MM.DD: under investigation (date started)
      - ✅MM.DD: completed (date completed)
      - ⏸MM.DD: paused, on hold (date paused)
      - 🚫MM.DD: won't do (date decided)
      - If the tasks are in a ticketing system, consider using ticket status here
    - Notes: detailed status, explanation, etc. Begins with optional MM.DD status modtime if pertinent.
- Avoid extraneous content puporting to be about future work.
  - Never editorialize with labels like "Critical", "Important", "Read this first", "urgent" or "high-priority" -- use order to establish priority.
  - Do not capitalize or boldify exclamations like: Bug, Gap, Pending, Next
  - Do not use ⚠️ or such exclamations so that they aren't confused with Tasks or TODOs.
  - Lists of future work should have "Tasks" in their label, not
    - Next Steps: duh, first task is always "next"
    - To Do: TODO should only be used to mark future changes that block nothing and are blocked by nothing
    - Action Items: for meeting outcomes, not lists of sequential tasks
    - Plan: too synonymous with "Strategy"
  - Never use future dates unless it captures a dependency or commitment.

### DRY and History

- Be DRY (Don't Repeat Yourself):
  - Don't include revision history, modtime, etc. if that's available from the platform (e.g. git, Confluence).
  - Exception: Work Logs in project documents (see ProjectTemplate.md § Work Log) serve a different purpose than revision history — they capture *why* decisions were made and provide recovery context for agents resuming mid-task. These are not WET with git history.
  - Never say "End of document" -- even at the end of the document.
  - In version-controlled docs, never include pointers to repo docs that are not version-controlled. In particular, never link to `aidocs/` from git-controlled files — aidocs are ephemeral conversation artifacts, not durable references.
  - Avoid version-controlled comments/docs explaining recent corrections to code/docs. Version-controlled content is for durable info. Git history is the place to record changes.

### The docs/ Folder

- Content in docs/ should never mention dates unless relating to formal production events (e.g. migrations, releases of critical changes/bugfixes).
- docs/ is not about history — not even doc history.
- Don't include changelogs or revision dates in docs/ documents, because that is WET with git history.
- The only exception: release history for major features or incompatible changes.

### Ad Hoc Documents

- When creating ad hoc markdown docs during conversations, do not check them into VCS.
- For Catalog Relationships repos (those with a `./shared/` symlink), place them in `shared/aidocs/` (i.e. `relationship-shared/aidocs/`) in subfolder yyyy-mm-dd/. Do not use per-repo aidocs/ folders.
- For all other repos, place them in the repo's aidocs/ folder in subfolder yyyy-mm-dd/.
- Use hhmm_CamelCase.md for naming, where hhmm is create time not modtime.
- If updating such an ad hoc doc created on an earlier date, move it into the current date and use modtime for hhmm.
- Do not create ad hoc documents for short (<100 lines) content that can be presented inline.
- Avoid creating multiple ad hoc markdown documents at one time. Combine them into a single document with a TOC and a summary, to avoid WETness.

### Raw Text for Pasting (e.g. Commit Messages)

- For content that the user might need to paste as text (e.g. raw text commit message, raw markdown PR description), present the content as inline raw text that can be copy-pasted, rather than rich text (e.g. with bullets) that doesn't paste well into text panes.
- Do not use bullets or rich text. Make it be plain ascii text, like in a text box. Make sure that newlines get included when the user copies it for pasting.
- Do not write in run-on paragraphs. Use newlines and bullets as appropriate.

## File Operations

- Always re-read a file immediately before editing it, even if you read it recently. The user or another agent may have modified it in parallel. This enables maximal concurrent work among agents and humans.
- Never use `rm` directly. Always use `trash` command or `mv` to `~/.Trash/`
- When duplicate/conflicting files exist, always ASK which version to keep before deleting either
- Show the diff and wait for user decision

## Version Control

- Never add files to VCS without user confirmation.
- Never switch branches or switch to a commit or push or pull without user confirmation.
- Never commit changes or stage or unstage files unless you're absolutely sure the user wants that.

### PR Diff Source of Truth

When reviewing a PR or describing what a branch/PR changes relative to its base:

- Use `gh pr diff <number>` (or `gh pr view <number> --json files`) as the **sole authoritative source** of what a PR changes. This is the merge diff — exactly what GitHub shows on the "Files changed" tab.
- **Never** use `git diff main..branch` or `git log main..branch` to determine a PR's changes. Branches accumulate merge commits, intermediate history, and ancestry artifacts that do not reflect the actual PR diff. Using them will cause you to hallucinate changes that aren't part of the PR.
- Commits are useful for understanding *how* the author arrived at the changes (intent, iteration history). But the diff — not the commits — defines *what* the PR changes.
- If `gh pr diff` and `git diff main..branch` disagree, `gh pr diff` is correct. Period.

## Environment Setup

### Shell PATH

Wibey's Bash tool inherits the full user PATH from VSCode — no manual `export PATH` needed.
Shared PATH configuration lives in `~/bin/shellrc.common`, sourced by both `~/bin/zshrc` and `~/bin/bash_profile`.

## Terminals

### Pagers

When running a terminal command that may produce paged output, you need to prevent the command from hanging in a pager:

- ALWAYS use `git --no-pager` for git commands (e.g., `git --no-pager diff`, `git --no-pager log`)
- OR pipe commands to `cat` (e.g., `git diff | cat`, `less file.txt | cat`)
- Never run commands that will open interactive pagers like `less`, `more`, `man` without disabling pagination

### Heredocs

- Be very careful when using heredocs in terminal commands. Too often, agents will run complicated commands with sophisticated (or even nested) heredocs, and the command will hang and the agent will be unable to continue.

### Terminal Blindness

This issue occurs mainly in GitHub Copilot in Intellij IDEA. The terminal output detection can fail, causing commands to appear to produce no output even though their output is visible in the user's terminal.

**Root cause:** The Copilot plugin's `TerminalUtils.collectTerminalOutput()` uses `commandStartY = cursorY + historyLinesCount + cmdLines - 1` to locate output in the terminal buffer via `getText().drop(commandStartY)`. As commands accumulate, `cursorY` grows toward `screenHeight` (terminal row count). When `commandStartY` exceeds the total lines in `getText()`, `drop()` produces an empty sequence and the plugin returns blank output. The Copilot terminal tab is reused across conversations, so drift accumulates across an entire IDEA session.

**Solution (applied in `~/.bash_profile` and `~/.bashrc`):**
- `export BASH_SILENCE_DEPRECATION_WARNING=1` in `.bash_profile` — eliminates 3-line macOS bash warning at startup
- `set +o noclobber` in `.bashrc` IntelliJ block — prevents "cannot overwrite" error messages from file redirects
- `PROMPT_COMMAND='printf "\e[H\e[2J"'` in `.bashrc` IntelliJ block — after each command, moves screen content to scrollback (preserving output for Copilot to read) and resets `cursorY` to 1 via cursor-home. This prevents `commandStartY` from growing toward `screenHeight`. Terminal height does not significantly affect drift rate with this fix — output volume is what matters.
- Do NOT use `\e[3J` (ED3) — JediTerm's implementation clears BOTH scrollback AND screen (bug: should only clear scrollback per xterm spec). This destroys output before Copilot can read it.

**Limitations:** The `\e[H\e[2J` fix provides ~30 commands of reliable output capture per session. After that, gradual drift (off-by-one, then off-by-two) appears from scrollback accumulation. Running `clear` manually resets the drift at any point. Root fix requires changes to the Copilot plugin's `collectTerminalOutput()` polling loop.

**Fallback if blindness recurs:** Redirect output to a temporary file in the repo's toplevel `tmp/` folder using timestamped naming: `command > tmp/YYYYMMDD_HHMMSS_agent.out 2>&1`
- Then read the output file directly (e.g., with your file reading tool)
- Also run `cat` or `tail` on the file in the terminal so the user can read along with you
- Do not clean up temp files in `tmp/` — they are for debugging and the user may want to inspect them later. The `tmp/` folder should be gitignored.
- If you still cannot see the output after file redirection, do not attempt further workarounds. Alert the user and recommend that they restart their IDE to (temporarily) restore terminal functionality.

### PingFed Authentication

Many Walmart internal sites (Concord, DX Console, Grafana, etc.) require PingFed SSO authentication. When using agent-browser (or any browser automation) to access these sites:

- **Open your browser immediately.** If a prompt might require agent-browser for any step, open your own headed session as your first action — before reading docs, before planning, before anything else. This lets the user authenticate while you prepare, instead of blocking mid-workflow. Use `$$` (shell PID) for a unique session name that won't collide with other agents. The session persists for the full conversation and must never be closed.
- Open the page in **headed mode** (`--headed`) so the user can see and interact with the login form.
- After opening, **poll the page** in a loop (e.g. every 3-5 seconds) waiting for the login wall to disappear. Check for the PingFed login form (look for "User ID" / "Password" fields or the PingFed domain in the URL) and keep polling until the target page content appears.
- Do not assume a single fixed wait is enough — the user may need 10-30+ seconds to type credentials, handle MFA, etc.
- Do not try to fill in credentials programmatically. The user will type them.
- Polling pattern:

```bash
# Open in headed mode
$SKILL_DIR/scripts/agent-browser-wrapper.sh open "https://internal-site.walmart.com/..." --headed

# Poll until authenticated (PingFed login form disappears)
for i in $(seq 1 20); do
  sleep 3
  SNAPSHOT=$($SKILL_DIR/scripts/agent-browser-wrapper.sh snapshot -c 2>&1)
  if echo "$SNAPSHOT" | grep -q "User ID"; then
    echo "Still on PingFed login page, waiting... ($i)"
  else
    echo "Authenticated!"
    break
  fi
done
```

- If after ~60 seconds the user still hasn't authenticated, inform them and ask if they need more time.
- **Never close an authenticated browser window.** Do not call `close` at the end of a workflow or between navigations. Every `close` destroys the PingFed session, forcing the user to re-type their password and handle MFA. To navigate elsewhere, just `open` a new URL in the same session. Leave the browser open when the workflow is done.
- **Reuse your session within a conversation.** Track which browser session you opened and reuse it for all subsequent browser operations in the same conversation. PingFed auth carries across all Walmart internal sites — one login covers Jira, Confluence, Grafana, Atom, Editorial, CCM, etc.

## Dates and Times

**Always verify the current date before using it.** AI agents frequently hallucinate dates, confuse MM/DD with DD/MM, or use stale dates from context. Before creating date-stamped files or folders:

```bash
date "+%Y-%m-%d %H:%M %Z"
```

This is cheap (a few tokens for the command and output) and prevents embarrassing date hallucinations. Run this once per session or whenever you need to use the current date.

## Project-Specific Notes

### Catalog Relationships Multi-Repo Ecosystem

**CRITICAL: Auto-Discovery Pattern for Catalog Relationships Repos**

When working in any of these repo patterns in `~/src/`:
- `relationship-*` (relationship-service, relationship-bootstrap, relationship-airflow, relationship-shared)
- `variant-*` (variant-grouping-stream, variant-spark-jobs, variant-grouping-spark, variant-grouping-utils)
- `qarth-*` (qarth-group-service)
- `suggested-*` (suggested-grouping-service)
- `linked-*` (linked-fee-spark)
- `ssaas-variantbatching`

**Always check for AGENTS.md on entry:**

1. If `AGENTS.md` exists at repo root, **read it immediately** for project-specific context
2. If a `./shared/` symlink exists, it points to `../relationship-shared/` which contains:
   - Team documentation in `shared/docs/`
   - Ad hoc conversation docs in `shared/aidocs/` (use this, not per-repo aidocs/)
   - Custom Wibey skills in `shared/.wibey/skills/`
   - SQL scripts in `shared/sql/`
   - Postman collections in `shared/postman/`
   - Developer tools in `shared/tools/`

**Key Resources (read these when you need architectural context):**

- `AGENTS.md` — Agent instructions (if present, read this FIRST)
- `shared/docs/CatalogRelationships.md` — System overview, all repos, deployables
- `shared/docs/CatalogArchitecture.md` — Architecture and data flow
- `shared/docs/CatalogIDs.md` — ID types (WPID, item_id, GTIN, BVShell, etc.)
- `shared/docs/WibeyAgentRef.md` — Agent reference for ad-hoc tasks
- `shared/docs/WibeyMcpSkills.md` — Available Wibey skills and MCP servers
- `shared/docs/OperationsLog.md` — Incident history and troubleshooting
- `shared/docs/repos/<repo-name>.md` — Per-repo documentation

**Git Workflow for Shared Resources:**

- `./shared/` is a symlink to `../relationship-shared/` (a separate git repo)
- When committing changes to files under `shared/`, **cd into shared/** first to commit in the relationship-shared repo
- Other repos will see changes immediately via the symlink

**Wibey Skills Auto-Discovery:**

- Custom skills live in `shared/.wibey/skills/` (canonical location). Wibey syncs this to `.claude/skills/` but may overwrite `.claude/` copies at any time. **Always edit the `.wibey/skills/` copy — never `.claude/skills/`.**
- Skills include: atom-feed, catalog-read, ccm-config, grafana-dashboard, jira-standup, jira-ticket, klipboard, md2confluence, ols-search, service-registry
- See `shared/docs/WibeyMcpSkills.md` for usage examples

**When in doubt:** Check for `AGENTS.md` first, then `shared/docs/` for comprehensive context.

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
