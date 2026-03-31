# Write Coordination Test — Protocol

## Overview

A concurrent write coordination experiment. Multiple agents write to a shared
document simultaneously. Each uses `write_if_unchanged` to prevent clobbering.

## Parameters

- Target document: `~/bin/write-test/doc.md`
- Turns per agent: 10
- Slot range: 1–20
- Write interval: 5–8 seconds between turns (choose randomly each turn)
- CAS retry wait: 1–3 seconds (choose randomly)

## Your Identity

Your agent ID will be given to you when you receive this protocol (e.g. `agent-a`).

- Log file:  `~/bin/write-test/agent-YOURID.log`
- Temp file: `/tmp/wct-YOURID.md`

## Document Format

```
# Write Coordination Test

## Stats
Total turns completed: 7
agent-a: 4 turns, 1 CAS retries
agent-b: 3 turns, 2 CAS retries
Slots occupied: 6 of 20

## Slot Registry
 3: agent-b @ 2026-03-30 14:22:18 (turn 2, 0 retries)
 7: agent-a @ 2026-03-30 14:22:31 (turn 1, 0 retries)
11: agent-b @ 2026-03-30 14:23:05 (turn 3, 1 retries)
```

### Stats block rules

- `Total turns completed` — always the first stats line; sum of all agents' successful turns
- Per-agent line: `AGENT_ID: N turns, N CAS retries`
  - Insert your line alphabetically between "Total turns completed" and "Slots occupied"
  - If your line doesn't exist yet, add it
  - CAS retries = cumulative total across all your turns so far
- `Slots occupied: N of 20` — always the last stats line; count of distinct slots in registry

**All values must be parsed from the file you just read — never maintained purely from memory.**

### Slot Registry rules

- One line per slot number, sorted ascending
- Exact format: `NN: AGENT_ID @ YYYY-MM-DD HH:MM:SS (turn N, N retries)`
  - Slot number right-aligned in 2-char field: ` 3:` not `3:`
  - `retries` = CAS failures before this write succeeded for this turn
- If slot already exists: replace that line
- If slot is new: insert in sorted position; increment Slots occupied

## Algorithm

Repeat for turns 1 through 10:

1. Choose a random slot 1–20. **This slot is fixed for the turn — never re-roll on retry.**
2. Set `retries = 0` for this turn.

**Write loop (repeat until exit 0):**

3. `HASH=$(shasum -a 256 ~/bin/write-test/doc.md | awk '{print $1}')`
4. Read the full contents of `~/bin/write-test/doc.md`
5. Build new document content by parsing what you just read (step 4):
   - Increment `Total turns completed` by 1
   - Increment your turn count by 1; add `retries` to your cumulative CAS retries
   - If slot is new: increment `Slots occupied` by 1
   - Insert or replace the slot line, maintaining sort order
   - Get current timestamp for the slot line
6. Write new content to `/tmp/wct-YOURID.md`
7. Run:
   ```
   ~/bin/write_if_unchanged ~/bin/write-test/doc.md \
       --from /tmp/wct-YOURID.md \
       --expect-sha256 "$HASH" \
       --note "agent=YOURID, turn=N"
   ```
8. **Exit 0** (success): append to log, wait 5–8s, proceed to next turn
9. **Exit 3** (CAS mismatch): increment `retries`, append to log, wait 1–3s, go back to step 3
10. **Any other exit code**: log the error, abort

## Log Format

One line per write attempt appended to `~/bin/write-test/agent-YOURID.log`:

```
TIMESTAMP turn=N slot=NN attempt=N status=SUCCESS
TIMESTAMP turn=N slot=NN attempt=N status=CAS_RETRY
```

`attempt` starts at 1; increments on each retry. A `SUCCESS` line closes the turn.

## Critical Rules

- Steps 3–4 happen **inside the write loop**, immediately before step 7. Never reuse a
  hash or file contents from a prior iteration.
- Step 5 parses values from the file read in step 4 — not from local counters.
- Turns are strictly sequential — finish the write loop before starting the next turn.
