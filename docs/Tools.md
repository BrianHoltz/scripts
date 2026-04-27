# AI/IDE Toolchain

## IDEs


| Feature                        | IDEA         | VS Code      | Cursor      |
| ------------------------------ | ------------ | ------------ | ----------- |
| Score                          | 21.5         | 18.5         | 12.5        |
| IDE                            | 2025.3.3     | 1.116.0      | 3.1.14      |
| VSCode engine                  | —            | —            | 1.105.1     |
| Wibey                          | 1.0.7        | 1.0.8        | 1.0.6       |
| └ parallel agents              | ❌            | ❌            | ❌           |
| └ type @ busy Wibey            | ✅            | ❌❌           | ❌❌          |
| └ context += @ file            | ✅            | 🟡<100KB     | 🟡<100KB    |
| └ context += selection         | ✅ cmd-' pill | ✅ cmd-L pill | ❌❌          |
| └ image paste                  | ❌❌           | ✅            | ✅           |
| └ convo title edit             | ❌            | ✅            | ✅           |
| └ convo title auto             | last prompt  | last prompt  | last prompt |
| └ convo search                 | ❌            | ✅            | ✅           |
| └ convo timestamps             | ✅            | ✅            | ✅           |
| └ convo bookmark               | ❌            | ✅            | ✅           |
| └ rich/linked paste            | ❌            | ❌            | ❌           |
| Github Copilot                 | 1.6.1-243    | 0.39.0       | 1.388.0     |
| └ parallel agents              | ✅            | ✅            | ✅           |
| └ context += selection         | ✅ auto       | ✅ auto       | ?           |
| └ convo title                  | 🟡 manual    | ✅ auto       | ✅ auto      |
| AI diff review                 | ✅ per delta  | 🟡 per file  | 🟡 per file |
| AI diff in linked repo         | ✅            | ❌            | ❌           |
| git ops in linked repo         | ✅            | ✅            | ❌           |
| approval UX                    | ✅            | ✅            | ✅           |
| md preview                     | ✅            | 🟡 only 1    | ✅✅ wysiwyg  |
| md preview search              | ✅            | ✅            | ❌❌          |
| md table format                | ✅✅ auto      | 🟡 manual    | 🟡 manual   |
| md pastes details block        | ❌            | ✔️           | ✔️          |
| md headers paste bold to Slack | ✅            | ❌            | ❌           |
| search/find                    | ✅            | ✅            | ✅           |
| git                            | 🟡           | ✅✅           | 🟡          |
| debug                          | ✅            | ?            | ?           |
| database                       | ✅            | ❌            | ❌           |
| http                           | ✅            | ❌            | ❌           |
| editor history UI              | ✅            | 🟡           | 🟡          |


Score rubric

- Glyph values: ✅✅ = 2 pts, ✅ = 1 pt, 🟡 / ✔️ = 0.5 pts, ❌ / ? = 0 pts, ❌❌ = −1 pt
- Version/text-only cells (version numbers, descriptive text) = excluded
- Copilot rows excluded from IDE score
- Editor score: each IDE gets the maximum score achievable by any editor available to it
  - IDEA: shuzijun only (3.5 pts)
  - VS Code: best of typedown / zaaack → zaaack (4 pts)
  - Cursor: best of typedown / zaaack / Cursor native → zaaack (4 pts)
- Final score = IDE row subtotal + best editor subtotal



## Markdown Viewers/ Editors

typedown and zaaack work in both VS Code and Cursor


| Behavior                 | IDEA viewer | IDEA shuzijun       | typedown    | zaaack | Cursor native |
| ------------------------ | ----------- | ------------------- | ----------- | ------ | ------------- |
| version                  | 2025.3.3    | 2.0.5               | 1.1.7       | 0.1.13 | 2.6.19        |
| >1 tab at a time         | ✅           | ✅✅                  | ✅✅          | ❌      | ✅✅            |
| re-read changed file     | ?           | ?                   | ✅           | ?      | ?             |
| wide tables              | ?           | 🟡 scrolls but pads | ❌ truncates | ✅✅     | ❌ truncates   |
| non-bloated side padding | ?           | ❌❌                  | ❌           | ✅      | ❌             |
| shows images             | ?           | ?                   | ?           | ?      | ?             |
| find in file             | ✅           | ✅                   | ❌           | ❌      | ❌             |
| structure                | ✅           | ✅                   | ❌           | ❌      | ❌             |
| link editing             | ?           | ✔️                  | ❌           | ✔️     | ❌             |
| toolbar                  | ?           | ✔️                  | ✔️          | ✔️     | ❌             |


