# AI/IDE Toolchain

## Scorecard

| Feature                  | IDEA           | VS Code       | Cursor       |
|--------------------------|----------------|---------------|--------------|
| IDE                      | 2025.3.3       | 1.110 @ 03.05 | 2.6.19       |
| VSCode engine            | —              | —             | 1.105.1      |
| Wibey                    | 1.0.4          | 1.0.0         | 1.0.0        |
| parallel Wibey           | X              | X             | X            |
| type @ busy Wibey        | ✓              | X             | X            |
| context += @ file        | ✓              | <100KB        | <100KB       |
| context += selection     | cmd-' pill     | cmd-L pill    | XXXXX        |
| image paste              | ✓              | ✓             | ✓            |
| rich/linked paste        | X              | X             | X            |
| Github Copilot           |                |               |              |
| .  context += selection  | auto           | auto          | cmd-L inline |
| AI diff review           | per delta      | per file      | per file     |
| AI diff in shared        | ✓              | X             | ?            |
| approval UX              | ✓              | ✓             | ✓            |
| parallel agents          | —              | ✓             | ✓✓           |
| terminal non-blind       | X              | ✓             | ✓            |
| md preview               | per doc        | only 1        | per doc      |
| md preview search        | ✓              | ✓             | ✓            |
| md edit plugin \*-window | ✓ shuzijun     | ✓✓ wysiwyg    | ✓✓ wysiwyg   |
| md edit plugin 1-window  | ✓ shuzijun     | ✓✓ zaaack     | ✓✓ zaaack    |
| md table edit            | ✓✓ auto format | ✓ reformat    | ✓ reformat   |
| md pastes details block  | X              | ✓             | ✓            |
| search/find              | ✓✓             | ✓             | ✓            |
| git                      | ✓              | ✓✓            | ✓            |
| debug                    | ✓✓             | ?             | ?            |
| database                 | ✓✓             | X             | X            |
| http                     | ✓✓             | X             | X            |
| editor history UI        | ✓✓             | ✓             | ✓            |

## Top Frictions

- In no IDE does Wibey automatically track the current selection as context, which Github Copilot does in all 3 IDEs.
- Cursor+Wibey: Cmd-L now inserts selection context into builtin chat, not Wibey Chat

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

### TypeDown Patches

TypeDown WYSIWYG markdown editor (tarikkavaz.typedown-markdown-editor) has no settings for line-height, table padding, or list spacing. Patches to the extension files:

- CSS in `dist/extension.js`:
  - `.ProseMirror` `line-height`: changed from `1.7` to `1.4`
  - `.ProseMirror table td, .ProseMirror table th` `padding`: changed from `6px 10px` to `2px 10px`
  - Added `.ProseMirror table td p, .ProseMirror table th p { margin: 0; }` — ProseMirror wraps cell content in `<p>` tags with browser-default `1em` margins, which is the main source of tall rows
  - Added `.ProseMirror ul, .ProseMirror ol { margin-top: 0.25em; margin-bottom: 0.25em; }` and `.ProseMirror li p { margin: 0; }` — same `<p>`-in-`<li>` issue as tables
- Focus bug fix in `src/markdownEditorInitScript.js`: after a brief pause in typing, cursor/focus warped to end of document. Root cause: `onDidSaveTextDocument` sends `documentChanged` back to the webview, which calls `setEditorContent()` → `editor.commands.setContent()`, replacing the entire ProseMirror doc and destroying the selection. Fix: skip `setEditorContent()` in the `documentChanged` handler when the incoming text matches `lastMarkdown`.
- All patches apply to both `~/.vscode/extensions/` and `~/.cursor/extensions/` under `tarikkavaz.typedown-markdown-editor-<version>/`. Patches are overwritten on extension update — reapply after each update. Reload the window (Developer: Reload Window) after patching.

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
