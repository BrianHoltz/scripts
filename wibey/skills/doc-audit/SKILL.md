> **Source:** ~/src/relationship-shared/.wibey/skills/doc-audit/SKILL.md
> **Last synced:** 2026.04.04
> **Sync model:** Manual. After updates at work, copy back to ~/bin/ and commit.

# Doc Audit Skill

Consolidated reference for documentation authoring, project document formatting, and audit standards for the agent-toolkit framework.

## Topics Covered

- **Status / Active Work / Work Log** — conditional temporal views, status excerpts, consistency pipeline
- **Where pending work lives** — two containers (Tasks, Active Work), two flags (TODO, TBD)
- **Task list conventions** — glyph meanings, status rules, date format, task discipline
- **Work Log format** — heading/bullet format, pacing (~30 min entries), status section updates
- **Evidence protocol** — dagger links, entry structure, perishable data dating
- **Temporal writing rules** — timeless perspective, no relative dates, no future prose
- **Content brittleness** — keeping docs in sync with code, avoiding line number references, TOC maintenance
- **Ad hoc documents** — placement in aidocs/, naming convention, when to create them
- **Styling discipline** — footnote glyphs, table cell vocabulary, hyperlink conventions, escaping
- **Doc audit checklist** — status audit, semantic audit, task creep audit
- **DRY principles** — no revision history, no redundancy with git
- **Doc audit dates** — format, when needed, update rules

## Tasks and Logs

### If The Doc Has a Tasks List

A Tasks list is a planning device — it captures what was scoped before work began, not a retroactive record of what happened. In a perfectly Agile project, Tasks are 1:1 with Jira tickets, which are all created before the project starts.

- Rows are added to describe planned work, not to describe completed work
- Completed rows stay (as a high-level status/scope log)
- Rows are rarely removed (only when entire line of work is canceled: 🚫)
- Status column is updated as work progresses

### If The Doc Also Has a Status Section

If the doc has both a Tasks list and a Status section, the Status section should include a verbatim excerpt of the Tasks list:

- **Status rows are verbatim copies of Tasks rows** — never paraphrased or reworded
- **Status excerpt** should include:
  - All started, incomplete tasks (▶️ status)
  - All tasks completed in the last 2 business days (no older completed tasks)
  - Exception: minimum of the last 3 completed tasks (even if older than 2 business days)
  - The next 2 tasks, chosen by judgment/priority
- Update the Status section whenever the excerpted Tasks change (new tasks added, tasks completed, blockers introduced, phase transitions)

### If The Doc Is An Agent-Toolkit Project Plan

Our project docs also include Active Work and Work Logs sections.

**Active Work (The Present)** — mutable working state for in-progress items. Answers: "What are we working on right now?"

- Reflects only ▶️ (in-progress) tasks
- Contains subtasks, blockers, partial results, dependencies
- If work is interrupted, next person/agent picks up here
- Cleared when (sub)tasks complete — concluded items move to Work Log, never duplicated

**Work Log (The Past)** — Work Log is an audit trail of effort — what we spent time on, what the problems were, and how we moved closer to the goal. Git commits describe what changed; the Work Log describes how we got there.

- Records decisions made, discoveries, costs incurred, obstacles overcome
- Provides context for why code looks the way it does
- Built incrementally (one entry every ~30 minutes during active work)
- Different purpose from git revision history (why/how, not what)
- Completed items from Active Work are recorded here, then cleared from Active Work

**Consistency Pipeline** — Tasks → Status → Active Work → Work Log must stay in sync:

- **Tasks ↔ Status**: Status rows are verbatim copies of Tasks rows (never paraphrased)
- **Tasks ↔ Active Work**: Active Work subtasks relate only to ▶️ tasks
- **Active Work ↔ Work Log**: Concluded items are cleared from Active Work (not duplicated)

### Where Pending Work Lives: Two Containers + Two Flags

**Containers (look here for "what's next"):**
- **Tasks** — planned work with defined scope. Search Tasks when deciding what work to do.
- **Active Work** — in-progress subtasks/blockers. Search Active Work when resuming an interrupted session.

**Flags (inline markers for non-blocking items):**
- **TODO** — low-priority improvement that blocks nothing and (often) is blocked by nothing. Use as code/doc comments. If work blocks something, it's a Task, not a TODO.
- **TBD** — placeholder for values waiting to be filled in. Use inline where value belongs.

## Task List Conventions

All task lists follow a consistent format:

### Status Glyphs

