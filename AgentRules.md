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
    - Status: omit blank after glyph if need to prevent breaking
      - blank: not blocked, not started
      - ▶️ DD.MM: started
      - ⏸ DD.MM: paused, on hold (since optional date)
      - ⏳ DD.MM: waiting on external (since optional date)
      - 👀 DD.MM: under review (since optional date)
      - ✅ DD.MM: completed
      - 🚫 DD.MM: won't do (optional decision date)
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

### ~/src/ repos layout

Many repos in `~/src/` have a `./shared/` symlink to `../relationship-shared/`:

- `./shared/` is a symlink to `../relationship-shared/`
- When committing changes to files under `shared/`, run git commands from the `relationship-shared` repo, not the current repo
- The `relationship-shared` repo is a separate git repo with its own history
- See `shared/docs/CatalogRelationships.md` for an overview of the repos
