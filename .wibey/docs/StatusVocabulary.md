# Status Vocabulary

## Status Definitions


|      | Status        | Meaning                                                                | Jira                  | DX / Teflon                | PD / Statuspage    | SN / ITIL          | Google SRE |
| ---- | ------------- | ---------------------------------------------------------------------- | --------------------- | -------------------------- | ------------------ | ------------------ | ---------- |
|      | **Pending**   |                                                                        |                       |                            |                    |                    |            |
| 🔮   | FUTURE        | Beyond current scope; aspirational or follow-on work                   | —                    | —                         | —                 | —                 | —         |
| ⬜   | UNSTARTED     | Noted but not started. synonym: BACKLOG                                | —                    | —                         | —                 | —                 | —         |
| 📣   | INVOKED       | Our team notified; our incident doc opened                             | —                    | Triage Initial Assessment  | Acknowledged       | Assigned           | Response   |
| ➡️ | ROUTED        | Investigation handed off; incident still live                          | Won't Do (reassigned) | —                         | —                 | —                 | —         |
|      | **Working**   |                                                                        |                       |                            |                    |                    |            |
| 🕵️ | INVESTIGATING | Actively working root cause. synonym: ENGAGED                          | In Progress           | Investigate                | Investigating      | In Progress        | Response   |
| 🎯   | DIAGNOSED     | Root cause confirmed; fix not yet deployed                             | In Progress           | —                         | Identified         | In Progress        | Response   |
| 🛠️ | FIXING        | Fix underway — PR open, CRQ in flight                                 | In Progress           | Investigate                | —                 | In Progress        | Mitigation |
| 👀   | UNDER_REVIEW  | Fix is awaiting feedback from another person/team                      | —                    | —                         | —                 | —                 | —         |
|      | **Waiting**   |                                                                        |                       |                            |                    |                    |            |
| ⏰   | AWAITING      | Time-bounded hold; unblocking event committed and expected             | On Hold               | —                         | —                 | On Hold            | —         |
| 🛑 ❓ | BLOCKED       | Stuck on external; no committed ETA — escalate. (🛑 = action needed; ❓ = answer/decision needed) | Blocked               | —                         | —                 | On Hold            | —         |
| ↗️ | RELAYED       | Our team's work handed off; other team carrying forward                | In Progress           | —                         | —                 | —                 | Resolution |
| ⏸️ | PAUSED        | Intentionally shelved; not active but not yet canceled                 | —                    | —                         | —                 | —                 | —         |
|      | **Iterating** |                                                                        |                       |                            |                    |                    |            |
| 💥   | FIX_FAILED    | Deployed fix confirmed not working; back to investigating              | Reopened              | Investigate                | Investigating      | In Progress        | Mitigation |
| 👎   | NOT_APPROVED  | Change/fix not approved and so was not deployed                        | Won't Do              | —                         | —                 | Canceled           | —         |
| ❌   | CANCELED      | Fix attempt canceled; back to investigating                            | Canceled / Won't Do   | —                         | —                 | Canceled           | —         |
|      | **Finishing** |                                                                        |                       |                            |                    |                    |            |
| ↩️ | ROLLED_BACK   | Deployment reverted as mitigation                                      | In Progress           | Mitigate                   | Investigating      | In Progress        | Mitigation |
| 🟡   | MITIGATED     | Customer impact reduced; root cause may remain                         | —                    | Mitigated but not Resolved | —                 | In Progress        | Mitigation |
| 🔭   | MONITORING    | Fix deployed and believed stable; watching metrics before closing      | In Progress           | —                         | Monitoring         | In Progress        | Resolution |
| ✅   | RESOLVED      | Impact gone; root cause addressed (synonyms: CLOSED, DONE)             | Done / Resolved       | Resolved                   | Resolved           | Resolved           | Resolution |
| 🔵   | AS_DESIGNED   | Behavior matches spec; no fix needed                                   | Won't Fix / Invalid   | —                         | —                 | Resolved (w/ note) | —         |
| 🔹   | WONT_FIX      | Root cause known; consciously not fixing                               | Won't Fix             | —                         | Resolved (w/ note) | Resolved (w/ note) | —         |
| 🔕   | FALSE_ALARM   | Spurious or misunderstood signal; not an actual problem                | Won't Do / Invalid    | —                         | —                 | Canceled           | —         |

- **Jira** — Atlassian issue tracker; states shown are standard Jira workflow values (In Progress, On Hold, Blocked, Reopened, Done, Won't Do, Won't Fix, Canceled, Duplicate).
- **DX / Teflon** — DX Platform defines the triage phases (Triage → Investigate → Mitigate → Resolve) and the "Mitigated but not Resolved" intermediate state. Teflon is an incident management framework defining P0/P1/P2 severity and the Incident Commander role.
- **PD / Statuspage** — [PagerDuty](https://www.pagerduty.com/) on-call alerting (lifecycle: Triggered → Acknowledged → Investigating → Identified → Monitoring → Resolved) combined with Atlassian Statuspage for external status communication.
- **SN / ITIL** — ServiceNow Incidents ticketing system (lifecycle: New → Assigned → In Progress → On Hold → Resolved → Closed → Canceled; P1 Critical – P5 Very Low). [ITIL](https://en.wikipedia.org/wiki/ITIL) (IT Infrastructure Library) is the industry process standard that ServiceNow implements.
- **Google SRE** — [Google Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) uses overlapping lifecycle *phases* rather than discrete states: Detection → Response → Mitigation → Resolution → Post-Incident. Column values indicate which phase each status falls within.

## Sources

**Industry SOTA (general knowledge + external research 2026.04.24):**

- PagerDuty / Atlassian Statuspage: Triggered → Acknowledged → Investigating → Identified → Monitoring → Resolved
- ITIL / ServiceNow standard: New → Assigned → In Progress → On Hold → Resolved → Closed → Canceled
- Google SRE lifecycle phases: Detection → Response → Mitigation → Resolution → Post-Incident
- FireHydrant milestones (most granular public tool): Started · Detected · Acknowledged · Investigating · Identified · Mitigated · Resolved · Retrospective Started · Retrospective Completed · Closed
- incident.io: Triage → Investigating → Fixing → Monitoring → Impact Mitigated → Debrief Completed → Closed
- RFC 7970 IODEF (IETF standard, the only formal specification): new · in-progress · forwarded · resolved · future (5 states)
- MONITORING confirmed present in: Atlassian Statuspage, OpsGenie, GitHub Status, Cloudflare, incident.io — universally placed between fix deployment and resolved declaration; exits on clean metrics or IC judgment after a time window.