- **_(blank)_** = not started
- **▶️** = in progress
- **⏳** = blocked on external (Notes column names the blocker)
- **👀** = under review
- **✅** = completed
- **⏸** = paused/on hold
- **🚫** = won't do

### Format Rules

- **No space between glyph and date**: `✅03.14` not `✅ 03.14`
- **Dates in MM.DD format** (never DD.MM): `03.14` not `14.03` or `Mar 14`
- **Glyph + date appear in Status column**, with detailed explanation in Notes column

### Task Table Columns

Acceptable columns (not all required):

- **Task** — terse, permanent title/description designed not to change
- **LOE** — prior estimated person-days. Only for planning; remove after Jira tickets created. Never log effort after completion.
- **Jira** — optional; terse anchor text linked to ticket
- **Status** — glyph + MM.DD date
- **Notes** — detailed explanation, blockers, rationale

### Task Discipline Rules

- **Never add a task and mark it complete in the same work session.** Work already finished when the task would be written belongs in the Work Log, not the task table.
- **Never backfill completed work into Tasks.** Completed rows stay in the table (useful record), but Tasks is forward-looking only. If work was completed before the task was planned, it belongs in Work Log.
- **Future work appears only in task lists and TODOs.** No "Critical/Important/Urgent" labels — use order. No capitalized exclamations (Bug, Gap, Pending, Next). No ⚠️ in task tables (use it for alarming situations that need footnotes).

## Work Log Format

Work Log headings use day-level dates; entries use per-action timestamps (~30 min apart):

```
### 03.16 Sun Refactored cache layer

- **14:32:** Pulled PR #582, found race condition in auth middleware lock ordering
- **15:02:** Added mutex lock to fix race; unit tests updated and passing
- **15:32:** Ran full test suite; 2 flaky timeouts (unrelated), otherwise green
- **16:01:** Created PR #589 for review; ready for staging tomorrow
```

**Heading format:** `### MM.DD Dow Title of The Day's Work` (prefix with YYYY at year boundaries: `### 2026.03.16 Sun ...`)

**Entry format:** `- **HH:MM:** Entry text` (bold timestamp + colon, then action text)

Aim for one entry every ~30 minutes during active work.

## Status Section Updates

When modifying a file in `projects/` that has a `## Status` section:

1. **Re-read the Status section** after making your changes
2. **Check whether your changes affect the status summary**:
   - New tasks added?
   - Tasks completed?
   - New blockers introduced?
   - Phase transitions?
   - New appendices?
3. **If yes, update Status section** to reflect current state
4. **Never backdate status changes** — reflect what's true now

---

## Evidence Protocol

Every verifiable empirical claim must cite its source.

### Inline Link Convention

Use Unicode dagger † (U+2020) with no space before it:

```
claim text[†](#e-descriptive-slug)
```

Example: "Latency dropped 40% after the cache change[†](#e-latency-drop)."

### Evidence Entry Structure

Place evidence entries in a dedicated `## Evidence` section near the bottom of the document, above Work Log. Each entry is a `###` heading:

```
### Brief description of what is being evidenced

<a id="e-descriptive-slug"></a>

- **Claim**: the specific assertion being backed
- **Source**: URL, file path, git commit SHA, dashboard name, or person name + role
- **Dates**: source vintage (when authored/published) and collection date (ISO YYYY-MM-DD, when retrieved)
- **Quote / data**: exact text excerpt, metric value, or command output
```

Omit any field that genuinely doesn't apply, but include as many as possible.

### Additional Evidence Rules

- **Letter-number prefixes for many items**: For docs with >5 evidence items, use `[†A1](#a1-slug)`, `[†A2](#a2-slug)`, etc.
- **Unsourced claims**: Label "Inference:" or "Unverified:" until evidenced — they are assertions, not findings.
- **Perishable data** (production stats, row counts, latency, costs, queue depths): Add vintage parenthetical linking to evidence entry:

  ```
  claim text[(2025)](#e-slug) for annual figures
  claim text[(2025-03)](#e-slug) for monthly figures
  claim text[(2025-03-14)](#e-slug) for daily figures
  ```

  The granularity matches shelf life: annual for slow data, daily for fast-moving data.
- **Documents as sources**: When citing dated sources (incident, analysis, ADR), put the parenthetical date *after* the verb and link the date to the source:

  ```
  Rohith cataloged ([2025.09](#e-bv-sync-issue)) 5 manifestations
  ```

  Not: `Rohith (Sep 2025) cataloged...`

