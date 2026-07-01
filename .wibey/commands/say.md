---
description: Display a banner with custom text
allowed-tools: Bash
---

Interpolate values into the template block below and render it as Markdown exactly as shown.

**Rules:**

- Output exactly the interpolated template block, with the same number of lines and ordering.
- Do not add commentary, bullets, code fences, or extra whitespace.
- `yyyy.mm.dd.Dow.hhmm` — run `date "+%Y.%m.%d.%a.%H%M"` and substitute the output.
- `repo` — the basename of the current git repo (e.g. `git rev-parse --show-toplevel | xargs basename`); use the workspace folder name if not in a git repo.
- `branchname` — the current git branch (e.g. `git rev-parse --abbrev-ref HEAD`); omit if not in a git repo.
- Replace `message` with the verbatim argument text provided by the user.

**Template:**

```
---
# yyyy.mm.dd.Dow.hhmm repo:branchname
# message
---
```
