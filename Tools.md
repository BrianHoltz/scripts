# AI/IDE Toolchain

## Scorecard


| Feature            | IDEA           | VS Code   | Cursor |
|--------------------|----------------|-----------|--------|
| terminal non-blind | X              | ✓         | ✓      |
| image paste        | ✓              | ✓         | ✓      |
| rich text paste    | X              | X         | X      |
| AI diff review     | per delta      | per file  | ✓      |
| approval UX        | constipation   | ✓         | ✓      |
| parallel agents    | —              | ✓         | ✓✓     |
| parallel Wibey     | X              | X         | X      |
| type @ busy Wibey  | ✓              | X         | X      |
| md preview         | toggle per doc | annoying  | ✓      |
| md edit plugin     | ✓              | ✓         | ?      |
| md table edit      | auto format    | ✓         | ✓      |
| md pastes details  | X              | ✓         | ✓      |
| search/find        | ✓✓             | ✓         | ✓      |
| git                | ✓              | ✓✓        | ✓      |
| debug              | ✓✓             | ?         | ?      |
| database           | ✓✓             | X         | X      |
| http               | ✓✓             | X         | X      |
| editor history UI  | ✓✓             | ✓         | ✓      |


## Copilot

- **Works with VS Code, Intellij IDEA, Android Studio**
- **Unlimited use of GPT4.1**
- **Supports Gemini3Pro**
- **Displays premium request usage (in IDEA and VSCode)**
- Extra Info from Claude Opus 4.5:
  - **Free tier available (2000 completions/month, 50 chat messages)**
  - **Native GitHub integration (PR summaries, issue context)**
  - **Multi-file edits in agent mode with @workspace**
  - *No MCP (Model Context Protocol) support*

## Cursor

- *every model request counts against monthly budget*
- **seamless parallel agents**
- **Displays premium usage summary (cf. "usage summary")**
- **in-context edit prompt**
- Extra Info from Claude Opus 4.5:
  - **Composer mode for multi-file refactoring**
  - **Built-in codebase indexing for semantic search**
  - **Tab completion with diff preview**
  - *Closed source, can't self-host or audit*

## VS Code

- **Supports Copilot**
- **Supports parallel agents as of 2025-12**
- Extra Info from Claude Opus 4.5:
  - **Free, open source, massive extension ecosystem**
  - **Native Copilot integration with Edit mode**
  - **Remote development (SSH, containers, WSL)**
  - *Chat panel context limited vs dedicated AI IDEs*

## IDEA

- **Superior features: search/find, git, debug, database, http, yaml preview**
- *Terminal Blindness — still confirmed in IDEA 2025.2.5 (2026-02-25)*
- *command-approval constipation*
- *Does not fully support parallel agents*
- *Cannot paste file/line reference!?*
- Extra Info from Claude Opus 4.5:
  - **AI Assistant with JetBrains' own models + cloud options**
  - **Unmatched refactoring for Java/Kotlin (type-aware renames, extract method)**
  - **Built-in profiler and memory analysis**
  - *Expensive ($249/yr commercial, $169 w/ AI Assistant)*
