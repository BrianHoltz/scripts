# AI/IDE Toolchain

## IDEs


| Feature                 | IDEA           | VS Code       | Cursor       |
| ------------------------- | ---------------- | --------------- | -------------- |
| Score                   | 17             | 17            | 12.5         |
| IDE                     | 2025.3.3       | 1.110 @ 03.05 | 2.6.19       |
| VSCode engine           | —             | —            | 1.105.1      |
| Wibey                   | 1.0.4          | 1.0.1         | 1.0.1        |
| └ parallel agents      | ❌             | ❌            | ❌           |
| └ type @ busy Wibey    | ✅             | ❌❌          | ❌❌         |
| └ context += @ file    | ✅             | 🟡&lt;100KB   | 🟡&lt;100KB  |
| └ context += selection | ✅ cmd-' pill  | ✅ cmd-L pill | ❌❌         |
| └ image paste          | ❌ often fails | ✅            | ✅           |
| └ convo title edit     | ❌             | ✅            | ✅           |
| └ convo title auto     | last prompt    | last prompt   | last prompt  |
| └ convo search         | ❌             | ✅            | ✅           |
| └ convo timestamps     | ✅             | ✅            | ✅           |
| └ convo bookmark       | ❌             | ✅            | ✅           |
| └ rich/linked paste    | ❌             | ❌            | ❌           |
| Github Copilot          | 1.6.1-243      | 0.39.0        | 1.388.0      |
| └ parallel agents      | ✅             | ✅            | ✅           |
| └ context += selection | ✅ auto        | ✅ auto       | ?            |
| └ convo title          | 🟡 manual      | ✅ auto       | ✅ auto      |
| AI diff review          | ✅ per delta   | 🟡 per file   | 🟡 per file  |
| AI diff in linked repo  | ✅             | ❌            | ❌           |
| git ops in linked repo  | ✅             | ✅            | ❌           |
| approval UX             | ✅             | ✅            | ✅           |
| md preview              | ✅             | 🟡 only 1     | ✅✅ wysiwyg |
| md preview search       | ✅             | ✅            | ❌❌         |
| md table format         | ✅✅ auto      | 🟡 manual     | 🟡 manual    |
| md pastes details block | ❌             | ✔️          | ✔️         |
| search/find             | ✅             | ✅            | ✅           |
| git                     | 🟡             | ✅✅          | 🟡           |
| debug                   | ✅             | ?             | ?            |
| database                | ✅             | ❌            | ❌           |
| http                    | ✅             | ❌            | ❌           |
| editor history UI       | ✅             | 🟡            | 🟡           |

<details>
<summary>Score rubric</summary>

- Glyph values: ✅✅ = 2 pts, ✅ = 1 pt, 🟡 / ✔️ = 0.5 pts, ❌ / ? = 0 pts, ❌❌ = −1 pt
- Version/text-only cells (version numbers, descriptive text) = excluded
- Copilot rows excluded from IDE score
- Editor score: each IDE gets the maximum score achievable by any editor available to it
  - IDEA: shuzijun only (0.5 pts)
  - VS Code: best of typedown / zaaack → zaaack (4 pts)
  - Cursor: best of typedown / zaaack / Cursor native → zaaack (4 pts)
- Final score = IDE row subtotal + best editor subtotal

</details>

## Markdown WYSIWYG Editors

typedown and zaaack work in both VS Code and Cursor


| Behavior                 | IDEA shuzijun       | typedown     | zaaack | Cursor native |
| -------------------------- | --------------------- | -------------- | -------- | --------------- |
| version                  | 2.0.5               | 1.1.7        | 0.1.13 | 2.6.19        |
| >1 tab at a time         | ✅✅                | ✅✅         | ❌     | ✅✅          |
| wide tables              | 🟡 scrolls but pads | ❌ truncates | ✅✅   | ❌ truncates  |
| non-bloated side padding | ❌❌                | ❌           | ✅     | ❌            |
| find in file             | ✅                  | ❌           | ❌     | ❌            |
| link editing             | ✔️                | ❌           | ✔️   | ❌            |
| toolbar                  | ✔️                | ✔️         | ✔️   | ❌            |

### IDE Keybindings

| Action          | IDEA                    | VS Code      | Cursor       |
| --------------- | ----------------------- | ------------ | ------------ |
| zoom in / out   | `^⌥=` / `^⌥-` ⚠️        | `⌘=` / `⌘-` | `⌘=` / `⌘-` |
| open file       | `⇧⌘O` ⚠️                | `⌘P`         | `⌘P`         |
| search project  | `⇧⌘F`                   | `⇧⌘F`        | `⇧⌘F`        |
| Wibey history   | ?                       | ?            | ?            |
| Wibey new chat  | ?                       | ?            | ?            |

IDEA keybinding overrides (defaults shown in table, actual bindings below):