## Temporal Writing Rules

All prose in tracked docs must read as timeless — durable observations, not corrections of earlier drafts.

### Timeless Perspective

Every sentence should seem as if it were always there. Analytical contrasts are fine ("the PRDs define the problem space more precisely than the engineering pages do"). Self-conscious narrative is not ("the gap may be *smaller than* the pages *let on*").

**Tell**: If a sentence only makes sense to someone who read a previous version of the document, it's narrative, not analysis. Narrative belongs in git commits and work logs.

### No Relative Temporal References in Persistent Files

Never use: "today", "tomorrow", "yesterday", "this morning", "this afternoon", "tonight", "next week"

Instead use absolute dates: "Mar 31" not "today", "Mon Mar 31 afternoon" not "this afternoon"

(Relative references in chat replies are fine — the constraint is for files.)

### No Dates Unless Capturing a Formal Event

`docs/` content should not mention dates except for formal production events (migrations, releases of critical changes/bugfixes). No changelogs or revision dates — git history provides that. Exception: release history for major features or incompatible changes.

### No Future Dates Unless Capturing a Commitment

Future work lives in task rows and TODOs only, never as prose promises.

---

## Content Brittleness

Keep docs maintainable and resilient to code changes.

- **Avoid redundancy with code.** Don't write comments that just repeat what the code says. Use comments for interfaces (e.g. JavaDoc) and non-obvious considerations.
- **Code should be self-documenting** through naming — avoid comments redundant with plain reading.
- **Never reference file line numbers** in enduring docs (exception: Evidence entries anchored to a specific commit SHA).
- **Never use numbered lists** in version-controlled docs — they force cascading renumbering on insert. Use headers or bullets instead.
- **Keep TOC in sync** with actual headings when you update the doc.

---

## Ad Hoc Documents

Short-lived conversation artifacts that don't belong in permanent reference docs.

### Placement

- **With shared/ symlink**: Place in `shared/aidocs/yyyy-mm-dd/` (any repo, same location via symlink)
- **Without shared/ symlink**: Place in `<repo>/aidocs/yyyy-mm-dd/`
- Never create per-repo `aidocs/` folders in team setups; use the shared location

### Naming

Format: `hhmm_CamelCase.md` where `hhmm` is create time, not modification time.

If updating a doc created on an earlier date, move it into the current date folder and use modtime for `hhmm`.

### When to Create

- Use for analysis, investigation notes, or conversation artifacts
- Don't check into VCS
- Only create if the content is substantial (>100 lines) or you're building incrementally
- Avoid creating multiple ad hoc docs at once — combine into a single TOC'd document to prevent WETness
- Never link to ad hoc docs from tracked files

---

## Styling Discipline

Standardized formatting so agents and humans produce visually consistent docs.

### Footnote Glyphs

**Informational** (neutral, no action needed):

1. † (dagger)
2. ‡ (double dagger)
3. ⁑ (double asterisk)
4. 📌 (pushpin)

**Problem** (needs remediation/investigation):

1. ⚠️ (yellow triangle)
2. ❗ (red exclamation)
3. 📣 (megaphone)
4. 🔔 (bell)

Use them for table cell annotations only. A cell should contain at most one footnote glyph. The glyph *is* the cell content when there's no data; otherwise append it to the value (e.g. `sync commit†`).

Within a given table or list, each glyph maps to exactly one note. Glyphs may be freely reused across different tables/docs.

### Table Cell Vocabulary

Standard special values:

- **— (emdash)** — not applicable; the concept doesn't apply to this row
- **TBD** — value exists or will arrive naturally; just needs to be filled in at the appropriate time
- **TODO** — work is needed to produce the value. Blocks nothing, blocked by nothing.
- **?** — unknown whether the value can, should, or does exist
- **⚠️** — alarming situation; should be linked to a footnote explaining the concern
- **blank cell** — only for visual grouping (e.g. sub-rows). Otherwise use emdash, ?, or TBD.
- **^^^** — same link/value as the row above

### Escaping

- **Dollar signs in prose**: Escape as `\$` (IntelliJ treats `$...$` as inline LaTeX math, so two unescaped `$` in the same paragraph render the text between as italic math)
- **Dollar signs in table cells**: Safe (pipes prevent cross-cell pairing)

### Hyperlinks

Link the relevant text; don't parenthetically name the target.

