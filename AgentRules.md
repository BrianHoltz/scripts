# AgentRules.md - Global AI Agent Rules

These rules apply to all projects and all AI models. Any project-specific or model-specific AI rules override them only where they explicitly conflict. This file can be stored in (or symlinked from):

- ~/.config/github-copilot/intellij/global-copilot-instructions.md
- ~/.cursor/cursorrules
- ~/.claude/CLAUDE.md

## Coding Workflow

When implementing a change on checked-in production code with tests, use TDD:

1. If there are uncommitted code (not docs) changes or main needs pulling, stop and ask the user to ensure the repo is in an intended committed known-good state with no changes that need merging from main.
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

## Documentation

### Content Brittleness

- Keep documentation and any comments in sync with code.
- Code should tend to be self-documenting through naming, so avoid comments that are redundant with a plain reading of the code.
- Use comments mainly for documenting interfaces (e.g. JavaDoc) and for highlighting important considerations that are not obvious to the average human/agent reader.
- Never reference explicit file line numbers in comments/docs, because such brittle references too easily go stale. Instead reference filenames and class/method names. There is almost never a need to quote code in docs, because code will change and the docs won't be updated.
- Never use numbered lists in version-controlled docs, as it forces excessive renumbering updates. Use headers or bullets instead, and name an item if you need to reference it.
- When updating a document that has a TOC, always check if the TOC needs updating.

### Over-Styling

- Avoid extraneous "---" horizontal markdown lines. Trust the headings to render appropriately.
- Never use all-caps to steal attention. Only use all-caps when quoting an all-caps string literal.
- Use bold/italics sparingly. Don't cry wolf.
  - Bold is fine when acting as a title, e.g. for the first words of a list item or first cell of a row.
  
### Planning

- Readers should encounter calls for future work only in two forms: task lists and TODOs.
- Task Lists
  - All plans should have a single unified tasks list. Acceptable columns:
    - Task: a terse title/description, designed not to ever need changing
    - LOE: prior estimated person days. Optional for planning, never for logging.
    - Jira: terse anchor text linked to the task ticket. Optional.
    - Status: no space between glyph and date
      - blank: not blocked, not started
      - ▶️DD.MM: started (date started)
      - ⏳DD.MM: waiting on external (date blocked)
      - 👀DD.MM: under review (date submitted)
      - ✅DD.MM: completed (date completed)
      - ⏸DD.MM: paused, on hold (date paused)
      - 🚫DD.MM: won't do (date decided)
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
  - Never say "End of document" -- even at the end of the document.
  - In version-controlled docs, never include pointers to repo docs that are not version-controlled.
  - Avoid version-controlled comments/docs explaining recent corrections to code/docs. Version-controlled content is for durable info. Git history is the place to record changes.

### The docs/ Folder

- Content in docs/ should never mention dates unless relating to formal production events (e.g. migrations, releases of critical changes/bugfixes).
- docs/ is not about history — not even doc history.
- Don't include changelogs or revision dates in docs/ documents, because that is WET with git history.
- The only exception: release history for major features or incompatible changes.

### Ad Hoc Documents

- When creating ad hoc markdown docs during conversations, do not check them into VCS.
- Place them all into the repo's aidocs/ folder in subfolder yyyy-mm-dd/.
- Use hhmm_CamelCase.md for naming, where hhmm is create time not modtime.
- If updating such an ad hoc doc created on an earlier date, move it into the current date and use modtime for hhmm.
- Do not create ad hoc documents for short (<100 lines) content that can be presented inline.
- Avoid creating multiple ad hoc markdown documents at one time. Combine them into a single document with a TOC and a summary, to avoid WETness.

### Raw Text for Pasting (e.g. Commit Messages)

- For content that the user might need to paste as text (e.g. raw text commit message, raw markdown PR description), present the content as inline raw text that can be copy-pasted, rather than rich text (e.g. with bullets) that doesn't paste well into text panes.
- Do not use bullets or rich text. Make it be plain ascii text, like in a text box. Make sure that newlines get included when the user copies it for pasting.
- Do not write in run-on paragraphs. Use newlines and bullets as appropriate.

## File Operations

- Never use `rm` directly. Always use `trash` command or `mv` to `~/.Trash/`
- When duplicate/conflicting files exist, always ASK which version to keep before deleting either
- Show the diff and wait for user decision

