# AI/IDE Toolchain

## Scorecard

| Feature                  | IDEA           | VS Code       | Cursor       |
|--------------------------|----------------|---------------|--------------|
| IDE                      | 2025.3.3       | 1.110 @ 03.05 | 2.6.19       |
| VSCode engine            | —              | —             | 1.105.1      |
| Wibey                    | 1.0.4          | 1.0.1         | 1.0.1        |
| └ parallel agents        | X              | X             | X            |
| └ type @ busy Wibey      | ✓              | ⚠️            | ⚠️           |
| └ context += @ file      | ✓              | <100KB        | <100KB       |
| └ context += selection   | cmd-' pill     | cmd-L pill    | ⚠️           |
| └ image paste            | often fails    | ✓             | ✓            |
| └ rich/linked paste      | X              | X             | X            |
| Github Copilot           | 1.6.1-243      | 0.39.0        | 1.388.0      |
| └ parallel agents        | ✓              | ✓             | ✓            |
| └ context += selection   | auto           | auto          | ?            |
| └ conversation name      | manual         | auto          | auto         |
| AI diff review           | per delta      | per file      | per file     |
| AI diff in other repo    | ✓              | X             | ?            |
| approval UX              | ✓              | ✓             | ✓            |
| md preview               | per doc        | only 1        | per doc      |
| md preview search        | ✓              | ✓             | X            |
| md edit plugin \*-window | ✓ shuzijun     | ✓✓ typedown   | ✓✓ typedown  |
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

- Eagerly awaiting parallel Wibey agents. For now I can run all 3 IDEs on the same repo and thus get 3-way parallelism.
- Top silly frictions: let me buffer up my next prompt, and make it super-easy to reference the current file and selection.
  - Wibey disables buffering up the next prompt in VSCode and Cursor, but allows it in IDEA. Allowing this would give 30% of the value of parallel agents. I don't like interrupting agents to add their next prompt and then tell them to first finish the previous one.
  - In no IDE does Wibey automatically track the current selection as context, which Github Copilot does in IDEA and VSCode, probably Cursor too.
  - Cursor+Wibey: Cmd-L broke! It now inserts selection context into builtin chat, not Wibey Chat.

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

### Proxy (Walmart vs personal laptop)

Proxy is configured **per machine** in Cursor User settings. Personal laptop has proxy disabled; Walmart laptop should keep proxy so Cursor can reach the internet via corporate proxy.

- **Where:** `~/Library/Application Support/Cursor/User/settings.json` (macOS). Each laptop has its own file.
- **Personal laptop (no proxy):** Remove or leave unset: `http.proxy`, `http.proxySupport`, and the Walmart-only `http.noProxy` entries. Keep `http.noProxy` with just `.local` and `169.254/16` if you like.
- **Walmart laptop (restore proxy):** Add or restore these in the same `settings.json`:

```json
"http.noProxy": [
    ".walmart.com",
    ".wal-mart.com",
    ".walmartlabs.com",
    "wmlink",
    "wamnetNAD",
    ".local",
    "169.254/16"
],
"http.proxy": "http://proxy.wal-mart.com:9080",
"http.proxySupport": "override",
"http.proxyStrictSSL": true,
"http.systemCertificates": true,
"http.fetchAdditionalSupport": true,
"http.systemCertificatesNode": false,
```

Then restart Cursor. If you use Settings Sync, turning off sync on the Walmart laptop (or re-adding these after a sync) keeps the proxy from being overwritten.

### Copilot Chat in Cursor (why it wasn’t available)

- **Cause:** Copilot has two extensions. We only installed **GitHub Copilot** (completions). **GitHub Copilot Chat** is separate and was not installed. Cursor’s marketplace doesn’t list it; the latest Chat VSIX from the VS Code marketplace requires VS Code **^1.111.0** and Cursor is on **1.105.1**, so the unpatched install is rejected.
- **Fix (patched Chat install):** A patched VSIX that accepts engine ^1.105.0 is at `~/bin/copilot-chat-patched.vsix`. **Fully quit Cursor**, then in a terminal run:
  ```bash
  cursor --install-extension ~/bin/copilot-chat-patched.vsix
  ```
  Then open Cursor again. If you see “Please restart VS Code before reinstalling…”, you must quit Cursor completely and run the command with Cursor closed. After a successful install, **Cmd+Shift+P** → “GitHub Copilot: Open Copilot” (or similar) should appear and the Copilot Chat view/panel should be available.

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
- Shuzijun Markdown Editor plugin: theme follows IDE via `UIUtil.isUnderDarcula()` — no separate theme setting. If the editor renders dark while IDE is light (e.g. after OS theme auto-switch), close and re-open the tab to fix.