### IDE Keybindings


| Action         | IDEA             | VS Code     | Cursor      |
| -------------- | ---------------- | ----------- | ----------- |
| zoom in / out  | `^⌥=` / `^⌥-` ⚠️ | `⌘=` / `⌘-` | `⌘=` / `⌘-` |
| open file      | `⇧⌘O` ⚠️         | `⌘P`        | `⌘P`        |
| search project | `⇧⌘F`            | `⇧⌘F`       | `⇧⌘F`       |
| Wibey history  | ?                | ?           | ?           |
| Wibey new chat | ?                | ?           | ?           |


IDEA keybinding overrides (defaults shown in table, actual bindings below):

- ⚠️ **zoom** `^⌥=` / `^⌥-` (`ZoomInIdeAction` / `ZoomOutIdeAction`) → remapped to `⌘=` / `⌘-`. Displaced `CollapseRegion` / `ExpandRegion` (fold/unfold) — unbound and unneeded.
- ⚠️ **open file** `⇧⌘O` (`GotoFile`) → remapped to `⌘P`. Displaced `FileChooser.TogglePathBar` from `⌘P` — unneeded.

### Keybindings (swapped from defaults in VS Code and Cursor)

The default keybindings collided with preference — typedown's simpler shortcut was wasted on the less-preferred editor. Swapped via `keybindings.json` in both VS Code and Cursor:

- **typedown** "Open in WYSIWYG mode": default `^ ⌥ ⌘ M` → swapped to `⌥ ⇧ ⌘ M`
- **zaaack** "Open with markdown editor": default `⌥ ⇧ ⌘ M` → swapped to `^ ⌥ ⌘ M`
- **Markdown Preview Enhanced** (`shd101wyy.markdown-preview-enhanced`): bound `⇧ ⌘ V` to `markdown-preview-enhanced.openPreview` so Cmd+Shift+V opens Enhanced preview (which supports intra-doc anchor links) instead of the built-in preview (which has broken intra-doc links in some cases). Done via `keybindings.json`: unbind built-in `workbench.action.markdown.openPreview` from `⇧⌘V`, then bind `markdown-preview-enhanced.openPreview` to `⇧⌘V`.

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

### Panel Management (Move to Opposite Sidebar)

To move a sidebar panel (Explorer, Search, etc.) to the opposite side of the UI:

1. Press `⌘⇧P` to open the command palette
2. Run `Move View`
3. Select the panel to move (e.g., Explorer)
4. Choose **"Move to Opposite Sidebar"**

This is useful for repositioning panels between left and right sidebars as needed.

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
- *Accept All in diff review simply accepts what's on disk and ends the review — safe even if the user made local edits during review.*

### Proxy / GitHub Copilot off VPN

When VPN is off, `proxy.wal-mart.com:9080` is unreachable, blocking GitHub Copilot. Fix: add GitHub domains to `http.noProxy` so Copilot bypasses the proxy entirely (internal traffic still routes through it).

Current `http.noProxy` in `~/Library/Application Support/Code/User/settings.json` (as of 2026.04.26):

```json
"http.noProxy": [
    ".local",
    "169.254/16",
    ".walmart.com",
    ".wal-mart.com",
    ".walmartlabs.com",
    "wmlink",
    "wamnetNAD",
    "github.com",
    ".github.com",
    ".githubcopilot.com",
    ".githubusercontent.com"
]
```

`http.proxy` and `http.proxySupport: override` remain in place for all other traffic.

### Markdown Preview Font Size

The built-in preview `markdown.preview.fontSize` defaults to something tiny (was accidentally set to 6). Current settings in `~/Library/Application Support/Code/User/settings.json`:

```json
"markdown.preview.fontSize": 13,
"markdown.preview.lineHeight": 1.2,
```

### Markdown WYSIWYG Editor Font → Match Preview Font

VS Code's `[markdown]` language-specific `editor.fontFamily` applies to the raw source editor — setting it to a proportional font breaks pipe-delimited tables. **Do not use it.** Each WYSIWYG editor has its own font control:

