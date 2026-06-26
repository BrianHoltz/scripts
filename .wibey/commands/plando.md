---
name: plando
description: Structured plan-and-execute workflow with aidocs task record and audit trail.
---

> [!NOTE]
> **Mirror-safe command.** This file contains no Walmart-proprietary content and is
> designed to be manually mirrored to personal laptops. The canonical copy lives in
> [`relationship-shared/.wibey/commands/`](https://gecgithub01.walmart.com/CatalogRelationships/relationship-shared).
> **If you are reading this outside of Walmart GHE, do not edit it here** — make
> changes in relationship-shared and re-sync.

# Plan and Do

This command does NOT use plan mode. You stay in your current permission mode and both plan and execute in a single session. The goal is to get the benefits of structured planning without the mode-switch overhead.

Make and execute a detailed systematic plan for the following request.

- **Orient.** If `AGENTS.md` exists, read it and consult its "What to Read for a Given Task" table for any docs relevant to this request. Read the repo-specific doc in `shared/docs/repos/` if one exists.
- **Clarify.** Ask any clarifying questions before you start.
- **Record.** If shared/aidocs/ folder (or similar untracked task-record location) exists in the workspace, find or create a task record for this work. Keep it up-to-date with your plan, status, and datetime-stamped work log. Footnote to Evidence urls for any empirical claims so they can be checked. The point of this trail is future reference — agents cannot search previous conversations, so aidocs is how institutional memory survives across sessions. **After creating or updating an aidocs file, always open it in VS Code** using `code <filepath>`.
- **Plan.** Break the work into numbered phases with clear deliverables.
- **Execute.** Be creative in using the deep knowledge and skills in this repo and any linked shared/ repo. If you are Wibey, also leverage your DX/MCP powers and run the /safe-browse command if you think you might need a browser. Think critically and independently about the information you encounter, and question your assumptions.
