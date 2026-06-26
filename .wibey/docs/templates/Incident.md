# Incident Title

## Summary

*Replace everything in italics with incident info. No paragraphs! Sentences/clauses should become sub-bullets.*

- **Where** Tracked: *One sub-bullet per tracker, sorted earliest first. No ticket-type labels. Include ticket title (abbreviate if long).*
  - **2026.04.24.Fri** [`CATGTRLSHP-193`](https://jira.megacorp.com/browse/CATGTRLSHP-193) VP creation activities stuck *(Jira: date bold, ID linked, title after)*
  - [`2026.04.24.Fri Brian Holtz #quarth-support`](https://slack.megacorp.com/archives/C...) seller variant grouping blocked *(Slack: entire string linked, context after)*
- [**What**](#scope) Business Impact: envs=stg|prod, tenants=list *(both mandatory, both lowercase). What broke for whom. Volumes if known.*
- [**Why**](#root-cause-analysis) It Happened: *Current leading hypothesis. Will change — that's fine, update it.*
- [**How**](#symptoms) It Manifests — [Scope](#scope): *Synthesis of Symptoms + Scope: what the problem looks like and how far it reaches. 2–3 bullets max; not root cause. Must include 1–2 direct evidence links — ideally an OLS Discover permalink (Share → Copy URL, encodes query + time histogram) and/or a Grafana panel — that let any reader (1) confirm the symptoms are real and when they began, and (2) check whether they're still happening now. Capture the OLS permalink while you're in OLS before closing the tab — it's nearly impossible to reconstruct later.*
- **Which** Systems Involved: *list of systems, each proper noun linked to most relevant target in docs/ or in this doc*.
- **Who:** *One sub-bullet per person. Always include the team member(s) who investigated. Reporter is often already named in Where Tracked.*
  - *Name (handle) — Team, role*
- [**When**](#timeline): *(All timestamps: `yyyy.mm.dd.Dow HH:MM` — HH:MM required when known; TBD otherwise. Detected and Engaged are mandatory COE fields. Invoked and Routed are team additions — collapse into Detected/Invoked or Routed/Engaged when simultaneous.)*
  - Introduced: *(Required — even if estimated. When the causal code/config/data change landed — the moment the vulnerability became possible. Estimate from git history, deploy log, or CCM change history. May predate Started by weeks or years.)*
  - Started: *(Required — even if estimated. When the defect first activated — conditions first crossed the trigger threshold. May predate Detected by days.)*
  - Detected: *(mandatory — when problem first observed; write as Detected/Invoked if the team was notified at the same moment)*
  - Invoked: *(when the team was notified — omit if same as Detected)*
  - Engaged: *(mandatory — when the right team started working; write as Routed/Engaged if the team handed off at the same moment)*
  - Routed: *(when the team handed off to the owning team — omit if your team owns the fix)*
  - Resolved: *(when the problem was fixed)*

## Status

*Where things stand right now. Updated each session. Use a token from [StatusVocabulary.md](../StatusVocabulary.md) — optionally qualified with an em-dash (e.g. `INVESTIGATING — root cause undiagnosed`).*

## Contents

- [Summary](#summary)
- [Status](#status)
- [Tasks](#tasks)
- [Active Work](#active-work)
- [Draft Next Comms](#draft-next-comms)
- [Open Questions](#open-questions)
- [Symptoms](#symptoms)
- [Scope](#scope)
- [Investigation Sections](#incident-specific-investigation-sections)
- [Timeline](#timeline)
- [Root Cause Analysis](#root-cause-analysis)
- [Learnings](#learnings)
- [Action Items](#action-items)
- [Context](#context)
- [Closed Questions](#closed-questions)
- [Evidence](#evidence)
- [Work Log](#work-log)

## Tasks

Evolving investigation plan. Unlike project docs, tasks are added as the investigation unfolds — not pre-planned. Keep granularity coarse: a task is a major investigative thread or remediation step, not a sub-step. Use the standard status glyphs (▶️ ✅ ⏳). Completed tasks stay in the table — the table shows what we thought was important to investigate and whether we did it. The Work Log captures the detail of how each task played out. Because investigations are fast-moving and hard to pre-plan, a coarse Task may first appear in the table already completed. Keep the table to ~10 entries; use Active Work for current sub-steps when the table would otherwise get noisy.


| Task | Status | Notes |
| ---- | ------ | ----- |

## Active Work

*Optional. Use only when the Tasks table would become noisy without it — typically when an investigation thread is actively in progress and has multiple concurrent sub-steps worth tracking. Delete this section (or leave it empty) when not needed.*

Current sub-steps, blockers, and partial results for the in-progress thread. Mutable working state — updated every session. When a sub-step completes, write a Work Log entry and remove it from here. This is where the next agent or human picks up if the session is interrupted.

## Draft Next Comms

Pre-composed messages ready to send — Slack replies, Jira comments, emails. Each draft is a `###` sub-heading with target, a `Status: DRAFT` or `Status: READY` line, and the message body in a blockquote. Include an [incident doc](link) reference in every draft. When a draft is sent, delete it from here entirely and record one Work Log entry with the destination and Slack `ts` or message URL.

## Open Questions

Unresolved decisions that need an *answer* from your own team — not an action, and not a response from another team. If a question turns out to need an external answer, *convert* it: remove it from here, create a Draft Next Comms entry, and mark any blocking task 🛑 — never leave a question in both places. Every question that blocks an investigative thread must have a corresponding ▶️ (or 🛑) row in the Tasks table. Name a tool or owner if known — don't let uncertainty about that stop you from writing the question. Move to Closed Questions once answered — never delete.

## Symptoms

Full description of observable behavior. Reproduces the Summary bullets with evidence: error messages verbatim, counts, affected tenants, time window. Reference Evidence entries for sourced claims.

## Scope

Documents the footprint of the incident across five dimensions: impact, systems, people, data entities, and time.

- **Business/Customer Impact:** Full expansion of the Summary bullet. What broke for whom, which tenants (US/CA/STG/PROD), estimated volume or percentage affected, customer-facing vs. internal-only.
- **Systems:** Services involved — producer, consumer, dependency. Who owns each.
- **People/Teams:** Reporters, on-call, adjacent teams engaged. xMatters/Slack handles.
- **Entities:** Specific catalog records in play — WPIDs, GTINs, DGIDs, feed IDs, item_ids. The sample set for verification queries.
- **Time:** Impact duration synthesized from [Summary → When](#summary) timestamps — do not repeat raw timestamps here. Cover the total customer-impact window (Started → Resolved or mitigation); whether it crossed peak hours, a release window, or a maintenance window; whether impact was continuous or intermittent.

## [Incident-specific investigation sections]

Name these for what was investigated, not for the conclusion. Common examples:

- Feed / Payload Analysis
- Database State
- OLS / Grafana Findings
- Code Path
- Config State (CCM, YAML, feature flags)

Each section: what was examined, what was found, what it means. Prefix unverified inferences with "Inference:". Every empirical claim gets a dagger footnote to Evidence.

## Timeline

Unified chronological record of what happened, including events discovered retroactively.

- Time format: `YYYY.MM.DD.Dow HH:MM TZ`
- Include: deploys, config changes, upstream events, alerts, stakeholder communications, mitigations
- Exclude: routine investigation steps — those belong in Work Log
- Retroactive entries are fine; note them as such if timing is approximate

## Root Cause Analysis

The definitive explanation of why the incident happened. Distinguish the proximate trigger (the immediate cause) from the systemic root cause (the underlying condition that made the trigger possible). Never skip this section — even a one-liner is better than leaving it blank. For complex incidents, use the 5 Whys: start with the symptom and ask Why until you reach something structural, not just operational.

Avoid "confirmed" for active claims — use "evidenced by [†]" or "undefeated" (tested against named alternatives; all failed to falsify) until disconfirming checks pass. See [AgentAntiPatterns.md](../AgentAntiPatterns.md) (your local library of painful lessons).

### Counterfactual Analysis

Required when root cause is contested or non-obvious. Apply the methodology in [IncidentRCA.md](../IncidentRCA.md#counterfactual-analysis).

## Learnings

Update as the investigation progresses — don't wait for resolution. Capture insights as they emerge.

- **How It Could Have Been Avoided:** What change — to code, config, process, or architecture — would have prevented this class of incident.
- **How It Could Have Been Detected:** What alert, dashboard, or monitoring gap meant this surfaced late. Was the defect silent (no observable signal between Started and Detected)? MTTD = When → Started → Detected; Dormant window = When → Introduced → Started. What alert would have cut MTTD?
- **How It Could Have Been Investigated:** Where the investigation lost time — wrong tool, wrong field, wrong hypothesis held too long. Feed findings here into `shared/docs/AgentAntiPatterns.md` (or wherever you keep your shared docs).

## Action Items

Remediation work, distinct from investigation Tasks above.

### Exposure Check

For each applicable [dimension](../IncidentRCA.md#problem-dimensions), ask: **Which other [X] might share the same trigger conditions, and what evidence confirms it's clean?**

Example questions:
- Which other relationship types might share this trigger — if VP is affected, what evidence confirms CASEPACK is clean?
- Which other execution modes (async, sync, batch, backfill) share this code path, and what evidence confirms each is clean?
- Which other tenants or environments might be affected, and what evidence confirms each is clean?

## Context

### Related Incidents

Links to similar prior incidents with one-line description of the relation.

### Documents

Relevant `shared/docs/repos/` (or wherever you keep your shared docs) entries, pipeline docs, design docs consulted. External Confluence links, service registry entries, Jira epics.

### Concepts

Definitions of terms, acronyms, and system components specific to this incident. Define any term at first use — inline if brief, or here if the explanation is longer than a parenthetical. Every acronym introduced in the doc should have an entry here.

**Linking and sourcing conventions:**

- **Link every use** of each term in the doc to its definition: `[P0001](#concepts)`, `[OCC](#concepts)`. Exception: the definition itself and H1 titles.
- **Quote or link official definitions first.** If the term is defined in `shared/docs/` (or wherever you keep your shared docs) (e.g., `CatalogIDs.md`, `CatalogRelationships.md`, a `repos/<service>.md`), quote or paraphrase from there and link to the source rather than writing a new definition from scratch. This keeps terminology consistent across all incident docs.
- **Add new terms back to shared/docs/.** If you define a concept here that belongs in a shared doc (a new acronym, a system component, a platform behavior), add it there too. Incident docs are ephemeral; `shared/docs/` (or wherever you keep your shared docs) is the long-lived reference.

## Closed Questions

Open Questions that have been resolved. Move entries here verbatim; add the resolution and date. Do not delete — the record of what we ruled out and why is part of the investigation audit trail.

## Evidence

Every sourced claim uses a dagger footnote: `claim[†](#e-slug)`. Label unsourced claims "Inference:" until evidenced. See the doc-audit skill for the Evidence protocol. Entry format:

### Brief description of what is being evidenced

<a id="e-descriptive-slug"></a>

- **Claim**: the specific assertion being backed
- **Source**: URL, file path, git commit SHA, OLS query, Slack permalink, or dashboard name
- **Dates**: source vintage (when authored/published) and collection date (YYYY.MM.DD.Dow, when retrieved)
- **Quote / data**: exact text excerpt, metric value, or command output

## Work Log

Append-only. Timestamped with `date "+%H:%M"` — never estimated. Retroactive entries use `bef.HH:MM`. One entry per significant discovery or decision. Most investigation activity lives here, not in Timeline.

### MM.DD Dow

- **HH:MM:** Entry.
