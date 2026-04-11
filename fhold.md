# Concurrent Write Permit Protocol

## fhold usage

```
NAME
    fhold - manage under-review flags and concurrent-write permits

SYNOPSIS
    fhold {review|permit} register FILE [--agent ID] [--task TEXT]
    fhold {review|permit} release FILE [--agent ID]
    fhold {review|permit} check FILE
    fhold status FILE
    fhold gc [--tag-root DIR]

DESCRIPTION
    If a given file is being updated by only one AI agent, 
    then the user wants to review the diff in their IDE.
    But if the file is being updated by multiple AI agents,
    then the user wants the agents to do parallel writes without clobbering each other.

    fhold lets agents coordinate which mode to use. Agents
    register their intention about the file, detect when their intentions
    collide, and let the user choose.

    Agents can register two kinds of holds:

    review (has_unreviewed_writes) — exclusive. The agent's changes are on
    disk but awaiting review. If the user rejects any, the IDE reverts all
    changes made after those writes. The IDE may or may not detect the
    conflict on its own, and typically handles it poorly.

    permit (concurrent_write_permit) — non-exclusive. The user authorized
    unreviewed parallel writes when the agent registered this permit.
    Multiple agents may hold permits simultaneously. No agent should make
    IDE-reviewed writes while any permit exists for the file.



    Holds are implemented as sidecar tag files under --tag-root
    (default: /tmp/fhold.tags/). Each file is keyed by sha256 of the
    resolved target path (same scheme as write_if_unchanged locks).
    Ephemeral; cleared on reboot.

    The author's practice is to apply fhold only to git-tracked markdown files.

SUBCOMMANDS
    review register FILE  Tag FILE with has_unreviewed_writes. Atomic
                          (O_CREAT|O_EXCL). Fails if a review hold already
                          exists (contention). Records agent, task, timestamp,
                          and pre-write sha256.
    review release FILE   Remove the has_unreviewed_writes tag from FILE.
                          Typically called after the user accepts or rejects
                          the IDE diff.
    review check FILE     Print review hold status: owner agent, task, age,
                          whether post-burst hash is set, and whether stale.
    permit register FILE  Tag FILE with concurrent_write_permit for this agent.
                          Multiple permit holds may coexist. Any permit hold
                          present = unreviewed mode.
    permit release FILE   Remove this agent's concurrent_write_permit tag.
                          When all permit holds are gone, review mode resumes
                          automatically.
    permit check FILE     List all active permit holds for FILE with agent IDs
                          and last-activity times.
    status FILE           Summary: review hold state, active permit holds,
                          current mode (reviewed / unreviewed), and file sha256.
    gc                    Garbage-collect stale review holds (TTL expired, no
                          heartbeat) and stale permit holds (mtime > TTL).

OPTIONS
    --agent ID            Agent/session identifier. Default: $WIBEY_SESSION_ID
                          or $USER.
    --task TEXT            One-line description stored in the review hold
                          (review register only).
    --tag-root DIR        Tag directory (default: /tmp/fhold.tags/).
    --ttl SECS            Stale hold TTL in seconds (default: 1800).

    -H, --raw-help        Show this raw usage text and exit
    -h, --help            Show colorized usage and exit

EXIT CODES
    0  success
    1  usage error (bad arguments)
    2  contention — review hold already held by another agent
                   (review register only)
    3  no hold found (release of nonexistent hold)

EXAMPLES
    # Register a review hold before writing
    fhold review register README.md --agent ses_abc --task "update install steps"
    write_if_unchanged README.md --from /tmp/new_readme.md --expect-sha256 "$HASH"
    # ... user reviews diff in IDE, then tells agent to release ...
    fhold review release README.md --agent ses_abc

    # Switch to unreviewed mode (after contention resolution)
    fhold permit register README.md --agent ses_abc
    fhold permit register README.md --agent ses_def
    # ... both agents write freely via write_if_unchanged ...
    fhold permit release README.md --agent ses_abc
    fhold permit release README.md --agent ses_def
    # all permit holds gone → review mode resumes

    # Check file status
    fhold status README.md
```

## Context

Agent 2 needs to write to a file. It calls `fhold review register` and discovers Agent 1 already has a review hold — meaning Agent 1's changes are on disk but awaiting user review in the IDE.

## Menu (as presented to user)

`[filename]` has a review hold from another agent. Resolve or ignore the pending changes, then indicate your decision:

