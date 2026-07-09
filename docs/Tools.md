# AI/IDE Toolchain

## IDEs


| Feature                        | IDEA         | VS Code      | Cursor                  |
| ------------------------------ |--------------|--------------| ----------------------- |
| Score                          | 28.5         | 20.5 ⚙️      | 19.5                    |
| IDE                            | 2026.2 EAP   | 1.125.1      | 3.10.17                 |
| VSCode engine                  | —            | —            | 1.105.1                 |
| Wibey                          | 1.0.20       | 1.0.16 ⚙️    | 1.0.18                  |
| └ parallel agents             | ✅            | ✅            | ✅                      |
| └ enqueue next prompt         | ❌            | ✅            | ✅                      |
| └ context += @ file           | ✅            | 🟡<100KB     | 🟡<100KB                |
| └ context += selection        | ✅ cmd-' pill | ✅ cmd-L pill | 🟡 cmd-L pill via Agent |
| └ image paste                 | ✅ ⚙️        | ✅            | ✅                      |
| └ convo title edit            | ✅✅ ⚙️      | ✅            | ✅                      |
| └ convo title auto            | first prompt ⚙️ | last prompt  | last prompt          |
| └ convo search                | ✅            | ✅            | ✅                      |
| └ convo timestamps            | ✅            | ✅            | ✅                      |
| └ convo bookmark              | ✅            | ✅            | ✅                      |
| └ rich/linked paste           | ❌            | ❌            | ❌                      |
| Github Copilot                 | 1.11.2-251   | 0.39.0       | 1.388.0 ????            |
| └ parallel agents             | ✅            | ✅            | ✅                      |
| └ context += selection        | ✅ auto       | ❌            | ❌                      |
| └ convo title                 | 🟡 manual    | ✅ auto       | ✅ auto                 |
| AI diff review                 | ✅ per delta  | 🟡 per file  | 🟡 per file             |
| AI diff in linked repo         | ✅            | ❌            | ❌                      |
| git ops in linked repo         | ✅            | ✅            | ✅                      |
| approval UX                    | ✅            | ✅            | ✅                      |
| md preview                     | ✅            | 🟡 only 1    | ✅✅ wysiwyg            |
| md preview search              | ✅            | ✅            | ❌❌ neither            |
| md table format                | ✅✅ auto      | 🟡 manual    | 🟡 manual               |
| md pastes details block        | ❌            | ✔️           | ✔️                    |
| md headers paste bold to Slack | ✅            | ❌            | ❌                      |
| search/find                    | ✅            | ✅            | ✅                      |
| git                            | 🟡           | ✅✅           | ✅✅                    |
| debug                          | ✅            | ?            | ?                       |
| database                       | ✅            | ❌            | ❌                      |
| http                           | ✅            | ❌            | ❌                      |
| editor history UI              | ✅            | 🟡           | 🟡                      |

Score rubric

- Glyph values: ✅✅ = 2 pts, ✅ = 1 pt, 🟡 / ✔️ = 0.5 pts, ❌ / ? = 0 pts, ❌❌ = −1 pt
- ⚙️ suffix = capability provided by a local patch (`~/bin/patches/`); reapply after extension update
- Version/text-only cells (version numbers, descriptive text) = excluded
- Copilot rows excluded from IDE score
- Editor score: each IDE gets the maximum score achievable by any editor available to it
  - IDEA: native WYSIWYG editor (8.0 pts); beats viewer (7.0) and shuzijun (3.5)
  - VS Code: typedown (3.5 pts); zaaack broken ~2026.06.01 (was 7 pts w/ patch)
  - Cursor: typedown (3.5 pts); zaaack broken ~2026.06.01 (was 7 pts w/ patch)
- Final score = IDE row subtotal + best editor subtotal

## Markdown Viewers/ Editors

- VSCode md preview hangs for big files, but zaaack handles them
  - zaaack lacks: string search; intra-doc link nav; outline view. Wibey fixed them all!
- typedown and zaaack work in both VS Code and Cursor


