---
name: clipboard-read
description: |
  Read the macOS clipboard and display its full contents — images, rich text with hyperlinks, or plain text. Use whenever the user says:
  - "see clipboard" / "check clipboard" / "read clipboard" / "show clipboard"
  - "what's on my clipboard" / "paste that" / "what did I copy"
  - "read my clipboard" / "show me what I copied"
  - "clipboard-read then..." / "do a clipboard-read"
  - "extract the URLs from my clipboard"
  Automatically handles images (screenshots, photos), rich text with hyperlinks (Slack, Confluence, Jira, email), and plain text. Never requires the user to specify which format.
  Works on macOS only.
metadata:
  author: b0h0166
sample-prompts:
  - "see clipboard"
  - "check clipboard"
  - "what's on my clipboard"
  - "read my clipboard"
  - "show me what I copied"
  - "show me what I copied with links"
  - "Extract the URLs from my clipboard"
  - "do a clipboard-read"
  - "clipboard-read then..."
---

> [!NOTE]
> **Mirror-safe skill.** This file contains no Walmart-proprietary content and is
> designed to be manually mirrored to personal laptops. The canonical copy lives in
> [`relationship-shared/.wibey/skills/clipboard-read/`](https://gecgithub01.walmart.com/CatalogRelationships/relationship-shared).
> **If you are reading this outside of Walmart GHE, do not edit it here** — make
> changes in relationship-shared and re-sync.

# clipboard-read — Read Clipboard (Images + Rich Text + Links)

Reads the macOS system clipboard in full fidelity: images are displayed visually, rich text preserves hyperlinks, plain text falls back cleanly. **Never requires the user to specify the format** — always runs the full detection sequence below.

## ❗ CRITICAL Rules

- **NEVER use `pbpaste` first.** It strips all hyperlinks and cannot see images. Always run the full detection sequence.
- **ALWAYS check for both image AND HTML** — a browser-copied image can have both a PNG and an HTML representation simultaneously.
- **NEVER ask the user which format their clipboard is in.** Run Step 1 and it tells you.

## Workflow

### Step 1: Detect clipboard types

```bash
osascript -e 'clipboard info' 2>/dev/null
```

This lists all available representations (e.g. `«class PNGf»`, `«class HTML»`, `TIFF picture`, `JPEG picture`). Use the output to decide which steps to run.

### Step 2: If image present (`«class PNGf»`, `JPEG picture`, `TIFF picture`, `GIF picture`, `«class AVIF»`)

Save the PNG representation to a temp file and display it using the Read tool:

```bash
osascript -e 'set imgData to (the clipboard as «class PNGf»)
set fileRef to open for access POSIX file "/tmp/clipboard_img.png" with write permission
set eof of fileRef to 0
write imgData to fileRef
close access fileRef' && echo "saved"
```

Then call `Read("/tmp/clipboard_img.png")` to display the image inline. Always prefer PNG even if other image formats are present.

### Step 3: If HTML present (`«class HTML»`)

Extract HTML and parse links/formatting:

```bash
osascript -e 'the clipboard as «class HTML»' 2>/dev/null | python3 -c "
import sys, re
data = sys.stdin.buffer.read().decode('utf-8', errors='replace')
m = re.search(r'HTML([0-9A-Fa-f]+)', data)
if m:
    print(bytes.fromhex(m.group(1)).decode('utf-8', errors='replace'))
else:
    print('NO_HTML_CLIPBOARD')
"
```

Parse the HTML inline and convert to markdown:
- Hyperlinks: `<a href="URL">text</a>` → `[text](URL)`
- Message text, sender, timestamp if it looks like a Slack/Teams message
- Bold, italic, lists, tables as markdown

If both image and HTML are present (common for browser-copied images), show the image first then the HTML text/links below it.

### Step 4: If neither image nor HTML — fall back to plain text

```bash
pbpaste
```

Only reach this step if Steps 2 and 3 both produced nothing.

## Decision Matrix

| `clipboard info` shows | Action |
|---|---|
| `«class PNGf»` or image type | Step 2 (save + display image) |
| `«class HTML»` | Step 3 (extract HTML, parse links) |
| Both image + HTML | Step 2 then Step 3 |
| Neither | Step 4 (pbpaste) |

## After Reading

- If the user said "see clipboard then do X": extract the relevant data (URLs, text, image content) and immediately proceed to task X without waiting for confirmation.
- Large HTML (over ~500 lines): summarize rather than dump raw.
- The HTML may contain inline styles from the source app — ignore styling, preserve only content and links.

## Gotchas

- macOS only (uses `osascript`)
- The `set eof of fileRef to 0` line in Step 2 truncates any existing file before writing — required to avoid corrupt PNG if `/tmp/clipboard_img.png` already exists from a previous run.
- `osascript` returns hex-encoded data for binary types; the python3 snippet decodes it.
- The old perl-based extraction also works but python3 is cleaner and more universally available.
