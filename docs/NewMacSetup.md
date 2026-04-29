# New Personal MacBook Setup

*Generated 2026.04.28 from work MacBook inventory. Filtered: Walmart-only tools excluded.*

## Manual: Bootstrap

```sh
# Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# Post-install: add eval line to ~/.zprofile per brew output

# SSH key + GitHub auth (auth needed before ~/bin/ clone and for Copilot sign-in)
ssh-keygen -t ed25519 -C "brianholtz1965@gmail.com"
# Add ~/.ssh/id_ed25519.pub to github.com → Settings → SSH keys
brew install gh
gh auth login

# ~/bin/ shell integrations
git clone git@github.com:BrianHoltz/scripts.git ~/bin
ln -sf ~/bin/docs/AgentRules.md ~/.claude/CLAUDE.md
ln -sf ~/bin/shellrc/zprofile ~/.zprofile
ln -sf ~/bin/shellrc/zshrc ~/.zshrc
ln -sf ~/bin/shellrc/bash_profile ~/.bash_profile
ln -sf ~/bin/shellrc/bashrc ~/.bashrc
ln -sf ~/bin/shellrc/shellrc.common ~/.shellrc.common

# VS Code + Copilot
brew install --cask visual-studio-code
code --install-extension github.copilot
code --install-extension github.copilot-chat
```

Open `code ~/bin/docs/NewMacSetup.md` — VS Code picks up the `gh` session for Copilot sign-in automatically.

## Copilot: Core Apps

All install correctly via brew — no web downloads needed.

```sh
brew install --cask \
  google-chrome \
  firefox \
  cursor \
  jetbrains-toolbox \
  stats \
  tableplus \
  github \
  postman \
  slack \
  zoom \
  google-drive
```

- After JetBrains Toolbox: install IntelliJ IDEA Community or Ultimate from Toolbox UI
- `stats` — menu bar CPU/RAM/disk/network; auto-launches at login
- Google Drive — launches at login automatically after install

## Copilot: Additional Apps

```sh
brew install --cask claude
brew install --cask discord
brew install --cask signal
brew install --cask vlc
brew install --cask plex
brew install --cask libreoffice
brew install --cask kiwix
brew install --cask simple-comic
brew install --cask google-earth-pro
brew install --cask emacs-app
brew install --cask vysor
```

## Manual: Additional Apps

- Kindle — App Store
- Family Tree Maker — https://mackiev.com/ftm/
- OBSBOT Center — https://www.obsbot.com/download
- YiHomeMacInt — App Store
- Reolink for Mac — https://reolink.com/software-and-manual/
- World of Tanks Blitz — App Store

## Copilot: Shell / Git Config

```sh
git config --global user.name "Brian Holtz"
git config --global user.email "brianholtz1965@gmail.com"
git config --global core.editor "code --wait"
git config --global pull.rebase true
```

## Copilot: Core CLI

```sh
brew install \
  git-filter-repo \
  jq \
  node \
  python@3.13 \
  parallel \
  netcat \
  pstree \
  sqlite \
  rdiff-backup \
  d2
```

(`gh` installed in Bootstrap.)

- `d2` — text-to-diagram CLI (used for architecture docs)
- `rdiff-backup` — incremental backup utility
- `parallel` — GNU parallel (used in scripts)

```sh
# ~/bin/ script deps (agent_browse requires these)
pip3 install playwright requests
playwright install chromium
```

## Copilot: VS Code Extensions

```sh
# Core workflow (Copilot already installed)
code --install-extension eamodio.gitlens
code --install-extension shd101wyy.markdown-preview-enhanced
code --install-extension tarikkavaz.typedown-markdown-editor
code --install-extension zaaack.markdown-editor
code --install-extension bierner.markdown-mermaid
code --install-extension darkriszty.markdown-table-prettify
code --install-extension davidanson.vscode-markdownlint

# Dev tools
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-python.debugpy
code --install-extension hediet.vscode-drawio
code --install-extension mechatroner.rainbow-csv
code --install-extension techer.open-in-browser
code --install-extension tomoki1207.pdf
code --install-extension yzane.markdown-pdf
code --install-extension johnpapa.vscode-peacock
```

Install same extensions in Cursor via `cursor --install-extension <id>`.

## Copilot: VS Code / Cursor Settings

Add to `~/Library/Application Support/Code/User/settings.json`
(and `~/Library/Application Support/Cursor/User/settings.json`):

```json
{
  "workbench.editor.enablePreview": false,
  "workbench.editor.enablePreviewFromQuickOpen": false,
  "markdown.preview.fontSize": 13,
  "markdown.preview.lineHeight": 1.2,
  "markdown-preview-enhanced.previewMode": "Multiple Previews",
  "markdown-preview-enhanced.previewColorScheme": "systemColorScheme",
  "typedown.editor.fontFamily": "-apple-system, BlinkMacSystemFont, 'Segoe WPC', 'Segoe UI', system-ui, 'Ubuntu', 'Droid Sans', sans-serif",
  "typedown.editor.fontSize": 13,
  "markdown-editor.customCss": ".vditor .vditor-reset, .vditor-ir pre.vditor-reset, .vditor-sv { font-family: -apple-system, BlinkMacSystemFont, 'Segoe WPC', 'Segoe UI', system-ui, 'Ubuntu', 'Droid Sans', sans-serif !important; font-size: 13px !important; } .vscode-light .vditor--dark .vditor-reset { color: #111111 !important; background: #ffffff !important; } .vscode-light .vditor--dark .vditor-ir pre { color: #111111 !important; }",
  "chat.tools.global.autoApprove": true,
  "chat.tools.urls.autoApprove": { "*": true },
  "chat.agent.maxRequests": 250,
  "git.confirmSync": false,
  "explorer.confirmDelete": false,
  "security.workspace.trust.untrustedFiles": "open"
}
```

