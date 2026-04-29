---
description: Display a conversation banner
allowed-tools: Bash
---

Interpolate values into the template block below and render it as Markdown exactly as shown.

**Rules:**

- Output exactly the interpolated template block, with the same number of lines and ordering.
- Do not add commentary, bullets, code fences, or extra whitespace.
- `yyyy.mm.dd.Dow.hhmm` — run `date "+%Y.%m.%d.%a.%H%M"` and substitute the output.
- `repo` — the basename of the current git repo (e.g. `git rev-parse --show-toplevel | xargs basename`); use the workspace folder name if not in a git repo.
- `branchname` — the current git branch (e.g. `git rev-parse --abbrev-ref HEAD`); omit if not in a git repo.
- **If arguments were provided:** replace lines 2 and 3 of the template with a single line: `# ` followed by the verbatim argument text. Output is 4 lines total (the two `---` fences, the datetime line, and the one arg line).
- **If no arguments:** for the conversation summary line, use the IDE conversation title when available; otherwise generate a very close one-line summary from the current request. For the last-3-turns line, never mention invoking, running, rendering, or displaying `/convo` or the conversation banner itself.

**Template:**

```
---
# yyyy.mm.dd.Dow.hhmm repo:branchname
# one-line summary of entire conversation (prefer IDE title text)
# one-line description of last 3 turns, excluding any mention of /convo or banner rendering
---
```
