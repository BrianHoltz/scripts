# AI/IDE Toolchain

## IDEs


| Feature                        | IDEA         | VS Code      | Cursor                  |
| ------------------------------ | ------------ | ------------ | ----------------------- |
| Score                          | 21.5         | 21.5 ⚙️      | 12.5                    |
| IDE                            | 2025.3.3     | 1.119        | 3.3.27                  |
| VSCode engine                  | —            | —            | 1.105.1                 |
| Wibey                          | 1.0.7        | 1.10         | 1.0.6                   |
| └ parallel agents              | ❌            | ❌            | ❌                       |
| └ type @ busy Wibey            | ✅            | ❌❌           | ❌❌                      |
| └ context += @ file            | ✅            | 🟡<100KB     | 🟡<100KB                |
| └ context += selection         | ✅ cmd-' pill | ✅ cmd-L pill | 🟡 cmd-L pill via Agent |
| └ image paste                  | ❌❌           | ✅            | ✅                       |
| └ convo title edit             | ❌            | ✅            | ✅                       |
| └ convo title auto             | last prompt  | last prompt  | last prompt             |
| └ convo search                 | ❌            | ✅            | ✅                       |
| └ convo timestamps             | ✅            | ✅            | ✅                       |
| └ convo bookmark               | ❌            | ✅            | ✅                       |
| └ rich/linked paste            | ❌            | ❌            | ❌                       |
| Github Copilot                 | 1.6.1-243    | 0.39.0       | 1.388.0 ????            |
| └ parallel agents              | ✅            | ✅            | ✅                       |
| └ context += selection         | ✅ auto       | ❌            | ❌                       |
| └ convo title                  | 🟡 manual    | ✅ auto       | ✅ auto                  |
| AI diff review                 | ✅ per delta  | 🟡 per file  | 🟡 per file             |
| AI diff in linked repo         | ✅            | ❌            | ❌                       |
| git ops in linked repo         | ✅            | ✅            | ✅                       |
| approval UX                    | ✅            | ✅            | ✅                       |
| md preview                     | ✅            | 🟡 only 1    | ✅✅ wysiwyg              |
| md preview search              | ✅            | ✅            | ❌❌ neither              |
| md table format                | ✅✅ auto      | 🟡 manual    | 🟡 manual               |
| md pastes details block        | ❌            | ✔️           | ✔️                      |
| md headers paste bold to Slack | ✅            | ❌            | ❌                       |
| search/find                    | ✅            | ✅            | ✅                       |
| git                            | 🟡           | ✅✅           | ✅✅                      |
| debug                          | ✅            | ?            | ?                       |
| database                       | ✅            | ❌            | ❌                       |
| http                           | ✅            | ❌            | ❌                       |
| editor history UI              | ✅            | 🟡           | 🟡                      |


Score rubric

- Glyph values: ✅✅ = 2 pts, ✅ = 1 pt, 🟡 / ✔️ = 0.5 pts, ❌ / ? = 0 pts, ❌❌ = −1 pt
- ⚙️ suffix = capability provided by a local patch (`~/bin/patches/`); reapply after extension update
- Version/text-only cells (version numbers, descriptive text) = excluded
- Copilot rows excluded from IDE score
- Editor score: each IDE gets the maximum score achievable by any editor available to it
  - IDEA: shuzijun only (3.5 pts)
  - VS Code: best of typedown / zaaack → zaaack patched (7 pts; +3 from `patch-zaaack.py`)
  - Cursor: best of typedown / zaaack / Cursor native → zaaack patched (7 pts; same `patch-zaaack.py` covers both IDE extension dirs)
- Final score = IDE row subtotal + best editor subtotal

## Markdown Viewers/ Editors

- VSCode md preview hangs for big files, but zaaack handles them
  - zaaack lacks: string search; intra-doc link nav; outline view. Wibey fixed them all!
- typedown and zaaack work in both VS Code and Cursor