- **Diff resolved, stay in review mode** — This agent will register its own review hold and write its changes for review. Future agents finding a review hold will be offered the same options.
- **Diff resolved, switch to unreviewed mode** — This agent will register a permit hold and write without user review. All subsequent agent changes use permit holds until all permits have expired or been released, at which point review mode resumes automatically.
- **Diff ignored, switch to unreviewed mode** — Current on-disk state is treated as accepted; the review hold is released. All subsequent agent changes use permit holds and write safely in parallel (via write_if_unchanged) until all permits have expired or been released, at which point review mode resumes automatically. ⚠️ The pending diff can be safely accepted at any time, but rejecting any part of it will immediately overwrite any disk changes (including this agent's) that happened after that pending diff was authored.

## Hold Tags

Holds are implemented as sidecar tag files under `/tmp/fhold.tags/`. Each file is keyed by `sha256(resolved_path)[:24]`, the same scheme as write_if_unchanged locks. Not in any repo; ephemeral; cleared on reboot.

Applies only to git-tracked markdown files.

### Review Hold (has_unreviewed_writes)

**Meaning:** The agent's changes are on disk but awaiting review. If the user rejects any, the IDE reverts all changes made after those writes. The IDE may or may not detect the conflict on its own, and typically handles it poorly.

**Tag:** `<path-hash>.has_unreviewed_writes`

**When created:** Immediately before a burst write, via `fhold review register <file>`. Created atomically (O_EXCL). On success: exit 0, prints the tag path. On contention (review hold already exists): exit 2, prints the owning agent's session-id and task to stderr.

**Contents:**

```
agent: <session-id>
file: <repo-relative-path>
task: <one-line description>
acquired: <ISO timestamp>
pre-burst-sha256: <hash of file before any writes>
post-burst-sha256: <hash of file after burst completes>  ← written after burst
```

**Released by:** User resolves contention (accept or reject IDE diff) and tells agent; explicit `fhold review release`; TTL 30 min.

**Auto-stale detection:** If `post-burst-sha256` is set and current file hash differs → user rejected/modified the diff → hold is stale, auto-release on next check.

### Permit Hold (concurrent_write_permit)

**Meaning:** The user authorized unreviewed parallel writes when the agent registered this permit. Multiple agents may hold permits simultaneously. No agent should make IDE-reviewed writes while any permit exists for the file.

**Tag:** `<path-hash>.concurrent_write_permit.<session-id>`

**When created:** When an agent begins working on a file in unreviewed mode (i.e. after contention is resolved with a "switch to unreviewed mode" choice). Agents in review mode register review holds, not permit holds.

**Contents:** Minimal — agent-id and file path. The tag file's **mtime is the heartbeat**; refreshed on each write to the target file.

**Released by:** Explicit `fhold permit release`; TTL 30 min of mtime inactivity.

**Dual purpose:**

- Signals that this file is in unreviewed mode. Any permit hold present = unreviewed mode. No permit holds + no review holds = review mode (default).
- Tracks active agents so the last to release can restore review mode. When all permit holds are gone, review mode resumes automatically — no user action needed.

---

## Known Hazards

**IDEA Accept All hazard:** If the user makes any local edits to the file while reviewing an agent diff — including undos — clicking "Accept All" in IDEA will revert all such edits or undos and just accept the original proposed changeset. While a review hold is active, accept or reject individual diff chunks only; never use Accept All if local edits have been made.

---

## Prior Art

**Emacs `.#filename` symlink** — closest analogue to the review hold. Emacs creates a symlink (not a regular file) whose target encodes `USER@HOST.PID:BOOT`. Lives adjacent to the target file, not in /tmp. Exclusive only; no pending-review semantic; no multi-writer concept. Validates the "tag lives near the file" pattern, though we deliberately chose /tmp to avoid repo pollution.

**Git `index.lock` / `packed-refs.lock`** — validates O_EXCL atomic creation. Pure exclusive mutex with no metadata stored; recovery from crashes requires human intervention. Confirms file-based tags over POSIX are the right approach.

**POSIX fcntl/flock advisory locks** — three documented failure modes explain why we use file-based tags instead: (a) any fd close from any thread releases all locks on that inode; (b) unreliable or silent-no-op over NFS; (c) advisory-only means non-cooperating processes are not blocked. None of these affect our file-based approach.

**Non-exclusive permit holds** — no prior art found. The counting-semaphore pattern exists in-process but has no widely-used filesystem incarnation for coordinating independent writers. The inversion here — multiple simultaneous permit holds collectively signaling a shared mode — is uncommon in filesystem coordination.

**AI agent frameworks (AutoGen, CrewAI, LangGraph)** — all coordinate at the message or state-graph layer, not the filesystem. None treat concurrent file writes as a first-class concern or have a pending-review primitive.

**"Pending review" as a write-coordination primitive** — novel at the machine level. GitHub PR review status and Wikipedia Pending Changes are semantic analogues but are human editorial workflows operating at coarser granularity.

**Remote writer limitation** — tags in `/tmp` are invisible to agents on other hosts, the same failure mode that made POSIX flock unreliable on NFS. Deliberately out of scope: this protocol targets single-machine human-in-the-loop workflows only.