- **Good**: `dates to at least [2014](#history)`
- **Bad**: `dates to at least 2014 (see [History](#history))` or `dates to at least 2014 ([evidence](#history))`

When mentioning a document by title, link the title itself — not a separate "link" word. Append `(yyyy)` or `(Mon yyyy)` after the title if the date provides context:

- **Good**: `the [Variant Detailed Design](url) (Jan 2025) specifies...`
- **Bad**: `the Variant Detailed Design page ([Jan 2025](url)) specifies...`

When citing a dated source (incident, analysis, ADR), put the parenthetical date *after* the action/verb:

- **Good**: `Rohith cataloged ([2025.09](#e-item)) 5 manifestations`
- **Bad**: `Rohith (Sep 2025) cataloged 5 manifestations`

### Stylistic Restraint

- Avoid wasting space with horizontal rules — trust headings
- Never use all-caps for emphasis (only when quoting literal all-caps strings)
- Use bold/italics sparingly; bold is fine for list-item titles or table headers

## Doc Audit Checklist

### Status Audit

Internal consistency verifiable without domain expertise:

- ✅ TOC matches actual headings
- ✅ No orphaned sections (all sections referenced in TOC or prior section)
- ✅ All links resolve (no broken anchors, no dead URLs)
- ✅ No links from tracked files to untracked files (aidocs/, tmp/, etc.)
- ✅ For docs with Confluence mirrors: no relative links (they work in markdown/GHE but break in Confluence)
- ✅ **For docs with Status/Tasks/Active Work/Work Log:**
  - Tasks rows are accurately reflected in Status rows (verbatim copies, not paraphrased)
  - Active Work subtasks relate only to ▶️ (in-progress) tasks
  - Concluded items are cleared from Active Work, moved to Work Log (not duplicated)
  - Current conversation's work is accurately timestamped in Work Log

### Semantic Audit

Claims match current reality (requires domain knowledge and cross-referencing):

- ✅ Endpoints exist and are correct
- ✅ Schemas are current
- ✅ Kafka topics match production
- ✅ CCM keys match production configuration
- ✅ Code examples parse and reflect current codebase
- ✅ Architecture diagrams reflect deployed services
- ✅ URLs are reachable and current

Semantic audit dates older than 90 days are candidates for review.

### Task Creep Audit

Forensic check that the Tasks table has not been used as a work log (invoked on demand, not every session). Requires checking git history (`git log -p` on Tasks section) for violations:

- ✅ Rows added and marked ✅ in same commit or same day's commits
- ✅ Rows backfilled after work completed (added with status already set)
- ✅ Tasks describing work that happened (not work that was scoped)

**Remediation**: Move violating task content to Work Log entries. Keep the task row only if work was genuinely planned in advance; otherwise delete it.

### When to Audit

- **Status audit**: Verify or fix doc structure after substantial edits. Update date when complete.
- **Semantic audit**: Verify content against current code/production state. Update date when complete.

---

## DRY Principles

- **No revision history** if the platform provides it (git, Confluence)
- **Exception**: Work Logs capture *why* decisions were made and provide recovery context — different purpose from revision history
- **Never say "End of document"** — even at the end of the document
- **Never link to untracked files** from tracked files
- **Avoid version-controlled comments** explaining recent corrections — git history captures changes; tracked content is for durable info
- **For temporal writing rules**, see § Temporal Writing Rules above

---

## Reference: Doc Audit Dates

### Format

Place at the end of TOC (if present), else at the end of doc. Format as a single italic non-list-item line:

```
*Status audit: YYYY.MM.DD · Semantic audit: YYYY.MM.DD*
```

Example: `*Status audit: 2026.03.18 · Semantic audit: 2026.03.16*`

### When Needed

Not all docs need audit dates. Ephemeral artifacts (aidocs, incident reports, release docs) are inherently point-in-time and don't require them.

**Docs that should have audit dates**: Reference docs (`docs/*.md`, `docs/repos/*.md`), project docs, team playbooks.

### Update Rules

- **Update status date** when you verify or fix doc structure and cross-section consistency
- **Update semantic date** when you verify content against current code or production state
- **Semantic dates older than 90 days** are candidates for review

## See Also

- [AGENTS.md](../../AGENTS.md) — agent contract, entry points, doc placement rules
- [WibeyProjectMgt.md](WibeyProjectMgt.md) — rationale for the toolkit and project structure (marketing/adoption doc)
- [ProjectTemplate.md](../templates/ProjectTemplate.md) — template and inline guidance for new project docs