| Behavior                 | IDEA viewer | IDEA shuzijun       | typedown    | zaaack | Cursor native |
| ------------------------ | ----------- | ------------------- | ----------- | ------ | ------------- |
| version                  | 2025.3.3    | 2.0.5               | 1.1.7       | 0.1.13 | 2.6.19        |
| >1 tab at a time         | ✅           | ✅✅                  | ✅✅          | ✅✅     | ✅✅            |
| re-read changed file     | ?           | ?                   | ✅           | ?      | ?             |
| wide tables              | ?           | 🟡 scrolls but pads | ❌ truncates | ✅✅     | ❌ truncates   |
| non-bloated side padding | ?           | ❌❌                  | ❌           | ✅      | ❌             |
| shows images             | ?           | ?                   | ?           | ?      | ?             |
| find in file             | ✅           | ✅                   | ❌           | ✅ ⚙️   | ❌             |
| structure                | ✅           | ✅                   | ❌           | ✅ ⚙️   | ❌             |
| internal links           | ?           | ?                   | ?           | ✅ ⚙️   | ?             |
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

Zaaack multi-file editor behavior is singleton by default. Root cause in `out/extension.js`: `EditorPanel.currentPanel` is treated as the only instance and prior panel is disposed when opening a different file.

Working fix: patch `~/.vscode/extensions/zaaack.markdown-editor-0.1.13/out/extension.js` to maintain a per-file map (`EditorPanel.panelsByPath`) keyed by `uri.fsPath`, reveal existing panel for the same file, and dispose only that file's panel. This allows two different markdown files to stay open in Zaaack at the same time.

Concrete patch shape in `EditorPanel`:

```js
static panelsByPath = new Map();

static async createOrShow(context, uri) {
  const fsPath = uri?.fsPath || vscode.window.activeTextEditor?.document.uri.fsPath;
  const existingPanel = fsPath && EditorPanel.panelsByPath.get(fsPath);
  if (existingPanel) {
    existingPanel._panel.reveal(column);
    return;
  }

  // create panel as before
  const editorPanel = new EditorPanel(context, panel, extensionUri, doc, uri);
  EditorPanel.panelsByPath.set(editorPanel._fsPath, editorPanel);
}

dispose() {
  EditorPanel.panelsByPath.delete(this._fsPath);
  this._panel.dispose();
  ...
}
```

Do not dispose some other file's panel inside `createOrShow`; that singleton teardown is the behavior that forces tab reuse.

Important: preview settings (`workbench.editor.enablePreview*`, MPE `previewMode`) do not solve this by themselves because they control preview reuse, not Zaaack editor panel lifecycle.

Patch caveat: extension updates overwrite patched files; reapply after each Zaaack update.

### Zaaack Find / Outline / Anchor Nav (patched)