## Version Control

- Never add files to VCS without user confirmation.
- Never switch branches or switch to a commit or push or pull without user confirmation.
- Never commit changes or stage or unstage files unless you're absolutely sure the user wants that.

## Environment Setup

### Shell PATH

When using the Bash tool, the default PATH is limited. Use the full user PATH for tool availability:

```bash
export PATH="/Users/b0h0166/.local/bin:/Users/b0h0166/google-cloud-sdk/bin:/Users/b0h0166/bin:/Library/Java/JavaVirtualMachines/zulu-17.jdk/Contents/Home/bin:/Users/b0h0166/.jenv/shims:/opt/homebrew/Cellar/scala@2.12/2.12.18/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin:/usr/local/sbin:/usr/local/munki:/Users/b0h0166/Library/Application Support/JetBrains/Toolbox/scripts:/Users/b0h0166/.sledge/bin:/opt/homebrew/opt/kafka/bin"
```

Key tools available:
- newman: `/opt/homebrew/bin/newman`
- mvn: IntelliJ bundled at `/Applications/IntelliJ IDEA.app/Contents/plugins/maven/lib/maven3/bin/mvn`
- java: `/Library/Java/JavaVirtualMachines/zulu-17.jdk/Contents/Home/bin/java`

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

**Known Issue:** Multiple workarounds have been attempted and none work reliably:

- Appending `; echo ""` to shell commands
- Simplifying shell prompts
- Wrapping commands in `bash -c '...'`
- Running `exec bash` to replace the shell process - appears to hang the terminal because the agent doesn't see the command finish
- Switching the default shell to bash (`chsh -s /bin/bash`)
- Setting the explicit path `/bin/bash` in Preferences → Tools → Terminal → Shell path
- Add `TerminalOptionsManager` component to `.idea/workspace.xml`:

  ```xml
  <component name="TerminalOptionsManager">
    <option name="shellPath" value="/bin/bash" />
  </component>
  ```

**Current best practice:** Use per-project terminal shell configuration as documented above. If terminal output detection issues persist, redirect output to a temporary file in the repo's toplevel `tmp/` folder using timestamped naming: `command > tmp/YYYYMMDD_HHMMSS_agent.out 2>&1`
- Then read the output file directly (e.g., with your file reading tool)
- Also run `cat` or `tail` on the file in the terminal so the user can read along with you
- Do not clean up temp files in `tmp/` — they are for debugging and the user may want to inspect them later. The `tmp/` folder should be gitignored.
- If you still cannot see the output after file redirection, do not attempt further workarounds. Alert the user and recommend that they restart their IDE to (temporarily) restore terminal functionality.

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

- Custom skills in `shared/.wibey/skills/` are automatically available in repos with the shared symlink
- Skills include: atom-feed, catalog-read, ccm-config, grafana-dashboard, ols-search, service-registry
- See `shared/docs/WibeyMcpSkills.md` for usage examples

**When in doubt:** Check for `AGENTS.md` first, then `shared/docs/` for comprehensive context.

## Custom Commands

### convo

Park the current conversation for identification in Mac workspace/Mission Control switching.

Trigger: user says "convo" or "Convo"

Steps:
- If trigger is capitalized ("Convo"), emit 30 `&nbsp;` lines as raw markdown (not via bash — bash newlines don't render in chat)
- Run `date "+%Y-%m-%d %H:%M %Z"` via Bash to get the current date
- Determine the repo emoji by reading `.idea/workspace.xml` in the current workspace and parsing the `customColor` RGBA hex:
  - `ff0000ff` → 🔴 (relationship-service)
  - `ffa500ff` → 🟠 (relationship-bootstrap, relationship-airflow, linked-fee-spark)
  - `ffff00ff` → 🟡 (relationship-shared)
  - `008000ff` → 🟢 (qarth-group-service)
  - `0000ffff` → 🔵 (variant-grouping-stream)
  - `8000ffff` → 🟣 (suggested-grouping-service, ssaas-variantbatching, variant-spark-jobs)
  - no color set or unknown → omit emoji
- Emit the date and title as two H1 bold lines, with HR rules above and below, and the emoji prepended to the title:

---
# **YYYY-MM-DD HH:MM TZ**
# **{emoji} Terse Conversation Title**

---

Choose the title yourself from the conversation context — do not ask the user.