- **TypeDown**: has `typedown.editor.fontFamily` and `typedown.editor.fontSize` settings — current matching settings in `settings.json`:
  ```json
  "typedown.editor.fontFamily": "-apple-system, BlinkMacSystemFont, 'Segoe WPC', 'Segoe UI', system-ui, 'Ubuntu', 'Droid Sans', sans-serif",
  "typedown.editor.fontSize": 13
  ```
- **Zaaack**: no settings; requires CSS patch to `media/dist/main.css` — see § Zaaack Markdown Editor Patches below

If you want a no-patch approach in VS Code user settings, set `markdown-editor.customCss` to override Zaaack's built-in monospace binding:

```json
"markdown-editor.customCss": ".vditor .vditor-reset, .vditor-ir pre.vditor-reset, .vditor-sv { font-family: -apple-system, BlinkMacSystemFont, 'Segoe WPC', 'Segoe UI', system-ui, 'Ubuntu', 'Droid Sans', sans-serif !important; font-size: 13px !important; } .vscode-light .vditor--dark .vditor-reset { color: #111111 !important; background: #ffffff !important; } .vscode-light .vditor--dark .vditor-ir pre { color: #111111 !important; }"
```

Learned behavior: if a markdown tab still looks fixed-width after changing `typedown.editor.fontFamily`, the tab is likely Zaaack (`markdown-editor.openEditor`) rather than TypeDown (`typedown.openWysiwygEditor`). In that case, `markdown-editor.customCss` is the correct knob.

### Multiple Markdown Tabs (No Reuse)

To stop VS Code from reusing a single preview/pseudo-preview tab and allow side-by-side markdown panes, set in `~/Library/Application Support/Code/User/settings.json`:

```json
"workbench.editor.enablePreview": false,
"workbench.editor.enablePreviewFromQuickOpen": false
```

For Markdown Preview Enhanced specifically, also set:

```json
"markdown-preview-enhanced.previewMode": "Multiple Previews"
```

Without this, MPE defaults to **Single Preview** and keeps one preview tab that follows whichever markdown source tab is active.
MPE notes this setting requires a window reload/restart to take effect.

Practical workflow:

- Open Markdown Preview Enhanced with `⇧⌘V` (already rebound to MPE in this setup).
- Use `⌘\\` (Split Editor) or `Open Preview to the Side` to place additional previews/editors side-by-side.
- For WYSIWYG editors, use `Reopen Editor With...` and choose either TypeDown or Markdown Editor (Zaaack); with preview reuse disabled, each opened editor stays in its own tab.

Observed result: this workflow successfully enables independent previews per markdown file.

Zaaack multi-file editor behavior is singleton by default. Root cause in `out/extension.js`: `EditorPanel.currentPanel` is treated as the only instance and prior panel is disposed when opening a different file.

Working fix: patch `~/.vscode/extensions/zaaack.markdown-editor-0.1.13/out/extension.js` to maintain a per-file map (`EditorPanel.panelsByPath`) keyed by `uri.fsPath`, reveal existing panel for the same file, and dispose only that file's panel. This allows two different markdown files to stay open in Zaaack at the same time.

Important: preview settings (`workbench.editor.enablePreview*`, MPE `previewMode`) do not solve this by themselves because they control preview reuse, not Zaaack editor panel lifecycle.

Patch caveat: extension updates overwrite patched files; reapply after each Zaaack update.

### Zaaack String Search (Limitation)

**Find/search (Cmd+F) does not work inside Zaaack WYSIWYG editor.** Root cause: Zaaack runs as a webview inside the editor, and browser search APIs inside webviews have limited integration with VS Code's find UI. The underlying vditor library does not expose a search method through Zaaack's extension API.

**Workarounds:**

1. **Outline navigation** (heading-based): Zaaack's underlying vditor supports an outline panel for jump-to-heading navigation. Suggested enhancement: add `options.outline.enable=true` to Zaaack's vditor initialization to expose heading-based navigation menu in the WYSIWYG editor.

2. **Switch to source markdown view**: Press `Ctrl+Alt+Cmd+M` to toggle back to the plain markdown source editor (or use command palette "Open Default Editor"), where `Cmd+F` works normally. This trade-off abandons WYSIWYG rendering but gains standard find.

3. **Exit webview context**: Close the Zaaack editor tab and use Markdown Preview Enhanced preview instead. Preview tabs have independent search via browser context.