| Behavior                 | IDEA viewer | IDEA editor | typedown     | zaaack                            | Cursor native |
| ------------------------ | ----------- | ----------- | ------------ | --------------------------------- | ------------- |
| version                  | 2026.2 EAP  | 2026.2 EAP  | 1.1.7        | 0.1.15 (VSCode) / 0.1.13 (Cursor) | 2.6.19        |
| >1 tab at a time         | ✅          | ✅✅        | ✅✅         | ✅✅                              | ✅✅          |
| re-read changed file     | ?           | ?           | ✅           | ?                                 | ?             |
| wide tables              | ✅          | ✅          | ❌ truncates | ✅✅                              | ❌ truncates  |
| non-bloated side padding | ✅          | ✅          | ❌           | ✅                                | ❌            |
| shows images             | ✅          | ✅          | ?            | ?                                 | ?             |
| find in file             | ✅          | ✅          | ❌           | ✅ ⚙️                           | ❌            |
| structure                | ✅          | ✅          | ❌           | ✅ ⚙️                           | ❌            |
| internal links           | ✅          | ❌          | ?            | ✅ ⚙️                           | ?             |
| link editing             | ?           | ✔️        | ❌           | ✔️                              | ❌            |
| toolbar                  | -           | ✔️        | ✔️         | ✔️                              | ❌            |

### IDE Keybindings


| Action         | IDEA                 | VS Code       | Cursor        |
| -------------- | -------------------- | ------------- | ------------- |
| zoom in / out  | `^⌥=` / `^⌥-` ⚠️ | `⌘=` / `⌘-` | `⌘=` / `⌘-` |
| open file      | `⇧⌘O` ⚠️         | `⌘P`         | `⌘P`         |
| search project | `⇧⌘F`              | `⇧⌘F`       | `⇧⌘F`       |
| Wibey history  | ?                    | ?             | ?             |
| Wibey new chat | ?                    | ?             | ?             |

IDEA keybinding overrides (defaults shown in table, actual bindings below):

- ⚠️ **zoom** `^⌥=` / `^⌥-` (`ZoomInIdeAction` / `ZoomOutIdeAction`) → remapped to `⌘=` / `⌘-`. Displaced `CollapseRegion` / `ExpandRegion` (fold/unfold) — unbound and unneeded.
- ⚠️ **open file** `⇧⌘O` (`GotoFile`) → remapped to `⌘P`. Displaced `FileChooser.TogglePathBar` from `⌘P` — unneeded.

### Keybindings (swapped from defaults in VS Code and Cursor)

The default keybindings collided with preference — typedown's simpler shortcut was wasted on the less-preferred editor. Swapped via `keybindings.json` in both VS Code and Cursor:

- **typedown** "Open in WYSIWYG mode": default `^ ⌥ ⌘ M` → swapped to `⌥ ⇧ ⌘ M`
- **zaaack** "Open with markdown editor": default `⌥ ⇧ ⌘ M` → swapped to `^ ⌥ ⌘ M`
- **Markdown Preview Enhanced** (`shd101wyy.markdown-preview-enhanced`): bound `⇧ ⌘ V` to `markdown-preview-enhanced.openPreview` (NOT `openPreviewToTheSide`) — MPE handles intra-doc anchor links correctly where the built-in sometimes breaks them. Using `openPreview` keeps the preview in the same editor column without splitting.

Each swap uses a `-` (unbind) entry to remove the extension default, then a positive binding with the other shortcut. typedown also has a toggle pair (`openWysiwygEditor` / `openDefaultEditor` gated on `typedown.editorIsActive`), so both commands are rebound.

Extension command IDs:

- `typedown.openWysiwygEditor` (when `!typedown.editorIsActive`) / `typedown.openDefaultEditor` (when `typedown.editorIsActive`)
- `markdown-editor.openEditor` (when `editorTextFocus && editorLangId == markdown`)

## Top Frictions

- Parallel Wibey agents now available in all three IDEs (as of 2026.06).
- Top silly frictions: let me buffer up my next prompt, and make it super-easy to reference the current file and selection.
  - Wibey allows enqueuing the next prompt while busy in VS Code and Cursor, but not in IDEA. Allowing this in IDEA would give 30% of the value of parallel agents. I don't like interrupting agents to add their next prompt and then tell them to first finish the previous one.
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