The ⚙️ rows in the comparison table — find in file, structure, internal links — are added by `~/bin/patches/patch-zaaack.py` (canonical, lives in `~/bin/` repo and syncs across laptops via git). It patches `main.js` in **both** `~/.vscode/extensions/zaaack.markdown-editor-<version>/media/dist/` and `~/.cursor/extensions/zaaack.markdown-editor-<version>/media/dist/` (each IDE has its own extensions dir). **Pinned to Zaaack 0.1.13 + vditor 3.8.4** (the bundled lib version visible in `main.js`'s license footer). The script globs all matching versioned dirs so a Zaaack version bump does not require editing the script.

**Why patch instead of switching editors.** Every webview-based WYSIWYG competitor (typedown, IDEA shuzijun, Mark Sharp, Unotes, vscode-markdown-wysiwyg, Teddy Editor) shares the same Cmd+F gap — VS Code's find UI doesn't reach into webview content, and vditor doesn't expose a public search API. The only extension with native find is `remcohaszing.markdown-decorations`, but it's decoration-only and loses the rich WYSIWYG rendering that makes zaaack the best choice. So patching zaaack beats every alternative on the market as of 2026.05.

**The four patch sites in `main.js`** — all are uniquely addressable single-line minified strings:

1. **Outline view** — enable vditor's built-in outline panel:
  - Anchor: `toolbarConfig:{pin:!0},`
  - Insert after: `outline:{enable:!0,position:"left"},`
  - Why this works: vditor 3.8.4 has full outline support built in (line 229 of `main.js`: `outline:{enable:!1` is the default). The user-options spread (`...i`) follows our insertion, so saved preferences can still override.
2. **after()-hook bridge** — call our enhancer once vditor finishes initializing:
  - Anchor: `after(){V_(),Y_(),sB(),K_()}`
  - Replace with: `after(){V_(),Y_(),sB(),K_(),window.__zaaackEnhance&&window.__zaaackEnhance()}`
  - Why this works: `after()` fires after vditor mounts the DOM — `window.vditor` is live and the editor `<div id="app">` is populated.
3. **Enhancer definition** — append `window.__zaaackEnhance` body just before the closing IIFE:
  - Anchor: `vscode.postMessage({command:"ready"});})();`
  - Insert before `})();`: the enhancer JS starting with marker `/*__zaaackEnhance__*/` (used as the idempotency check).
  - Marker presence detection lets the script re-run safely without double-patching.
4. **vscode.postMessage wrap** — drop intra-doc anchor `open-link` messages so VS Code does not try to open them as files:
  - Anchor: `window.vscode=window.acquireVsCodeApi&&window.acquireVsCodeApi();window.global=window;`
  - Insert between the two assignments: a wrapper that intercepts `vscode.postMessage({command:"open-link", href})` and, when the href is non-http and contains `#`, scrolls the matching heading via `window.__zaaackGotoAnchor(frag)` instead of forwarding the message.
  - Marker `/*__zk_postwrap__*/` for idempotency.
  - **Belt-and-suspenders, not the primary chokepoint.** In practice the capture-phase click handler in patch site #3 stops the click before vditor ever calls `window.open` / `postMessage`, so this wrap rarely fires. It exists as a fallback for any code path that bypasses the click listener (e.g. programmatic `vditor.api` calls, or a future vditor version that posts directly).

**Enhancer responsibilities** (defined in the appended JS):

- **Anchor link nav.** Two layers, defense in depth:
  - *Primary*: a capturing `click` listener on `window`, `document`, and `documentElement`. Capture phase is critical so we fire **before** vditor's bubble-phase click handler on the editor element (at `main.js` byte ~388578: `var k=Object(H.d)(m.target,"data-type","a"); ...; window.open(k.querySelector(":scope > .vditor-ir__marker--link").textContent)`). The handler matches both `closest('a')` (preview-mode anchors) and `closest('[data-type="a"]')` (vditor's IR-mode link wrapper, which renders `[txt](url)` as `<span data-type="a"><span class="vditor-ir__marker--bracket">[</span><span class="vditor-ir__link">txt</span>...<span class="vditor-ir__marker--link">url</span>...</span>` — i.e. clicking the visible "txt" hits a SPAN, not an A, so a vanilla `closest('a')` walk returns null). For IR-mode hits the URL comes from `markerLink.textContent.trim()`. On any non-http URL: `e.preventDefault() + e.stopImmediatePropagation() + e.stopPropagation()`, then call `__zaaackGotoAnchor(frag)`.
  - *Secondary*: the postMessage wrap (patch site #4). Belt-and-suspenders for any path that bypasses the click listener.
  - `__zaaackGotoAnchor(frag)` resolves headings inside `.vditor-ir__content` / `.vditor-ir` / `.vditor-reset` / `#app` (first that exists). Lookup order: (a) `ed.querySelector('[id="' + CSS.escape(frag) + '"]')` (works when the markdown explicitly assigns ids), else (b) slug-match every `h1..h6`. The slug pipeline must use a `headingText()` walker that **skips child elements with class containing `vditor-ir__marker`** — vditor IR mode renders `## History` as `<h2><span class="vditor-ir__marker--heading">## </span>History</h2>`, so the naive `h.textContent` is `"## History"` and would slugify to `"-history"` (the `#` chars are stripped, replacing leading whitespace with `-`), which never matches the `#history` fragment. With marker spans excluded, the visible text is just `"History"` → slug `"history"` → match. The `slugify()` itself also strips leading `[#*\-_\s]+` as a second-line defense. On hit: `t.scrollIntoView({behavior:'smooth', block:'start'})`.
- **Find-in-page (⌘F).** Capturing `keydown` on `document` matches `(metaKey||ctrlKey) && key==='f'/'F'`. Opens a fixed-position overlay (`#__zk-bar`) at top-right. Search algorithm:
  - Build a `TreeWalker` over `#app` `SHOW_TEXT`. Reject nodes inside `#__zk-bar` (own UI), `vditor-toolbar`, `vditor-outline`, `vditor-hint`, `vditor-panel` so toolbar tooltips and the find overlay itself don't pollute results.
  - For each accepted text node, run `new RegExp(escapedQuery, 'gi')` and replace matches in-place by splitting the node into a `DocumentFragment` of plain text + `<span class="__zk-hit">match</span>`.
  - Track all hit spans in a `hits[]` array. Current hit gets `background:#ff9800`, others `background:#ffd54f`, both `color:#000`. `scrollIntoView({behavior:'smooth', block:'center'})` on selection.
  - Clearing replaces every span back with a text node, then calls `parent.normalize()` on every parent that lost a span — **critical**: without normalization, sibling text nodes left behind by `replaceChild` stay fragmented across span boundaries, so the next regex run can't find matches that span the boundary (e.g. typing "p" then "i": "Hello pillow" becomes `["Hello ","p","illow"]` after clearing the first hit, and `re.exec("p")`/`re.exec("illow")` separately never match `"pi"`). Bug symptom: 1-char queries highlight, 2+ char queries return 0/0. Fix: track unique parents in a `Set`, run `.normalize()` on each, then re-query.
  - Bindings: `⌘F` open, type to live-search (120 ms debounce), `Enter` / `Shift+Enter` next/prev, `Esc` close. Buttons in the bar do the same.
  - Styling uses VS Code CSS vars (`--vscode-editorWidget-background`, `--vscode-input-foreground`, `--vscode-widget-border`, etc.) so the bar matches the active theme.
- **Idempotency guard:** sets `ed.__zaaackEnhanced = true` on the `#app` element so re-firing of `after()` (theme switch triggers a full vditor re-init via `extension.js`'s `onDidChangeActiveColorTheme`, which destroys+recreates vditor — the new `#app` is a fresh element so the guard doesn't block legitimate re-attaches).

**CSP note.** The webview HTML in `extension.js`'s `_getHtmlForWebview()` sets no `Content-Security-Policy` meta tag, so inline scripts in `main.js` execute freely. If a future Zaaack version adds CSP, the enhancer needs to move to a separate file registered via `webview.asWebviewUri()`.

**Reapply procedure** (after Zaaack extension update, OS migration, or fresh checkout):

1. Confirm installed version(s): `ls ~/.vscode/extensions/ ~/.cursor/extensions/ 2>/dev/null | grep zaaack`. The script auto-globs every matching dir under both IDEs.
2. `python3 ~/bin/patches/patch-zaaack.py` — for each target dir, prints `[1/4]` … `[4/4]` and `done`. Re-running on already-patched files is a no-op (each patch site has its own marker / `XXX_NEW in src` short-circuit).
3. Sanity check: `node -c ~/.vscode/extensions/zaaack.markdown-editor-*/media/dist/main.js` should print no errors.
4. Reload VS Code / Cursor window (`Developer: Reload Window`) for each affected window.
5. Open a markdown file with `^⌥⌘M` and verify: outline panel appears on the left, `[link](#some-heading)` jumps in-place (no new tab opens), `⌘F` opens the find bar with multi-char search working.

**Recreating the patch from scratch** (if `~/bin/patches/patch-zaaack.py` is ever lost): use the four anchor strings + the enhancer responsibilities described above. The complete enhancer is ~150 lines of plain ES5 — every behavior listed above is sufficient to rewrite it. Four Python `assert src.count(ANCHOR) == 1` checks plus marker-comment idempotency = the pattern.

**Fallbacks if the patch ever breaks:**

1. **Switch to source markdown view**: `^⌥⌘M` toggles back to the plain markdown source editor where `⌘F` works natively.
2. **Use Markdown Preview Enhanced**: `⇧⌘V` opens a preview tab whose webview supports browser search.
3. **Restore from backup**: every run leaves `main.js.bak.<unix-ts>` next to the patched file.

Cursor parity status:

- Applied matching Cursor user settings in `~/Library/Application Support/Cursor/User/settings.json`:
  - `workbench.editor.enablePreview=false`
  - `workbench.editor.enablePreviewFromQuickOpen=false`
  - `markdown-preview-enhanced.previewMode="Multiple Previews"`
  - `markdown-preview-enhanced.previewColorScheme="systemColorScheme"`
  - `markdown.preview.fontSize=11`, `markdown.preview.lineHeight=1.2`
  - `typedown.editor.fontFamily` / `typedown.editor.fontSize`
  - `markdown-editor.customCss` override for proportional Zaaack editing font
- Applied matching Cursor keybindings in `~/Library/Application Support/Cursor/User/keybindings.json`:
  - `⇧⌘V -> workbench.action.markdown.openPreview` (built-in; preference over MPE in Cursor)
  - typedown / zaaack WYSIWYG shortcut swap parity with VS Code
- `patch-zaaack.py` now globs both `~/.vscode/extensions/` and `~/.cursor/extensions/` so a single run patches the same `main.js` in both IDEs. The `out/extension.js` multi-panel patch (singleton-to-`panelsByPath`-Map) is also expected in Cursor but is applied separately by hand (see *Zaaack Markdown Editor Patches* below).

### Markdown Preview Theme (auto-switch)

If your Markdown preview (for example, Markdown Preview Enhanced) does not switch between light/dark automatically when VS Code or your OS changes theme, add this to your user `settings.json`:

```json
"markdown-preview-enhanced.previewColorScheme": "systemColorScheme"
```

This makes the preview follow the active VS Code editor theme (and thus `window.autoDetectColorScheme`). If you prefer the preview to follow the OS system color scheme directly, use `"systemColorScheme"` instead of `"editorColorScheme"`.

### Cmd+Shift+V → Markdown Preview

**VS Code:** `keybindings.json` unbinds `⇧⌘V` from the built-in and rebinds it to `markdown-preview-enhanced.openPreview` — MPE handles intra-doc anchor links correctly where the built-in sometimes breaks them.

**Cursor:** `⇧⌘V` uses the built-in `workbench.action.markdown.openPreview` (preference). MPE's default binding is unbound via `-markdown-preview-enhanced.openPreview` in Cursor's `keybindings.json`.

If rendered markdown in Zaaack still appears oversized after settings changes, patch `~/.vscode/extensions/zaaack.markdown-editor-0.1.13/out/extension.js` theme overrides from `font-size: 13px;` to `font-size: 11px !important;` and add matching `11px !important` for `.vditor-ir pre.vditor-reset` and `.vditor-sv`.

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

### Wibey Extension Patches

#### New Conversation Bug Fix (v1.0.10)

**Bug:** Clicking "+" (new conversation button) shows the old/most-recent conversation instead of opening a blank chat.

**Root cause:** The `newParallelSession` webview handler — which replaced the old `newSession` flow in the parallel-session (MSM) architecture — does not call `clearMessages()`. So the previous conversation stays visible while the async `createParallelSession` round-trip runs. When that round-trip fails (e.g. `MultiSessionManager` not yet injected, or `buildSessionServices()` throws), `parallelSessionSwitched` never arrives and the old conversation is shown permanently.

**Files patched:**

1. `~/.vscode/extensions/wibey.wibey-vscode-extension-1.0.10/out/webview/webview.js` (minified) — add `clearMessages` to `newParallelSession` handler:

```python
# Run from shell:
python3 - <<'EOF'
path = '$HOME/.vscode/extensions/wibey.wibey-vscode-extension-1.0.10/out/webview/webview.js'
import os; path = os.path.expandvars(path)
c = open(path).read()
old = 'case"newParallelSession":c.showChat();{const e=bi.getState();'
new = 'case"newParallelSession":c.showChat(),o.clearMessages(),o.clearTodos(),h.clearQueue();{const e=bi.getState();'
assert c.count(old) == 1
open(path, 'w').write(c.replace(old, new, 1))
print("webview.js patched")
EOF
```

1. `~/.vscode/extensions/wibey.wibey-vscode-extension-1.0.10/out/handlers/MultiSessionHandler.js` (readable) — two changes:

**a.** In `handle()`, replace the silent return when MSM is null:

```js
// BEFORE (lines 46-49):
if (!this.multiSessionManager) {
    logger_js_1.logger.warn('[MultiSessionHandler] MultiSessionManager not initialized');
    return;
}

// AFTER:
if (!this.multiSessionManager) {
    logger_js_1.logger.warn('[MultiSessionHandler] MultiSessionManager not initialized');
    if (message.type === 'createParallelSession') {
        // Fall back to legacy new-session flow so the webview always lands on a blank chat.
        this.context.webviewController.postMessage({ type: 'newSession' });
    }
    return;
}
```

**b.** In `handleCreateSession()` catch, replace the non-limit `streamError` path:

```js
// BEFORE:
else {
    this.context.webviewController.postMessage({
        type: 'streamError',
        error: `Failed to create new session: ${errorMessage}`,
    });
}

// AFTER:
else {
    // Session creation failed — fall back to legacy new-session flow so the
    // webview shows a blank chat rather than staying on the old conversation.
    logger_js_1.logger.warn('[MultiSessionHandler] Falling back to legacy new-session after createSession failure');
    this.context.webviewController.postMessage({ type: 'newSession' });
}
```

After patching, run `Developer: Reload Window` in VS Code. Patches are overwritten on Wibey extension update — reapply after each update (adapt paths for new version).

---

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

`**--no-open` flag** — `wibey-usage dash --no-open` generates the HTML without opening a browser tab. Supported in both installed (`~/.wibey/usage/wibey-usage`) and skill source (`~/.wibey/skills/usage-dashboard/scripts/wibey-usage`).

**If today's data is missing:** the HTML is stale — regenerate manually: `~/.wibey/usage/wibey-usage dash`

Files that implement auto-regen (keep in sync):

- `~/.claude/hooks/session-end-usage.py` (active hook)
- `~/.wibey/skills/usage-dashboard/scripts/session-end-usage.py` (skill source)

## History

History of tool use practices, not of this doc.

- 2026.03.26 Thu: Opus gets stuck in IDEA last few days, switching to Sonnet
- 2026.05.09 Sat: Fixed the last three Zaaack gaps — Cmd+F find-in-page, outline view, and intra-doc anchor link nav — via `~/bin/patches/patch-zaaack.py` (4 idempotent patch sites in `media/dist/main.js`). Zaaack jumped from `🟡` to `✅✅` parity with IDEA's md preview, and (since the patch globs both `~/.vscode/extensions/` and `~/.cursor/extensions/`) Cursor now matches VS Code on markdown editing too. Upstream is MIT (`github.com/zaaack/vscode-markdown-editor`) but with low maintainer activity (108 open issues, 5+ stale PRs); the anchor-link-opens-directory bug appears unreported, so worth filing one issue. Find-in-page (#153) and outline (#24, #155) are already requested upstream.

