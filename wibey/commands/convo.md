---
description: Display a conversation banner
allowed-tools: Bash
---

Interpolate values into the template block below and render it as Markdown exactly as shown.

**Rules:**

- Output exactly the interpolated template block, with the same number of lines and ordering.
- Do not add commentary, bullets, code fences, or extra whitespace.
- For the conversation summary line, use the IDE conversation title when available; otherwise generate a very close one-line summary from the current request.

**Template:**

```
---
# yyyy.mm.dd.Dow.hhmm repo:branchname
# one-line summary of entire conversation (prefer IDE title text)
# one-line description of last 3 turns
---
```