### Human-vs-Agent Conflict Diff

When an agent writes to a file while you have unsaved edits in your buffer, VS Code opens a `(in file) ↔ (in Visual Studio Code)` diff. The green `+` lines are your buffer; the red `-` lines are what's on disk. Options:

- **Edit the green lines** — make any adjustments you want right in the diff view, then ⌘S to save your version to disk.
- **Toolbar ✓ (Accept)** — writes your entire buffer to disk as-is.
- **Toolbar ↩ (Revert)** — discards your buffer and reverts to the disk version.

There are no per-hunk accept buttons in this diff type (those only appear in the 3-way merge editor).

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

**Locked configuration (2026.04.29):**

- **Markdown Preview Enhanced (MPE) preview rendering**: `14px`, `line-height: 1.2` in `~/.local/state/crossnote/style.less`
- **VS Code built-in preview** (`markdown.preview.fontSize`): `13`, `line-height: 1.2` (fallback setting; MPE uses its own renderer)
- **Apply in both Code and Cursor** for parity: `~/Library/Application Support/{Code,Cursor}/User/settings.json`

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
- **Zaaack**: uses `markdown-editor.customCss` in settings.json with font-size `13px` and `line-height: 1.2`:
  ```json
  "markdown-editor.customCss": ".vditor .vditor-reset, .vditor-ir pre.vditor-reset, .vditor-sv { font-family: -apple-system, BlinkMacSystemFont, 'Segoe WPC', 'Segoe UI', system-ui, 'Ubuntu', 'Droid Sans', sans-serif !important; font-size: 13px !important; line-height: 1.2 !important; } .vscode-light .vditor--dark .vditor-reset { color: #111111 !important; background: #ffffff !important; } .vscode-light .vditor--dark .vditor-ir pre { color: #111111 !important; }"
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

### Zaaack Find / Outline / Anchor Nav (patched)

⚙️ rows — find in file, structure, internal links — are added by `~/bin/patches/patch-zaaack.py`. Run after each Zaaack update; the script globs both `~/.vscode/extensions/` and `~/.cursor/extensions/` so one run covers both IDEs. Full patch procedure and implementation notes: **ToolMods.md → Zaaack**.

### Markdown Preview Theme (auto-switch)

If your Markdown preview (for example, Markdown Preview Enhanced) does not switch between light/dark automatically when VS Code or your OS changes theme, add this to your user `settings.json`:

```json
"markdown-preview-enhanced.previewColorScheme": "systemColorScheme"
```

This makes the preview follow the active VS Code editor theme (and thus `window.autoDetectColorScheme`). If you prefer the preview to follow the OS system color scheme directly, use `"systemColorScheme"` instead of `"editorColorScheme"`.

### Cmd+Shift+V → Markdown Preview

**VS Code:** `keybindings.json` unbinds `⇧⌘V` from the built-in and rebinds it to `markdown-preview-enhanced.openPreview` (NOT `openPreviewToTheSide`) — MPE handles intra-doc anchor links correctly where the built-in sometimes breaks them. Using `openPreview` keeps the preview in the same editor column without splitting.

**Cursor:** `⇧⌘V` uses the built-in `workbench.action.markdown.openPreview` (preference). MPE's default binding is unbound via `-markdown-preview-enhanced.openPreview` in Cursor's `keybindings.json`.

### Zaaack Markdown Editor Patches

Dark theme, font, and link color patches. Full procedure: **ToolMods.md → Zaaack**.

### TypeDown Patches

Line-height, table padding, list spacing, and focus bug patches. Full procedure: **ToolMods.md → TypeDown**.

## IDEA

- **Superior features: search/find, git, debug, database, http, yaml preview**
- **Currently on 2026.2 EAP** (auto-updated ~2026.06.27). EAP auto-updates disabled as of 2026.07.04. Intend to return to stable releases once 2026.x stable ships. EAP brought two breaking changes requiring JAR patches (see ToolMods.md).
- *Terminal Blindness observed on personal laptop in IDEA; not observed on Walmart laptop as of 2026.04.04.*
- *command-approval constipation*
- *Parallel agents now supported (as of 2026.06)*
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
- **Toggle Line Numbers**: `⌥L`
  - Action ID: `EditorToggleShowLineNumbers`
  - Keystroke format: `alt l`

### Markdown Preview

The built-in Markdown preview uses `options/markdown.xml` under `MarkdownSettings`. Font size is 15px.

**Rendering engines (2026.2 EAP):**

- **JCEF preview** (`MarkdownJCEFHtmlPanel`) — right pane in "Markdown Split Editor" and the standalone Preview tab. Respects custom CSS. Default body font: `Helvetica, Arial, freesans, sans-serif` (bundled `default.css`).
- **Compose WYSIWYG editor** (`intellij.markdown.compose.preview.jar`, class `JcefLikeMarkdownStylingKt`) — the "Markdown Editor" tab (H/B/I toolbar). Hardcodes `FontFamily.SansSerif` (= SF Pro on macOS); reads `fontSize` from settings; ignores `fontFamily` and all CSS. **Table font size and cell wrapping are also hardcoded** — not configurable without patching the JAR.

**Valid `MarkdownSettingsState` fields in 2026.2 EAP:**

- `fontSize` (int) — affects both JCEF preview and Compose editor
- `fontFamily` (string) — passed to JCEF preview; ignored by Compose editor
- `useCustomStylesheetPath` (bool) + `customStylesheetPath` (string) — single external CSS file; path **must be inside the open project**, otherwise IDEA rejects it with an "unsafe custom stylesheet" warning and falls back to the default
- `useCustomStylesheetText` (bool) + `customStylesheetText` (string) — inline CSS text embedded in the XML; no path restriction, preferred approach

**⚠️ Dead field in 2026.2:** `customStylesheets` (the list form used by 2025.3 and earlier) is silently ignored in 2026.2 EAP. IDEA never logs an error — the CSS is simply never applied.

**To apply custom CSS in 2026.2:** Settings → Languages & Frameworks → Markdown → choose "Custom stylesheet text" (inline mode) and paste CSS there. Do not use the file-path option unless the CSS file lives inside the current project.

Quick notes:

- `MarkdownSettings.fontSize` lives in `options/markdown.xml`, not `editor-font.xml`.
- Editing `markdown.xml` while IDEA is running has no effect — IDEA reads settings at startup and writes them on exit (overwriting any manual edits made while running). Use the Settings UI instead.
- After changing font size via the Settings UI, close/reopen the Markdown tab to see the change in the JCEF preview.

### Disable "Allow Edits to Sensitive Files" Dialog

Add this to `~/Library/Application Support/JetBrains/IntelliJIdea2026.2/early-access-registry.txt`:

```
idea.readonly.fragments.notification.enabled
false
```

Restart IDEA for changes to take effect.

### Shuzijun Markdown Editor Patches

Currently applied: font size patch (13px body text), IDEA 2026.2 compat fix (`JBCefApp` classloader), MCP Server plugin Services panel suppression. Full procedures: **ToolMods.md → Shuzijun** and **ToolMods.md → MCP Server Plugin**.

### JCEF Remote Mode (built-in Markdown preview + Shuzijun both broken)

**Symptom:** Built-in IDEA Markdown preview shows nothing / "No subscribers for documentReady"; Shuzijun WYSIWYG tab throws NPE in `JBCefApp.createMessageRouter()`. Both broken simultaneously.

**Root cause:** IDEA 2026.2 enables JCEF out-of-process (remote) mode by default; native CEF objects are null in remote mode, breaking all JCEF consumers. Full root cause chain and fix: **ToolMods.md → JCEF Remote Mode**.

**Fix summary:** add `-Djcef.remote.enabled=false` to `~/Library/Application Support/JetBrains/IntelliJIdea2026.2/idea.vmoptions`. Restart IDEA. **Applied:** 2026.07.02.

### Wibey Extension Patches

New conversation bug fix (`clearMessages` on `newParallelSession`). Full procedure: **ToolMods.md → Wibey Extension**.

### Wibey IDEA — Image Paste Fix (⚙️ local branch, PR pending)

**Problem:** Cmd+V with any clipboard image was silently broken. Root cause: `IdeEventQueue` intercepts Cmd+V before any Swing handler — `paste()`, input maps, and `TransferHandler` are all bypassed.

**Fix:** `IdeEventQueue.addDispatcher()` in `InputAttachmentManager.setupClipboardPaste()`. Dispatcher tied to panel `Disposable` (not project) to avoid accumulating stale handlers.

**Files:** `InputAttachmentManager.kt`, `UserInputPanel.kt` — 7 unit tests.

**PR:** [#170](https://gecgithub01.walmart.com/genaica/wibey-jetbrains-plugin/pull/170) · **Project doc:** [WibeyIDEAImagePaste.md](https://gecgithub01.walmart.com/CatalogRelationships/relationship-shared/blob/main/projects/WibeyIDEAImagePaste.md)

### Wibey IDEA — Conversation Title Features (⚙️ local branch, PR pending)

Three fixes/features on top of stock 1.0.20:

- **Sidecar persistence:** `autoNameFromMessage()` now persists to sidecar JSON; History panel no longer reverts to last prompt on refresh.
- **Active-chat title strip:** 28px strip (label + pencil) above the chat area; inline rename with Enter/Escape. Previously rename only existed in the History panel.
- **Agent-driven rename:** "rename this conversation to X" triggers `wibey_set_conversation_title` in-process MCP tool; title updates mid-stream. Requires `createSdkMcpServer` + `queryOptions.mcpServers` (not `Options.tools`).
- **User-title guard:** once a user manually renames, subsequent prompts don't overwrite it.

**Files:** `ConversationManager.kt`, `SessionManager.kt`, `NativeChatToolWindowPanel.kt`, `ChatStreamHandler.kt`, `BunBridge.kt`, `StreamChunk.kt`, bridge TS files — 22 unit tests.

**PR:** [#169](https://gecgithub01.walmart.com/genaica/wibey-jetbrains-plugin/pull/169) · **Project doc:** [WibeyTitleFeatures.md](https://gecgithub01.walmart.com/CatalogRelationships/relationship-shared/blob/main/projects/WibeyTitleFeatures.md)

### Installing Both Patches Locally

Both fixes live on `brian/local-combined` in `~/src/wibey-jetbrains-plugin` (merge of `brian/conversation-title-features` + `brian/image-paste-fix`). Branch has `jvmToolchain(17)` local workaround committed (JDK 21 auto-provision hangs through Zscaler proxy; output bytecode is identical).

**To install** (must run in Terminal.app — Wibey kills long Gradle processes):

```bash
cd ~/src/wibey-jetbrains-plugin
git checkout brian/local-combined
./gradlew buildAndInstall   # ~5 min warm cache
# restart IDEA
```

**To update after either PR branch gets new commits:**

```bash
git checkout brian/local-combined
git merge brian/conversation-title-features   # whichever changed
./gradlew buildAndInstall
```

---

## Wibey Skills

### usage-dashboard: UTC day-boundary bug

Sessions after ~7 PM CDT credited to tomorrow due to UTC bucketing. Patch applied to `wibey_usage_lib.py` + `wibey-usage`. Full procedure: **ToolMods.md → usage-dashboard**.

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

`**--no-open` flag** — `wibey-usage dash --no-open` generates the HTML without opening a browser tab. Supported in both installed (`~/.wibey/usage/wibey-usage`) and skill source (`~/.wibey/skills/usage-dashboard/scripts/wibey-usage`).

**If today's data is missing:** the HTML is stale — regenerate manually: `~/.wibey/usage/wibey-usage dash`

Files that implement auto-regen (keep in sync):

- `~/.claude/hooks/session-end-usage.py` (active hook)
- `~/.wibey/skills/usage-dashboard/scripts/session-end-usage.py` (skill source)
