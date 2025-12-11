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

### General Principles

- Keep documentation and any comments in sync with code.
- Code should tend to be self-documenting through naming, so avoid comments that are redundant with a plain reading of the code.
- Use comments mainly for documenting interfaces (e.g. JavaDoc) and for highlighting important considerations that are not obvious to the average human/agent reader.
- Never reference explicit file line numbers in comments/docs, because such brittle references too easily go stale. Instead reference filenames and class/method names. There is almost never a need to quote code in docs, because code will change and the docs won't be updated.
- When updating a document with a TOC, always check if the TOC needs updating.
- Avoid extraneous "---" horizontal markdown lines. Trust the headings to render appropriately!
- Don't try to control the reader:
  - Never use all caps to steal attention.
  - Never editorialize things as "Critical", "Important", "Read this first", etc.
  - Never mark things as "urgent"" or "high-priority", just list them first.

### DRY and History

- Do not include things in documents that violate DRY (Don't Repeat Yourself):
  - Don't include revision history or modtime if that's available from git
  - Never include metadata (e.g. last updated time) that is available from the platform (e.g. git, Confluence).
  - Never say "End of document" -- even at the end of the document.
  - In version-controlled docs, never include pointers to local docs that are not version-controlled.
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

## Version Control

- Never add files to VCS without user confirmation.
- Never switch branches or switch to a commit without user confirmation.

## Java Version Issues

### The .java-version File

When encountering Java compilation problems (wrong bytecode version, class file format errors, NoClassDefFoundError for standard library classes), **always check `.java-version` first**:

```bash
cat .java-version
```

**Common symptoms of wrong Java version:**

- `class file has wrong version 65.0, should be 61.0`
- `Unsupported class file major version`
- Compilation errors on Java 17+ syntax (records, sealed classes, pattern matching)
- Tests failing to discover or run

**Root cause:** jEnv reads `.java-version` to set the local Java version. If this file contains `1.8` when the project requires `17`, compilation will fail or produce incompatible bytecode.

**Fix:**

```bash
echo "17" > .java-version
jenv local 17
java -version  # verify
```

**Known issue:** Something (possibly IDE extensions like Red Hat Java, or jEnv shell hooks) periodically resets `.java-version` to the jEnv global version. If your global is `1.8`:

- Set jEnv global to 17: `jenv global 17`
- Or make the file immutable: `chflags uchg .java-version` (use `chflags nouchg` to edit later)
- Or add a git hook to restore it on checkout

**Prevention:** If `.java-version` is in `.gitignore` but also committed, git won't track local changes. Check `git diff HEAD -- .java-version` to see if it's been modified locally.

## Terminals

### Pagers

When running a terminal command that may produce paged output, you need to prevent the command from hanging in a pager:

- ALWAYS use `git --no-pager` for git commands (e.g., `git --no-pager diff`, `git --no-pager log`)
- OR pipe commands to `cat` (e.g., `git diff | cat`, `less file.txt | cat`)
- Never run commands that will open interactive pagers like `less`, `more`, `man` without disabling pagination

### Heredocs

- Be very careful when using heredocs in terminal commands. Too often, agents will run complicated commands with sophisticated (or even nested) heredocs, and the command will hang and the agent will be unable to continue.

### Terminal Blindness

This issue occurs mainly in GitHub Copilot. The terminal output detection can fail, causing commands to appear to produce no output even though their output is visible in the user's terminal.

**Known Issue:** Multiple workarounds have been attempted and none work reliably:

- Appending `; echo ""` to shell commands
- Simplifying shell prompts
- Wrapping commands in `bash -c '...'`
- Running `exec bash` to replace the shell process - appears to hang the terminal because the agent doesn't see the command finish

**Current mitigation:** Switching the default shell to bash (`chsh -s /bin/bash`) had no effect, because IDEA overrides the system shell. IDEA's terminal shell must be configured in **Preferences** → **Tools** → **Terminal** → **Shell path** (set to `/bin/bash`). After changing this setting, restart the terminal session.

**Known persistence issue:** The IDEA terminal shell setting reverts to `/bin/zsh` after restarting IDEA. This appears to happen because:

- IDEA may not be saving the terminal shell path setting to its configuration files
- Settings Sync (if enabled) may override local preferences
- IDEA falls back to the macOS system default shell (zsh) when no explicit path is saved

**Workarounds attempted:**

- Setting the explicit path `/bin/bash` in Preferences → Tools → Terminal → Shell path - reverts on restart
- Disabling Settings Sync - [not yet tested]
- **Per-project terminal settings - SUCCESS**: Add `TerminalOptionsManager` component to `.idea/workspace.xml`:

  ```xml
  <component name="TerminalOptionsManager">
    <option name="shellPath" value="/bin/bash" />
  </component>
  ```

  This setting is project-specific and persists across IDEA restarts. Close existing terminal tabs and open new ones to see the change take effect.

**Additional bash compatibility issue:** After switching to bash, `update_terminal_cwd: command not found` errors appeared. This is because `update_terminal_cwd` is a macOS Terminal.app-specific function that's not available in IntelliJ or other terminals. Fixed by conditionally calling it only when `$TERM_PROGRAM == "Apple_Terminal"` in `~/.bash_profile`.

**Current best practice:** Use per-project terminal shell configuration as documented above. If terminal output detection issues persist, redirect command output to files in `tmp/` as documented in the next section.

**Current best practice when terminal output is still not visible:**

- Redirect output to a temporary file in the repo's toplevel `tmp/` folder using timestamped naming: `command > tmp/YYYYMMDD_HHMMSS_agent.out 2>&1`
- Then read the output file directly (e.g., with your file reading tool)
- Also run `cat` or `tail` on the file in the terminal so the user can read along with you
- Do not clean up temp files in `tmp/` — they are for debugging and the user may want to inspect them later. The `tmp/` folder should be gitignored.
- If you still cannot see the output after file redirection, do not attempt further workarounds. Alert the user and recommend that they restart their IDE to restore terminal functionality.

## Dates and Times

**Always verify the current date before using it.** AI agents frequently hallucinate dates, confuse MM/DD with DD/MM, or use stale dates from context. Before creating date-stamped files or folders:

```bash
date "+%Y-%m-%d %H:%M %Z"
```

This is cheap (a few tokens for the command and output) and prevents embarrassing errors like creating `2025-01-09` folders in December. Run this once per session or whenever you need to use the current date.

## Toolchain Comparisons

### Copilot

- **Works with VS Code, Intellij IDEA, Android Studio**
- **Unlimited use of GPT4.1**
- **Supports Gemini3Pro**
- **Displays premium request usage (in IDEA)**

### Cursor

- *every model request counts against monthly budget*
- **seamless parallel agents**
- **Displays premium usage summary (cf. "usage summary")**
- **in-context edit prompt**

### VS Code

- **Supports Copilot**
- *Does not support parallel agents*

### IDEA

- **Superior features: search/find, git, debug, database, http, yaml preview**
- *Terminal Blindness*
- *command-approval constipation*
- *Does not fully support parallel agents*
- *Cannot paste file/line reference!?*
