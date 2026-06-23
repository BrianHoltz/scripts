---
description: Display a conversation banner
allowed-tools: Bash, mcp__jetbrains-mcp__open_file_in_editor
---

Interpolate values into the template block below and render it as Markdown exactly as shown.

**Rules:**

- Output exactly the interpolated template block. Ordering is fixed; the `# doc:` line is conditional — include it only when a doc is identified (see below), omit it entirely otherwise.
- Do not add commentary, bullets, code fences, or extra whitespace.
- For the conversation summary line, use the IDE conversation title when available; otherwise generate a very close one-line summary from the current request.
- For the last-3-turns line, never mention invoking, running, rendering, or displaying `/convo` or the conversation banner itself.

**Doc detection (run before rendering):**

Identify the primary incident or project doc for this conversation — the one most recently **read or edited** by the agent (file paths matching `incidents/**/*.md` or `projects/**/*.md`). Mentions in `git status` output alone do not qualify; the file must have been opened or written.

If a doc is identified, run this Bash block (substituting the absolute path):

```bash
DOC_PATH="<absolute path>"
DOC_FILE=$(basename "$DOC_PATH")
DOC_CTIME=$(stat -f "%SB" -t "%Y.%m.%d.%H%M" "$DOC_PATH" 2>/dev/null)
# Fall back to mtime if birth time is unavailable (non-APFS or pre-2000)
[[ "${DOC_CTIME%%.*}" -lt 2000 ]] 2>/dev/null && \
  DOC_CTIME=$(stat -f "%Sm" -t "%Y.%m.%d.%H%M" "$DOC_PATH" 2>/dev/null)
DOC_MTIME=$(stat -f "%Sm" -t "%Y.%m.%d.%H%M" "$DOC_PATH" 2>/dev/null)
echo "file=$DOC_FILE ctime=$DOC_CTIME mtime=$DOC_MTIME"
```

Then call `mcp__jetbrains-mcp__open_file_in_editor` with `DOC_PATH` as the `filePath` — skip silently if the tool is unavailable (personal laptop / no IDE connection).

**Template:**

```
---
# yyyy.mm.dd.Dow.hhmm repo:branchname
# one-line summary of entire conversation (prefer IDE title text)
# one-line description of last 3 turns, excluding any mention of /convo or banner rendering
# doc: <filename.md>  created:<yyyy.mm.dd.hhmm>  modified:<yyyy.mm.dd.hhmm>
---
```

Omit the `# doc:` line entirely if no incident or project doc was identified.