**Cursor proxy**: no proxy on personal — omit/remove `http.proxy` and `http.proxySupport` from Cursor settings. See `Tools.md` § Cursor § Proxy.

Add to `~/Library/Application Support/Code/User/keybindings.json`
(and `~/Library/Application Support/Cursor/User/keybindings.json`):

```json
[
  { "key": "shift+cmd+v", "command": "-workbench.action.markdown.openPreview" },
  { "key": "shift+cmd+v", "command": "markdown-preview-enhanced.openPreviewToTheSide" },
  { "key": "ctrl+alt+cmd+m", "command": "-typedown.openWysiwygEditor", "when": "!typedown.editorIsActive" },
  { "key": "alt+shift+cmd+m", "command": "typedown.openWysiwygEditor", "when": "!typedown.editorIsActive" },
  { "key": "ctrl+alt+cmd+m", "command": "-typedown.openDefaultEditor", "when": "typedown.editorIsActive" },
  { "key": "alt+shift+cmd+m", "command": "typedown.openDefaultEditor", "when": "typedown.editorIsActive" },
  { "key": "alt+shift+cmd+m", "command": "-markdown-editor.openEditor", "when": "editorTextFocus && editorLangId == markdown" },
  { "key": "ctrl+alt+cmd+m", "command": "markdown-editor.openEditor", "when": "editorTextFocus && editorLangId == markdown" }
]
```

Result: `⌥⇧⌘M` opens TypeDown, `^⌥⌘M` opens Zaaack, `⇧⌘V` opens MPE side preview.

## Copilot: Extension Patches

These patches survive extension installs but are overwritten on extension *update* — reapply after each update.

**TypeDown** (`tarikkavaz.typedown-markdown-editor`): fix line-height, table padding, focus/cursor warp bug

- Patch `~/.vscode/extensions/tarikkavaz.typedown-markdown-editor-*/dist/extension.js`
- Patch `~/.cursor/extensions/tarikkavaz.typedown-markdown-editor-*/dist/extension.js` (same patch, both IDEs)
- Full patch details: `Tools.md` § TypeDown Patches

**Zaaack** (`zaaack.markdown-editor`): fix dark-mode colors, multi-panel support, font (VS Code only; not yet installed in Cursor)

- Patch `~/.vscode/extensions/zaaack.markdown-editor-*/media/dist/main.css`
- Patch `~/.vscode/extensions/zaaack.markdown-editor-*/out/extension.js`
- Full patch details: `Tools.md` § Zaaack Markdown Editor Patches

After patching either extension: `⇧⌘P` → Developer: Reload Window.

## Copilot: IntelliJ IDEA Settings

Paths below use `<version>` for the IDEA version directory (e.g. `IntelliJIdea2025.3`).

**Keymaps** — `~/Library/Application Support/JetBrains/<version>/keymaps/macOS copy.xml`:

```xml
<keymap version="1" name="macOS copy" parent="Mac OS X 10.5+">
  <action id="ZoomInIdeAction">
    <keyboard-shortcut first-keystroke="meta equals" />
    <keyboard-shortcut first-keystroke="meta add" />
  </action>
  <action id="ZoomOutIdeAction">
    <keyboard-shortcut first-keystroke="meta minus" />
    <keyboard-shortcut first-keystroke="meta subtract" />
  </action>
  <action id="GotoFile">
    <keyboard-shortcut first-keystroke="meta p" />
  </action>
</keymap>
```

**Markdown preview font** — `~/Library/Application Support/JetBrains/<version>/options/markdown.xml`:

```xml
<application>
  <component name="MarkdownSettings">
    <option name="fontSize" value="15" />
  </component>
</application>
```

**Disable sensitive-file dialog** — `~/Library/Application Support/JetBrains/<version>/early-access-registry.txt`:

```
idea.readonly.fragments.notification.enabled
false
```

Restart IDEA after adding. **Shuzijun Markdown Editor** (install plugin first, then patch):

- JAR: `~/Library/Application Support/JetBrains/<version>/plugins/markdown-editor/lib/markdown-editor-*.jar`
- Extract `vditor/style.css`, add `font-size: 13px !important` to `.vditor .vditor-reset`, `.vditor-sv`, `.vditor-ir`; repack with `jar uf`; restart IDEA
- Full patch details: `Tools.md` § Shuzijun Markdown Editor Patches

## Copilot: Claude Code

```sh
npm install -g @anthropic-ai/claude-code
```

- Personal laptop uses `~/bin/wibey/skills/` — no `shared/` symlink
- Expose skills per workspace via `.wibey/skills/<name>/SKILL.md` symlinks into `~/bin/wibey/skills/`
- Usage dashboard: install via `/install usage-dashboard` in a session; apply UTC timezone patches from `Tools.md` § usage-dashboard

## Copilot: Media & AI

```sh
brew install ffmpeg
brew install openai-whisper   # pulls pytorch, numpy, etc. — takes a while
```

- `ffmpeg` — pulls x264, x265, lame, opus, dav1d, libvpx, svt-av1, sdl2 automatically
- `openai-whisper` — local speech-to-text; also installs pytorch + openblas as deps

## Copilot: Optional

Containers:

```sh
brew install kubernetes-cli
brew install --cask docker
```

Bun:

```sh
brew install oven-sh/bun/bun
```

## Notes

- `brew list` on work Mac = deps-included; only manually install the named formulae above (deps pull automatically)
