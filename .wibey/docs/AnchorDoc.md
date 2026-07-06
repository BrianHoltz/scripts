# Anchor Doc Protocol

> [!NOTE]
> **Mirror-safe doc.** Contains no Walmart-proprietary content; designed to be manually
> mirrored to personal laptops. Canonical copy: `relationship-shared/docs/AnchorDoc.md`
> (also mirrored to [GitHub](https://github.com/BrianHoltz/scripts/blob/main/.wibey/docs/AnchorDoc.md)).

An *anchor doc* is the single authoritative task record for a work session. It persists
across agent sessions via git commits — agents cannot search prior conversations, so the
anchor doc is how institutional memory survives.

## Find Existing Anchor Doc

Run this protocol whenever a command needs to locate an already-active anchor doc.
Execute steps in order; stop at the first unambiguous match.

**Step F0 — Locate available doc folders.** Check the current workspace for these folder
types. They may appear directly at the repo root *or* inside a `shared/` symlink (the
work-laptop team-repo pattern). Only search folders that actually exist; skip the rest.

- `projects/` — project docs (flat files, one per long-lived project)
- `incidents/` — incident docs (quarter-organised subdirectories: `YYYY-Qn/`)
- `memos/` — memo docs
- `aidocs/` — ad hoc session records (date-organised subdirectories: `aidocs/yyyy-mm-dd/`)

Personal-laptop workspaces typically have only `aidocs/`. Workspaces using the
`shared/` symlink pattern typically have all four.

**Step F1 — Open editor tabs.** Check open files in priority order: active tab →
dirty/unsaved tabs → other open tabs. Filter for `.md` files in any available folder
from F0. Score each by topic overlap (see **Scoring** below). Use the highest-scoring
candidate if its score is unambiguously stronger than the rest.

**Step F2 — Disc search.** For each available folder in priority order —
`projects/` → `incidents/` → `memos/` → `aidocs/` — scan doc titles and first ~20 lines
(Summary or Active Work). Apply the same scoring. If any doc scores clearly higher: use
it; break ties by folder priority, then by recency.

**Step F3 — Ambiguous.** If two or more candidates score equally and neither folder
priority nor recency resolves the tie: show the user both filenames and one-line
summaries and ask which to use.

**Step F4 — None found.** The calling command decides what to do (see its own
anchor-doc step).

### Scoring

Extract 2–4 significant nouns/phrases from the current task (skip stopwords: the, a, an,
in, for, and, to, of, with). Count how many appear in the candidate doc's filename plus
its first ~20 lines. A single high-specificity term (Jira key, service name, error code,
unique proper noun) scores as 2. General terms score as 1 each. Candidacy threshold:
score ≥ 2, or one high-specificity hit. Highest score wins; if checking `aidocs/` docs,
also scan `## Active Work` — it often holds the most precise task description.
