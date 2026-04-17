# Doc Audit Skill

Consolidated reference for documentation authoring, project document formatting, and audit standards for the agent-toolkit framework.

## Table of Contents

- [Document Sections](#document-sections) — requirement matrix; mandatory Work Log + Evidence for non-reference docs
  - [Tasks](#tasks) · [Status](#status) · [Active Work](#active-work) · [Evidence](#evidence) · [Work Log](#work-log)
  - [Consistency Pipeline](#consistency-pipeline) · [Where Pending Work Lives](#where-pending-work-lives)
- [Task List Conventions](#task-list-conventions) — glyph definitions, format rules, discipline rules
- [Temporal Writing Rules](#temporal-writing-rules) — timeless perspective, no relative dates, no future prose
- [Content Brittleness](#content-brittleness) — keeping docs in sync with code, line number refs, TOC maintenance
- [Ad Hoc Documents](#ad-hoc-documents) — placement in aidocs/, naming convention, when to create
- [Styling Discipline](#styling-discipline) — footnote glyphs, table cell vocabulary, hyperlink conventions
- [Doc Audit Checklist](#doc-audit-checklist) — status audit, semantic audit, task creep audit
- [DRY Principles](#dry-principles) — no revision history, no redundancy with git
- [Doc Audit Dates](#reference-doc-audit-dates) — format, when needed, update rules

## Document Sections

Every tracked doc in this repo falls into one of two categories:

- **Reference docs** — `docs/*.md`, `docs/repos/*.md`, team playbooks. Maintained for accuracy against production; do not capture ongoing work.
- **Non-reference docs** — `projects/*.md`, `incidents/*.md`, `memos/*.md`, `releases/*.md`. Capture active or historical work efforts.

**Section requirements — ● required, ○ optional, — not applicable:**

| Section | Reference docs | Projects | Incidents | Memos / Releases |
|---|---|---|---|---|
| Tasks | — | ● | ○ | — |
| Status | — | ● | — | — |
| Active Work | — | ● | — | — |
| Evidence | ○ | ● | ● | ● |
| Work Log | — | ● | ● | ● |

**Any project, incident, or memo that lacks a Work Log or Evidence section is incomplete. Add both before closing the session.**

### Tasks

A planning device — captures scoped work before it begins. Not a retroactive record of what happened.

- Rows describe **planned** work, not completed work
- Completed rows stay (scope record); remove only on cancellation (🚫)
- Status updated as work progresses

See [Task List Conventions](#task-list-conventions) for glyph definitions, format rules, and discipline rules.

### Status

Quick-read project summary for agents or humans resuming a session. Sits near the top of project docs.

- **Status rows are verbatim copies of Tasks rows** — never paraphrased or reworded
- Excerpt includes: all ▶️ in-progress tasks; tasks completed in the last 2 business days (minimum: last 3 completed, even if older); the next 2 upcoming tasks by priority
- Update whenever Tasks change: new tasks, completions, blockers, phase transitions
- **Never backdate status changes** — reflect what is true now

### Active Work

Mutable working state for in-progress items. Answers: "What are we doing right now?"

- Reflects only ▶️ (in-progress) tasks
- Contains subtasks, blockers, partial results, dependencies
- Next agent or human picks up here after an interruption
- Cleared when subtasks complete — concluded items move to Work Log, never duplicated

### Evidence

**Required in all project, incident, and memo docs.** Every verifiable empirical claim must cite its source.

**Placement:** Dedicated `## Evidence` section near the bottom, above Work Log.

**Inline citation:** Unicode dagger † (U+2020), no space before: `claim text[†](#e-descriptive-slug)`

Example: "Latency dropped 40%[†](#e-latency-drop)."

**Entry structure** — each entry is a `###` heading:

```
### Brief description of what is being evidenced

<a id="e-descriptive-slug"></a>

- **Claim**: the specific assertion being backed
- **Source**: URL, file path, git commit SHA, dashboard name, or person name + role
- **Dates**: source vintage (when authored/published) and collection date (YYYY-MM-DD, when retrieved)
- **Quote / data**: exact text excerpt, metric value, or command output
```

Omit any field that genuinely doesn't apply; include as many as possible.

**Additional rules:**
- **Many items (>5):** use `[†A1](#a1-slug)`, `[†A2](#a2-slug)`, etc.
- **Unsourced claims:** label "Inference:" or "Unverified:" until evidenced
- **Perishable data** (stats, counts, latency, costs, queue depths): add vintage parenthetical:

  ```
  claim text[(2025)](#e-slug)       — annual figures
  claim text[(2025-03)](#e-slug)    — monthly figures
  claim text[(2025-03-14)](#e-slug) — daily figures
  ```

  Granularity matches shelf life: annual for slow data, daily for fast-moving data.
- **Citing dated sources** (incident, analysis, ADR): put the date *after* the verb:

  `Rohith cataloged ([2025.09](#e-bv-sync-issue)) 5 manifestations` — not `Rohith (Sep 2025) cataloged...`

### Work Log

**Required in all project, incident, and memo docs.** Audit trail of effort — what we spent time on, what the problems were, how we moved closer to the goal. Git commits describe *what* changed; the Work Log describes *how* we got there.

- Records decisions, discoveries, costs incurred, obstacles overcome
- Provides context for why code looks the way it does
- Built incrementally — one entry every ~30 minutes during active work
- Concluded items from Active Work are recorded here, then cleared from Active Work

**Format:**

```
### 03.16 Sun Refactored cache layer

- **14:32:** Pulled PR #582, found race condition in auth middleware lock ordering
- **15:02:** Added mutex lock to fix race; unit tests updated and passing
- **15:32:** Ran full test suite; 2 flaky timeouts (unrelated), otherwise green
- **16:01:** Created PR #589 for review; ready for staging tomorrow
```

Heading: `### MM.DD Dow Title of The Day's Work` (prefix YYYY at year boundaries: `### 2026.03.16 Sun ...`)

Entry: `- **HH:MM:** Entry text`

**For incidents specifically:** Write entries in real time, not retroactively — before switching contexts, after each significant finding. Minimum required entries: when the incident opens (symptom, scope, first data inspected); when each major hypothesis is formed or ruled out; when root cause is confirmed or unresolved; when the doc is committed. **If auditing an incident with no Work Log:** flag as a critical gap; reconstruct what you can from git history and commit messages — note `(reconstructed from git; original timestamps unavailable)` if you do.

### Consistency Pipeline

Tasks → Status → Active Work → Work Log must stay in sync:

- **Tasks ↔ Status**: Status rows are verbatim copies (never paraphrased)
- **Tasks ↔ Active Work**: Active Work subtasks relate only to ▶️ tasks
- **Active Work ↔ Work Log**: Concluded items are cleared from Active Work (not duplicated)

### Where Pending Work Lives

Two containers + two flags:

**Containers (search here for "what's next"):**
- **Tasks** — planned work with defined scope; search here when deciding what to do next
- **Active Work** — in-progress subtasks/blockers; search here when resuming an interrupted session

**Flags (inline markers for non-blocking items):**
- **TODO** — low-priority improvement blocking nothing; use as code/doc comments. If it blocks something, it's a Task.
- **TBD** — placeholder for a value waiting to be filled in; use inline where the value belongs

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

- **No space between glyph and date**: `✅03.14` not `✅ 03.14` so they don't line-break in tables
- **Dates in MM.DD format** (never DD.MM): `03.14` not `14.03` or `Mar 14` so they alphabetize
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

### Footnote Glyphs in Tables

Footnotes hyperlinked from text use daggers as described above. In tables, the footnotes are so nearby/small that it's often better to link to particular footnotes using visual markers rather than hyperlinked daggers. In that case, use these:

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

The glyph *is* the cell content when the cell otherwise has no data; otherwise append it to the value.

Within a given table or list, each glyph type maps to exactly one footnote. Glyphs may be freely reused across different tables/docs.

### Table Cell Vocabulary

Standard special values:

- **— (emdash)** — not applicable; the concept doesn't apply to this cell.
- **TBD** — value exists or will arrive naturally; just needs to be filled in at the appropriate time
- **TODO** — work is needed to produce the value. Blocks nothing, blocked by nothing.
- **?** — unknown whether the value can, should, or does exist
- **⚠️** — alarming situation; should be linked to a footnote explaining the concern
- **blank cell** — only for visual spacing/grouping (e.g. subheader rows). Otherwise use emdash, ?, or TBD.
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

- **Never insert hard newlines inside a markdown paragraph.** A paragraph is one unbroken line of text. Mid-paragraph newlines produce ragged source that wraps differently in every viewer and causes visual layout bugs in rendered output (e.g. a trailing code-span on a short wrapped line can render as a block). Write the full paragraph on one line; let the editor wrap visually.
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
- ✅ **Non-reference docs (projects, incidents, memos, releases) have both a Work Log and an Evidence section**
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
- ✅ Every Walmart acronym expansion is either (a) footnoted with an evidence link (file path, doc URL, code reference) or (b) hyperlinked directly to its canonical page. Unexpanded acronyms are acceptable; confidently wrong expansions are not. If no source exists, use the acronym without expansion.
- ✅ Team system names use preferred vocabulary from [CatalogRelationships.md § Vocabulary](CatalogRelationships.md#vocabulary): BV not VGS, RelationshipRT not Relship, GroupRT not QGS, Catalog Relationships not CatRel, BVShell not BV Shell.

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

### Banned Words and Phrases

These words and phrases are always wrong in tracked docs. No exceptions.

- **"final"** / **"FINAL"** — a document is not a draft cycle. There is no final; there is just what it says. If you write "final", you are implying there were non-final versions — which is what git is for.
- **"all prior drafts superseded"** — revision narrative. Delete it.
- **"current state as of [date]"** — if the state changes, this becomes a lie. Write what is true; let git record when it became true.
- **"updated to reflect"**, **"now reflects"**, **"as updated"** — correction narrative. Just say the thing.
- **"see previous version"**, **"prior version stated"** — links to deleted content. Meaningless.
- **"superseded by"** (self-referential) — only acceptable when describing an external artifact being replaced (e.g. "the v1 API was superseded by v2"), not when describing the document itself.

If you are tempted to write any of these, ask: does the sentence say something true about the subject, or does it say something about the editing history? If the latter, delete it.

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
