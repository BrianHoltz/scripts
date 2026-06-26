# Incident RCA Reference

Reference for root cause analysis of incidents on your platform. Provides the analytical toolkit used across all incident docs — Problem Dimensions, Counterfactual Analysis, and Exposure check. These are centralized here to keep incident templates thin and avoid repeating the taxonomy in every incident doc.

## Contents

- [Problem Dimensions](#problem-dimensions)
- [Counterfactual Analysis](#counterfactual-analysis)

## Problem Dimensions

The axes on which incidents vary. Each axis partitions the affected population differently — a good root cause theory must explain the distribution on every applicable axis, not just the symptom. Used in [Counterfactual Analysis](#counterfactual-analysis) and the [Exposure check](#exposure-check).

- **Object** — the entity being acted on; see [CatalogIDs.md](CatalogIDs.md) (WPID, GTIN, DGID, IGID…)
- **Relationship type** — refinement of Object that bifurcates business rules; see [CatalogRelationships.md](CatalogRelationships.md) (VP, CAREPLAN, VIRTUALPACK…)
- **Classification** — refinement of Object for reporting/rule application (product classifications, reporting hierarchies); see [CatalogIDs.md](CatalogIDs.md)
- **Subject** — who or what initiated the operation (service, API consumer, seller account, sender ID)
- **Channel / source** — item origin type: 1P supplier vs 3P marketplace. Distinct from Subject — same seller can send both.
- **Verb** — the operation, event type, endpoint, or action (CREATE, UPDATE, DELETE; Kafka event type; REST method)
- **Trigger / entry point** — the specific request, feed, or job that delivered the Verb (MP item feed, backfill job, async Kafka message). Not a trace key — correlationID belongs in Evidence.
- **Mode** — execution mechanism: async stream, sync API, batch job, backfill
- **Flow / pipeline** — named end-to-end process: product setup, relationship flow, variant batching; see [CatalogArchitecture.md](CatalogArchitecture.md)
- **System / service** — service where the defect or exposure lives (BV, RelationshipRT, variant-grouping-stream)
- **Tenant** — business unit (US Walmart, CA Walmart, Sam's Club…)
- **Locale** — language/currency/regulatory variant within a tenant
- **Environment** — stg/prod/canary/teflon, cluster, datacenter
- **Time** — when the defect started relative to system changes
- **Scale / rate** — how many entities affected, how often; applies to both bounding (Counterfactual) and extending (Exposure)

## Counterfactual Analysis

<!-- KT origin: Kepner-Tregoe Problem Analysis (1958). -->

Required when root cause is contested or non-obvious. A theory that can't explain its counterfactuals is wrong or incomplete. Fill these before committing to a root cause.

For each relevant [Problem Dimension](#problem-dimensions):
- Which [X] is affected that your theory says shouldn't be?
- Which [X] isn't affected that your theory says should be?

Examples:
- Relationship type: VP affected; CAREPLAN not — does the theory explain why?
- Verb/operation: CREATE affected; UPDATE not — or vice versa?
- Mode: async path affected; sync API not — does the code path diverge there?
- Time: Jun 15 affected; Jun 14 not — what changed between them?
- Scale/rate: 5 WPIDs affected; why not the 50 others from the same seller?

"Unknown" is a valid answer — it flags a gap. Findings carry forward to the Exposure check.