Not recommended: patching Zaaack to add a custom search button would be complex (vditor's internal search is not exposed via its public API, and custom webview search requires message passing between VSCode host and vditor instance), and patches are overwritten on extension update.

Cursor parity status:

- Applied matching Cursor user settings in `~/Library/Application Support/Cursor/User/settings.json`:
  - `workbench.editor.enablePreview=false`
  - `workbench.editor.enablePreviewFromQuickOpen=false`
  - `markdown-preview-enhanced.previewMode="Multiple Previews"`
  - `markdown-preview-enhanced.previewColorScheme="systemColorScheme"`
  - `markdown.preview.fontSize=13`, `markdown.preview.lineHeight=1.2`
  - `typedown.editor.fontFamily` / `typedown.editor.fontSize`
  - `markdown-editor.customCss` override for proportional Zaaack editing font
- Applied matching Cursor keybindings in `~/Library/Application Support/Cursor/User/keybindings.json`:
  - `⇧⌘V -> markdown-preview-enhanced.openPreviewToTheSide`
  - typedown / zaaack WYSIWYG shortcut swap parity with VS Code
- Not patchable yet in Cursor on this machine: no installed `zaaack.markdown-editor-*` extension under `~/.cursor/extensions/`, so the singleton-to-multi-panel `out/extension.js` patch could not be applied there yet.

### Markdown Preview Theme (auto-switch)

If your Markdown preview (for example, Markdown Preview Enhanced) does not switch between light/dark automatically when VS Code or your OS changes theme, add this to your user `settings.json`:

```json
"markdown-preview-enhanced.previewColorScheme": "systemColorScheme"
```

This makes the preview follow the active VS Code editor theme (and thus `window.autoDetectColorScheme`). If you prefer the preview to follow the OS system color scheme directly, use `"systemColorScheme"` instead of `"editorColorScheme"`.

### Cmd+Shift+V → Markdown Preview Enhanced

The built-in Markdown preview has broken intra-doc anchor links in some situations. Markdown Preview Enhanced (`shd101wyy.markdown-preview-enhanced`) handles them correctly. `keybindings.json` unbinds `⇧⌘V` from the built-in and rebinds it to `markdown-preview-enhanced.openPreviewToTheSide` so each use opens a side preview instead of replacing the current one.

### Zaaack Markdown Editor Patches

Zaaack WYSIWYG markdown editor (zaaack.markdown-editor) has broken dark theme support: hardcoded light-theme colors for tables, text, borders, and no live theme tracking. Patches to the extension files:

- CSS in `media/dist/main.css`:
  - Extended `body[data-use-vscode-theme-color="1"] .vditor` block to also override `--textarea-text-color`, `--toolbar-icon-color`, and `--border-color` using VSCode CSS variables (`--vscode-editor-foreground`, `--vscode-panel-border`)
  - Added `body[data-use-vscode-theme-color="1"] .vditor-reset` color override using `var(--vscode-editor-foreground)`
  - Added `.vditor--dark .vditor-reset` overrides for: text color, table `tr`/`td`/`th` backgrounds and borders, `hr`, `blockquote`, `kbd`, `.vditor-panel::after` — all the hardcoded light-theme colors that the original `.vditor--dark` CSS variables didn't reach
  - Changed `font-family` on `.vditor .vditor-reset` from `var(--vscode-editor-font-family)` (monospace) to the system sans-serif stack (`-apple-system, BlinkMacSystemFont, 'Segoe WPC', 'Segoe UI', system-ui, ...`) to match the built-in Markdown preview font
  - Set `font-size` on `.vditor .vditor-reset` to `13px` to match `markdown.preview.fontSize` (Cursor: use `12px`)
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
- *Terminal Blindness observed on personal laptop in IDEA; not observed on Walmart laptop as of 2026.04.04.*
- *command-approval constipation*
- *Does not fully support parallel agents*
- *Cannot paste file/line reference!?*
- *Pending Changes panel sometimes fails to show agent-written files (new untracked files, or edits via MCP/Write tool). Check* `git status` *to catch anything the panel missed.*
- *⚠️ Accept All hazard: if the user makes local edits (including undos) while reviewing an agent diff, Accept All collapses those edits into the accept gesture and reverts them. Use per-chunk accept/reject instead.*
- Extra Info from Claude Opus 4.5:
  - **AI Assistant with JetBrains' own models + cloud options**
  - **Unmatched refactoring for Java/Kotlin (type-aware renames, extract method)**
  - **Built-in profiler and memory analysis**
  - *Expensive ($249/yr commercial, $169 w/ AI Assistant)*

### Terminal Blindness (IDEA Copilot)

This issue occurs mainly in GitHub Copilot in Intellij IDEA. Terminal output detection can fail, causing commands to appear to produce no output even though their output is visible in the terminal.

- **Where observed:** reproducible on personal laptop; **never observed on Walmart laptop** so far (as of 2026.04.04)
- **Root cause (plugin behavior):** `TerminalUtils.collectTerminalOutput()` computes `commandStartY = cursorY + historyLinesCount + cmdLines - 1` and reads `getText().drop(commandStartY)`. Over time, `cursorY` drifts toward `screenHeight`; once `commandStartY` exceeds available text lines, output capture goes blank.
- **SOTA workaround status (applied):**
  - `~/bin/bash_profile`: `BASH_SILENCE_DEPRECATION_WARNING=1`
  - `~/bin/bashrc`: JetBrains block sets `set +o noclobber`
  - `~/bin/bashrc`: JetBrains block sets `PROMPT_COMMAND='printf "\e[H\e[2J"'`
  - `~/bin/bash_profile`: JetBrains sessions preserve `.bashrc` `PROMPT_COMMAND` (no override in history block)
- **Do not use `\e[3J`:** JediTerm clears both scrollback and screen, which destroys output before Copilot can read it.
- **Limitations:** `\e[H\e[2J` is not perfect; drift can recur after enough commands. Running `clear` resets drift.
- **Fallback:** redirect command output to `tmp/YYYYMMDD_HHMMSS_agent.out`, then read the file directly and mirror it with `cat` or `tail` in terminal.

### IDEA Keybindings

IDEA keybinding overrides are stored in `~/Library/Application Support/JetBrains/IntelliJIdea2025.3/keymaps/macOS copy.xml`. Edit this file to add standard bindings:

- **Zoom**: `⌘=` / `⌘-` (remapped from `^⌥=` / `^⌥-`)
  - Action IDs: `ZoomInIdeAction` / `ZoomOutIdeAction`
  - Keystroke format: `meta equals` / `meta minus` (with alternates `meta add` / `meta subtract`)
- **Open File**: `⌘P` (remapped from `⇧⌘O`)
  - Action ID: `GotoFile`
  - Keystroke format: `meta p`

### Markdown Preview

The built-in Markdown preview uses its own setting in `~/Library/Application Support/JetBrains/IntelliJIdea2025.3/options/markdown.xml` under `MarkdownSettings.fontSize`. Current override on this machine is set to 15px:

```xml
<application>
  <component name="MarkdownSettings">
    <option name="fontSize" value="15" />
  </component>
</application>
```

This is the right knob for preview size. It is separate from the regular editor font in `~/Library/Application Support/JetBrains/IntelliJIdea2025.3/options/editor-font.xml` (`DefaultFont.FONT_SIZE`, currently 12), and there is no project-level override in `Documents/.idea/`.
Quick tweak workflow:

- In preview, use Markdown Preview increase/decrease font actions for live zoom.
- Persisted value comes from `options/markdown.xml` (`MarkdownSettings.fontSize`), not `editor-font.xml`.
- If live view does not refresh immediately, close/reopen the Markdown tab first; restart IDEA only if that still does not pick it up.

### Disable "Allow Edits to Sensitive Files" Dialog

Add this to `~/Library/Application Support/JetBrains/IntelliJIdea2025.3/early-access-registry.txt`:

```
idea.readonly.fragments.notification.enabled
false
```

Restart IDEA for changes to take effect.

### Shuzijun Markdown Editor Patches

Shuzijun Markdown Editor plugin (com.shuzijun.markdown-editor) uses Vditor, which hardcodes `font-size: 16px` for body text in `.vditor-reset`, `.vditor-sv`, and `.vditor-ir`. That's too large for IDEA's 13px UI font. Theme follows IDE via `UIUtil.isUnderDarcula()` — no separate theme setting. If the editor renders dark while IDE is light (e.g. after OS theme auto-switch), close and re-open the tab to fix.

- CSS in `vditor/style.css` inside `markdown-editor-2.0.5.jar`:
  - Added `font-size: 13px !important` override on `.vditor .vditor-reset`, `.vditor .vditor-sv`, `.vditor .vditor-ir` — overrides the Vditor default 16px across preview, split-view, and IR editing modes
- Patches apply to `~/Library/Application Support/JetBrains/IntelliJIdea2025.3/plugins/markdown-editor/lib/markdown-editor-2.0.5.jar`. Patches are overwritten on plugin update — reapply after each update. Restart IDEA after patching (tab close/reopen is not enough — IDEA caches plugin JAR resources at startup).
- Patch procedure: extract `vditor/style.css` from the JAR, add the override, repack with `jar uf`

## Wibey Skills

### usage-dashboard: UTC day-boundary bug

The `usage-dashboard` skill buckets sessions by UTC date, not local time. Sessions after ~7 PM CDT (midnight UTC) are credited to tomorrow's bar in the chart.

**Root cause** — two places in the installed scripts:

- `~/.wibey/usage/wibey_usage_lib.py`: `msg_date = ts[:10]` slices the first 10 chars of a UTC `Z` timestamp without converting to local time first.
- `~/.wibey/usage/wibey-usage`: `DATE(s.ended_at)` in the SQL GROUP BY, plus the `--days` cutoff uses `datetime.now(timezone.utc)`.

**Fix** — in both the installed files AND the skill source (`~/.wibey/skills/usage-dashboard/scripts/`):

In `wibey_usage_lib.py`, replace the raw slice with a local-time conversion:

```python
# Before (UTC):
msg_date = ts[:10] if ts and len(ts) >= 10 else None

# After (local):
from datetime import timezone
import datetime as _dt
def _utc_ts_to_local_date(ts):
    if not ts or len(ts) < 10:
        return None
    try:
        dt = _dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.astimezone().strftime("%Y-%m-%d")
    except Exception:
        return ts[:10]
msg_date = _utc_ts_to_local_date(ts)
```

In `wibey-usage`, replace the SQL `DATE(s.ended_at)` fallback with a local-time equivalent. SQLite has no built-in local-time function; easiest fix is to store the local date in the DB at record time (fix the lib above) so the fallback is rarely hit, and additionally change the `--days` cutoff:

```python
# Before:
cutoff = (datetime.now(timezone.utc) - timedelta(days=args.days)).isoformat()

# After:
cutoff = (datetime.now().astimezone() - timedelta(days=args.days)).isoformat()
```

Patches needed in two locations each time the skill is reinstalled:
- `~/.wibey/skills/usage-dashboard/scripts/wibey_usage_lib.py` (canonical)
- `~/.wibey/skills/usage-dashboard/scripts/wibey-usage` (canonical)
- `~/.wibey/usage/wibey_usage_lib.py` (installed copy)
- `~/.wibey/usage/wibey-usage` (installed copy)

After patching, existing DB rows with UTC `usage_date` values won't be retroactively corrected — they'll remain on the UTC-bucketed dates.

### usage-dashboard: auto-regeneration via SessionEnd hook

The dashboard HTML at `~/.wibey/usage/dashboard.html` is static — baked at generation time. It must be regenerated to show new sessions. The `SessionEnd` hook in `~/.claude/settings.json` calls `session-end-usage.py`, which records to the DB and then spawns `wibey-usage dash --no-open` to regenerate the HTML automatically after each session.

**Hook config** (`~/.claude/settings.json`):
```json
{
  "type": "command",
  "command": "~/.claude/hooks/session-end-usage.py",
  "timeout": 30,
  "statusMessage": "Recording usage metrics and refreshing dashboard..."
}
```
Timeout is 30s (not 10) to allow time for the dash regeneration subprocess.

**`--no-open` flag** — `wibey-usage dash --no-open` generates the HTML without opening a browser tab. Supported in both installed (`~/.wibey/usage/wibey-usage`) and skill source (`~/.wibey/skills/usage-dashboard/scripts/wibey-usage`).

**If today's data is missing:** the HTML is stale — regenerate manually: `~/.wibey/usage/wibey-usage dash`

Files that implement auto-regen (keep in sync):
- `~/.claude/hooks/session-end-usage.py` (active hook)
- `~/.wibey/skills/usage-dashboard/scripts/session-end-usage.py` (skill source)

## History

History of tool use practices, not of this doc.

- 2026.03.26 Thu: Opus gets stuck in IDEA last few days, switching to Sonnet