- ⚠️ **zoom** `^⌥=` / `^⌥-` (`ZoomInIdeAction` / `ZoomOutIdeAction`) → remapped to `⌘=` / `⌘-`. Displaced `CollapseRegion` / `ExpandRegion` (fold/unfold) — unbound and unneeded.
- ⚠️ **open file** `⇧⌘O` (`GotoFile`) → remapped to `⌘P`. Displaced `FileChooser.TogglePathBar` from `⌘P` — unneeded.

### Keybindings (swapped from defaults in VS Code and Cursor)

The default keybindings collided with preference — typedown's simpler shortcut was wasted on the less-preferred editor. Swapped via `keybindings.json` in both VS Code and Cursor:

- **typedown** "Open in WYSIWYG mode": default `^ ⌥ ⌘ M` → swapped to `⌥ ⇧ ⌘ M`
- **zaaack** "Open with markdown editor": default `⌥ ⇧ ⌘ M` → swapped to `^ ⌥ ⌘ M`

Each swap uses a `-` (unbind) entry to remove the extension default, then a positive binding with the other shortcut. typedown also has a toggle pair (`openWysiwygEditor` / `openDefaultEditor` gated on `typedown.editorIsActive`), so both commands are rebound.

Extension command IDs:

- `typedown.openWysiwygEditor` (when `!typedown.editorIsActive`) / `typedown.openDefaultEditor` (when `typedown.editorIsActive`)
- `markdown-editor.openEditor` (when `editorTextFocus && editorLangId == markdown`)

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

**GitHub Copilot Chat is not supported in Cursor** — the Chat extension requires VS Code ^1.111.0 and Cursor is on 1.105.x, so it cannot be installed.

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

### Zaaack Markdown Editor Patches

Zaaack WYSIWYG markdown editor (zaaack.markdown-editor) has broken dark theme support: hardcoded light-theme colors for tables, text, borders, and no live theme tracking. Patches to the extension files:

- CSS in `media/dist/main.css`:
  - Extended `body[data-use-vscode-theme-color="1"] .vditor` block to also override `--textarea-text-color`, `--toolbar-icon-color`, and `--border-color` using VSCode CSS variables (`--vscode-editor-foreground`, `--vscode-panel-border`)
  - Added `body[data-use-vscode-theme-color="1"] .vditor-reset` color override using `var(--vscode-editor-foreground)`
  - Added `.vditor--dark .vditor-reset` overrides for: text color, table `tr`/`td`/`th` backgrounds and borders, `hr`, `blockquote`, `kbd`, `.vditor-panel::after` — all the hardcoded light-theme colors that the original `.vditor--dark` CSS variables didn't reach
  - Added `font-size` override to `.vditor .vditor-reset` to override the default 16px: **VS Code uses 13px**, **Cursor uses 12px** for better readability
- Theme change listener in `out/extension.js`:
  - Added `vscode.window.onDidChangeActiveColorTheme` listener that re-sends `type: 'init'` to the webview with the new theme, so the editor re-initializes with correct dark/light mode when VSCode theme changes
  - Fixed initial theme detection to treat `HighContrast` as dark (was only checking `Dark`)
- Patches apply to `~/.vscode/extensions/` under `zaaack.markdown-editor-<version>/`. Patches are overwritten on extension update — reapply after each update. Reload the window (Developer: Reload Window) after patching.

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
- *Pending Changes panel sometimes fails to show agent-written files (new untracked files, or edits via MCP/Write tool). Check* `git status` *to catch anything the panel missed.*
- Extra Info from Claude Opus 4.5:
  - **AI Assistant with JetBrains' own models + cloud options**
  - **Unmatched refactoring for Java/Kotlin (type-aware renames, extract method)**
  - **Built-in profiler and memory analysis**
  - *Expensive ($249/yr commercial, $169 w/ AI Assistant)*

### Shuzijun Markdown Editor Patches

Shuzijun Markdown Editor plugin (com.shuzijun.markdown-editor) uses Vditor, which hardcodes `font-size: 16px` for body text in `.vditor-reset`, `.vditor-sv`, and `.vditor-ir`. That's too large for IDEA's 13px UI font. Theme follows IDE via `UIUtil.isUnderDarcula()` — no separate theme setting. If the editor renders dark while IDE is light (e.g. after OS theme auto-switch), close and re-open the tab to fix.

- CSS in `vditor/style.css` inside `markdown-editor-2.0.5.jar`:
  - Added `font-size: 13px !important` override on `.vditor .vditor-reset`, `.vditor .vditor-sv`, `.vditor .vditor-ir` — overrides the Vditor default 16px across preview, split-view, and IR editing modes
- Patches apply to `~/Library/Application Support/JetBrains/IntelliJIdea2025.3/plugins/markdown-editor/lib/markdown-editor-2.0.5.jar`. Patches are overwritten on plugin update — reapply after each update. Restart IDEA after patching (tab close/reopen is not enough — IDEA caches plugin JAR resources at startup).
- Patch procedure: extract `vditor/style.css` from the JAR, add the override, repack with `jar uf`.
