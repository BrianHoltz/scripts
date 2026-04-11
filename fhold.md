# Concurrent Write Permit Protocol

Options presented to the user when a second writing agent finds an unreviewed writes flag on a markdown file.

## Context

Agent 2 needs to write to a file. It calls `--flag acquire` and finds Agent 1 has already flagged it — meaning Agent 1 has written changes that are pending review in the IDE.

## Menu (as presented to user)

`[filename]` has pending unreviewed changes from another agent. Resolve or ignore those changes, then indicate your decision:

- **Diff resolved, stay in review mode** — This agent will write its changes for review. Future agents finding this flag on the file will offer the same options.
- **Diff resolved, switch to unreviewed mode** — This agent will write its changes without user review. This file switches to unreviewed mode for all subsequent agent changes until all concurrent write permits have expired or been released, at which point review mode resumes automatically.
- **Diff ignored, switch to unreviewed mode** — Current on-disk state is treated as accepted; the flag is released. All subsequent agent changes to this file will be unreviewed and safely parallel (via write_if_unchanged) until all concurrent write permits have expired or been released, at which point review mode resumes automatically. ⚠️ The pending diff can be safely accepted at any time, but rejecting any part of it will immediately overwrite any disk changes (including this change by this agent) that happened after that pending diff was authored.

## Marker Types

All markers live under `/tmp/write_if_unchanged.markers/<sha256-of-repo-root>/`. Filenames mangle the repo-relative file path (slashes → `%2F`). Not in any repo; ephemeral; cleared on reboot.

Applies only to git-tracked markdown files.

### Unreviewed Writes Flag

**Meaning:** Unreviewed agent writes are on disk. If the user rejects any, the IDE will revert all changes made after those writes.

**Path:** `<mangled-path>.has_unreviewed_writes`

**When created:** Immediately before a burst write, via `write_if_unchanged --flag acquire <file>`. Created atomically (O_EXCL). On success: exit 0, prints the flag path. On contention (flag already exists): exit 1, prints the owning agent's session-id and task to stderr.

**Contents:**

```
agent: <session-id>
file: <repo-relative-path>
task: <one-line description>
acquired: <ISO timestamp>
pre-burst-sha256: <hash of file before any writes>
post-burst-sha256: <hash of file after burst completes>  ← written after burst
```

**Released by:** User resolves contention (accept or reject IDE diff) and tells agent; explicit release; TTL 30 min.

**Auto-stale detection:** If `post-burst-sha256` is set and current file hash differs → user rejected/modified the diff → flag is stale, auto-release on next check.

### Concurrent Write Permit

**Meaning:** The user authorized unreviewed safely-parallel writes on this file when the indicated agent registered this permit. Other agents may also make such writes after registering their own permit. Agents should make no IDE-reviewed writes while any permits exist for this file.

**Path:** `<mangled-path>.concurrent_write_permit.<session-id>`

**When created:** When an agent begins working on a file in unreviewed mode (i.e. after a flag contention is resolved with a "switch to unreviewed mode" choice). Agents in review mode do NOT register permits — they use flags instead.

**Contents:** Minimal — agent-id and file path. The file's **mtime is the heartbeat**; refreshed on each write to the target file.

**Released by:** Agent resignation (explicit delete when done); TTL 30 min of mtime inactivity.

**Dual purpose:**

- Signals that this file is in unreviewed mode. Any permit present = unreviewed mode. No permits + no flags = review mode (default).
- Tracks active agents so the last to resign can offer to switch back to review mode. When all permits are gone, review mode resumes automatically — no user action needed.

---

## Known Hazards

**IDEA Accept All hazard:** If the user makes any local edits to the file while reviewing an agent diff — including undos — clicking "Accept All" in IDEA will revert all such edits or undos and just accept the original proposed changset. While a `has_unreviewed_writes` flag is active, accept or reject individual diff chunks only; never use Accept All if local edits have been made.

---

## Prior Art

**Emacs `.#filename` symlink** — closest analogue to `has_unreviewed_writes`. Emacs creates a symlink (not a regular file) whose target encodes `USER@HOST.PID:BOOT`. Lives adjacent to the target file, not in /tmp. Exclusive only; no pending-review semantic; no multi-writer concept. Validates the "flag lives near the file" pattern, though we deliberately chose /tmp to avoid repo pollution.

**Git `index.lock` / `packed-refs.lock`** — validates O_EXCL atomic creation. Pure exclusive mutex with no metadata stored; recovery from crashes requires human intervention. Confirms file-based locks over POSIX are the right approach.

**POSIX fcntl/flock advisory locks** — three documented failure modes explain why we use file-based markers instead: (a) any fd close from any thread releases all locks on that inode; (b) unreliable or silent-no-op over NFS; (c) advisory-only means non-cooperating processes are not blocked. None of these affect our file-based approach.

**Non-exclusive write permits** — no prior art found. The counting-semaphore pattern exists in-process but has no widely-used filesystem incarnation for coordinating independent writers. The inversion here — multiple simultaneous write permits collectively signaling a shared mode — is uncommon in filesystem coordination.

**AI agent frameworks (AutoGen, CrewAI, LangGraph)** — all coordinate at the message or state-graph layer, not the filesystem. None treat concurrent file writes as a first-class concern or have a pending-review primitive.

**"Pending review" as a write-coordination primitive** — novel at the machine level. GitHub PR review status and Wikipedia Pending Changes are semantic analogues but are human editorial workflows operating at coarser granularity.

**Remote writer limitation** — markers in `/tmp` are invisible to agents on other hosts, the same failure mode that made POSIX flock unreliable on NFS. Deliberately out of scope: this protocol targets single-machine human-in-the-loop workflows only.
