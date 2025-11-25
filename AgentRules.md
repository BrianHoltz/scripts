# Global AI Agent Rules

These rules apply to all projects and all AI models. Any project-specific or model-specific AI rules override them only where they explicitly conflict. This file can be stored in (or linked from):
- ~/.config/github-copilot/intellij/global-copilot-instructions.md
- ~/.cursor/cursorrules

## Communication Style

- Don't be sycophantic.
- Be skeptical of existing code/docs and recent statements from both user and AI agents.
- Feel free to volunteer alternative ideas, and critique user suggestions.
- If you're not sure about user intent, ask clarifying questions before proceeding.

## Documentation

- Keep documentation and any comments in sync with code
- Code should tend to be self-documenting through naming, so avoid comments that are redundant with a plain reading of the code.
- Use comments mainly for documenting interfaces (e.g. JavaDoc) and for highlighting important considerations that are not obvious to the average human/agent reader.

### DRY

- Do not include things in documents that violate DRY (Don't Repeat Yourself):
    - Don't include revision history or modtime if that's available from git
    - In version-controlled docs, never include pointers to local docs that are not version-controlled.
    - Avoid version-controlled comments/docs explaining recent corrections to code/docs. Version-controlled content is for durable info. Git history is the place to record changes.

## Ad Hoc Documents

- When creating ad hoc markdown docs during conversations, do not check them into VCS.
- Place them all into the repo's aidocs/ folder in subfolder yyyy-mm-dd/.
- Use hhmm_CamelCase.md for naming, where hhmm is create time not modtime.
- If updating such an ad hoc doc created on an earlier date, move it into the current date and use modtime for hhmm.
- Do not create ad hoc documents for short (<100 lines) content that can be presented inline.
- For content that the user might need to paste as text (e.g. raw text commmit message, markdown PR description), present the content as inline raw text that can be copy-pasted, rather than rich text that doesn't paste well into text panes.

## Version Control

- Never add files to VCS without user confirmation.
- Never switch branches or switch to a commit without user confirmation.

## Terminals

### Pagers

When running a terminal command that may produce paged output, you need to prevent the command from hanging in a pager:
- ALWAYS use `git --no-pager` for git commands (e.g., `git --no-pager diff`, `git --no-pager log`)
- OR pipe commands to `cat` (e.g., `git diff | cat`, `less file.txt | cat`)
- Never run commands that will open interactive pagers like `less`, `more`, `man` without disabling pagination

### Heredocs

- Be very careful when using heredocs in terminal commands. Too often, agents will run complicated commands with sophisticated (or even nested) heredocs, and the command will hang and the agent will be unable to continue.

### Unresponsive Terminals

**This issue occurs mainly in GitHub Copilot.** Agents may occasionally lose access to command output in the terminal. **In normal operation, read terminal output directly—do not create temp files unless the terminal is actually unresponsive.**

If you notice that terminal commands are not producing visible output:

1. Rerun the command and redirect its output to a temporary file in the repo's `tmp/` folder using timestamped naming: `command > tmp/YYYYMMDD_HHMMSS_agent.out 2>&1`. The timestamp format is: 4-digit year, 2-digit month, 2-digit day, underscore, 2-digit hour (24h), 2-digit minute, 2-digit second. Use the repo's `tmp/` folder to avoid permissions problems. Then:
   - Read the file directly (e.g., with your file reading tool)
   - Also run `cat` or `tail` on the file in the terminal so the user can read along with you
2. Do not clean up temp files in `tmp/`—they are for debugging and the user may want to inspect them later. The `tmp/` folder should be gitignored.
3. If you still cannot see the output, do not attempt further workarounds. Promptly alert the user and recommend that they restart their IDE to restore terminal functionality.

Always avoid spending excessive time troubleshooting terminal output issues beyond these steps.
