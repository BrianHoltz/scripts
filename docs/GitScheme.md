# GitScheme.md - Repo Organization Plan

## Snapshot (2026.05.02 final)

- `~/Documents`: clean. `Google Drive/` subtree removed (migrated to `~/My Drive`). `.gitignore` pruned of dead Google Drive rules.
- `~/My Drive`: git pointer repaired → `~/gitdirs/gdrive`. Legacy Documents history imported via `git filter-repo` (322 commits). Pushed to `BrianHoltz/gdrive`. ✅ Working.
- `lpscc`: gitdir at `~/gitdirs/lpscc`, worktree at `LP SCC Financial/` (parent folder). All 23 commits preserved with paths rewritten to Admin/*. Pushed to `BrianHoltz/lpscc`. ✅ Working, ready for future expansion.
- `wiki`: re-cloned from `BrianHoltz/wiki` after local object-store corruption (crash on 2025.12.06). Corrupt copy archived at `wiki.corrupt.20260502`.
- `~/Personal.code-workspace`: multi-root workspace with 4 roots (GDrive, Documents, LPSCC, bin). Git detection set to `subFolders` for nested repo visibility.

## Requirements (Confirmed)

- Establish the new long-term git scheme.
- Migrate `Documents/Google Drive/*` history into `~/My Drive` repo (FamilyEncyclopedia.md=155 commits, Log Family.txt=48, etc — worth preserving).
- Agents see across all repos in one VS Code window.
- Minimize Explorer panes; exclude `src/*`.
- Back up lpscc to a private GitHub repo, with workspace root at `LP SCC Financial/` level.
- **Work laptop access (read-only in practice):** On the work laptop, VPN off allows Drive to sync `~/My Drive` in mirror mode — fine for reading. Any edits made that way bypass git entirely (no history, no merge tracking). Google Drive's conflict resolution creates a duplicate file named "filename (Conflicted copy ...)" rather than merging; it cannot reconcile those with git. Treat Drive-mirror access as read-only; all real edits go through a git commit on the personal laptop.

## Workspace Architecture (North Star)

### How VS Code multi-root workspaces actually work

- Each `"folders"` entry in `.code-workspace` → one Explorer root pane. Four entries = four panes.
- Nested git repos (repos inside a folder root) appear as subfolders in Explorer — no extra pane.
- Source Control sidebar: one section per repo, regardless of Explorer layout. Five repos = five Source Control sections, whether you have 1 folder root or 5.
- `git.autoRepositoryDetection: "openEditors"` suppresses phantom repo detection noise.

### Should `~/bin/` move under `~/Documents/`?

The appeal: `~/Documents` as a root would show `bin/` as a subfolder, reducing Explorer panes from 4 to 3.

**Reasons not to do it:**

- `~/bin/` is load-bearing infrastructure. `$PATH`, `~/.claude/CLAUDE.md`, `~/.cursor/cursorrules`, per-repo `.github/copilot-instructions.md` symlinks, and shell rc files all hardcode or resolve `~/bin/`. The symlink would work for `$PATH` but every agent or script that calls `~/bin/fhold`, `~/bin/safewrite`, etc. resolves the symlink at call time — fragile if the symlink ever breaks.
- Every new laptop restore requires: clone bin → put it in the right place → create symlink → verify PATH. Currently it is: clone bin → done.
- `~/Documents` is a git repo. Putting a separate git repo inside it means Documents must gitignore `bin/`. Any mistake in that gitignore silently leaks private paths into the public `scripts` repo or noise into `Documents`.
- The gain is one fewer Explorer pane. The Explorer pane count is not actually painful at 4.
- Source Control pane count is unchanged regardless — you still have one section per repo.

**Verdict: keep `~/bin/` where it is, and keep it as a separate workspace root.**

The real case for a separate `bin/` root is not filesystem layout — it's that `~/bin/` is actively edited on both laptops while the other roots are personal-laptop-only. A separate root makes it easy to open `~/bin/` alone on the work laptop without pulling in `Documents`, `My Drive`, or LPSCC. Collapsing it into `Documents` would save one Explorer pane but cost that flexibility.

### Recommended North Star: 4-root workspace

```
~/Personal.code-workspace   (local to laptop, not in any git repo)

Roots:
  ~/My Drive          → gdrive repo (separate git dir at ~/gitdirs/gdrive)
  ~/Documents         → Documents repo + wiki nested repo
  LP SCC Financial/   → lpscc repo (git dir at ~/gitdirs/lpscc), Admin/ tracked
  ~/bin               → scripts repo

Excluded by design:
  ~/src/*             → too many repos, work-laptop-specific

Git detection: git.autoRepositoryDetection = "subFolders"
```

This gives 4 Explorer panes and agents can search/edit across all of them. Source Control shows 4 sections (gdrive, Documents, lpscc, scripts) plus wiki as a 5th when it has changes.

If you ever find 4 panes annoying, the path to 3 is: accept that `~/Documents` shows `bin/` as a plain subfolder (not a git root pane) by symlinking, with the known caveats above.

## Repo Census (Current State)

| Repo | Working tree | Git dir | Remote | Laptops | Status |
| --- | --- | --- | --- | --- | --- |
| `scripts` | `~/bin` | in-tree | `BrianHoltz/scripts` public | personal + work | ✅ operational |
| `Documents` | `~/Documents` | in-tree | `BrianHoltz/Documents` private | personal | ✅ clean; Google Drive path removed |
| `gdrive` | `~/My Drive` | `~/gitdirs/gdrive` | `BrianHoltz/gdrive` private | personal | ✅ pointer repaired; 322-commit history imported; clean status |
| `lpscc` | `LP SCC Financial/` | `~/gitdirs/lpscc` | `BrianHoltz/lpscc` private | personal | ✅ 23 commits with paths rewritten to Admin/*; ready for future expansion |
| `wiki` | `~/Documents/HoltzDotOrg/Thoughts/wiki` | in-tree | `BrianHoltz/wiki` public | personal | ✅ re-cloned after corruption |
| `src/*` | `~/src/<name>` | in-tree | GitHub public | personal | excluded from workspace |

## Session Update (2026.05.02 — Final)

### Final Configuration Achieved

**GDrive repo:**
- Worktree: `/Users/brian/My Drive`
- Git dir: `~/gitdirs/gdrive`
- Status: ✅ Clean, 322-commit history, pushed to BrianHoltz/gdrive

**LPSCC repo — Re-rooted to Parent:**
- **Old state**: worktree at `LP SCC Financial/Admin/`, tracked Admin files as bare names
- **New state**: worktree at `LP SCC Financial/`, tracked Admin files as Admin/*, repo root at parent
- Git dir: `~/gitdirs/lpscc` (unchanged location)
- History: ✅ All 23 commits preserved; git-filter-repo rewrite prepended `Admin/` to all file paths
- Benefit: Can now commit files from anywhere under LP SCC Financial (not just Admin/)
- Pushed: ✅ Rewritten history pushed to BrianHoltz/lpscc (forced update)

**Workspace:**
- File: `~/Personal.code-workspace`
- Git detection: `subFolders` (shows nested repos and enables immediate Source Control visibility)
- Folder structure:
  - GDrive (`~/My Drive`) — direct repo root
  - Documents (`~/Documents`) — repo root + nested wiki
  - LPSCC (`LP SCC Financial/`) — repo root with Admin tracked
  - bin (`~/bin`) — repo root

### Result

- **Source Control pane**: Shows 4 main sections (gdrive, Documents, lpscc, scripts) + wiki when active
- **No nested repos hidden**: `subFolders` detection means repos appear immediately without opening files
- **LPSCC shown as "LPSCC"**: Named after workspace folder, not "Admin"
- **Future flexibility**: LPSCC repo root is now at parent level, enabling commits of other folders (e.g., Treasurer Reports) when desired

### Technical Notes

- Backups preserved: `~/gitdirs/lpscc.backup3.20260502` (pre-rewrite state)
- Filter-repo clean: No Admin/Admin/ nesting; paths correctly rewritten before checkout
- Remote restored: Origin correctly points to BrianHoltz/lpscc after forced push

## Plan

### Phase 1: Reconnect `~/My Drive` to its git dir

Repair the stale `.git` pointer (currently points to `/Users/b0h0166/gitdirs/gdrive`, which does not exist on this laptop):

```bash
mkdir -p ~/gitdirs

# If local gitdir is missing, reconstruct from GitHub.
if [ ! -d ~/gitdirs/gdrive ]; then
  git clone --bare git@github.com:BrianHoltz/gdrive.git ~/gitdirs/gdrive
fi

# Re-point working tree to this laptop's path.
printf 'gitdir: %s\n' "$HOME/gitdirs/gdrive" > "$HOME/My Drive/.git"

# Validate
git --git-dir="$HOME/gitdirs/gdrive" --work-tree="$HOME/My Drive" status
git --git-dir="$HOME/gitdirs/gdrive" --work-tree="$HOME/My Drive" remote -v
```

### Phase 2: Migrate history from `Documents` into `My Drive`

**Why it matters**: 22 files worth tracking; the high-value ones have deep history in `Documents`:
`FamilyEncyclopedia.md`=155 commits, `Log Family.txt`=48, `Log Holtzes.md`=12, `FamilyTree.md`=19, etc.

**Pre-verified**: all 7 files that differ between old snapshot and current `~/My Drive` have been diff-reviewed; `~/My Drive` is newer in every case. `-X ours` is confirmed safe.

**Why `git subtree split` failed in testing**: the space in `"Google Drive"` causes the git subtree command to misparse the prefix even when quoted. Use `git filter-repo` instead (reliable with spaces):

```bash
# 0) Ensure git-filter-repo is available.
pip install git-filter-repo 2>/dev/null || brew install git-filter-repo

# 1) Create filtered clone of Documents with only the Google Drive subtree.
TMP=$(mktemp -d)
git clone /Users/brian/Documents "$TMP/docs-filtered"
cd "$TMP/docs-filtered"
git filter-repo --subdirectory-filter "Google Drive" --force
# Result: commits now have files at root (FamilyDocuments/...), matching My Drive layout.

# 2) Fetch from filtered clone into My Drive repo.
cd ~/My\ Drive
git remote add docs-filtered-local "$TMP/docs-filtered" 2>/dev/null || true
git fetch docs-filtered-local

# 3) Merge with -X ours (safe: all 7 conflict files verified, My Drive is newer).
git merge --allow-unrelated-histories -X ours --no-ff docs-filtered-local/main \
  -m 'chore: import legacy Google Drive history from Documents repo'

# 4) Cleanup temp remote.
git remote remove docs-filtered-local
rm -rf "$TMP"
```

After this, `git log --follow -- FamilyDocuments/FamilyEncyclopedia.md` in `~/My Drive` will show the full 155-commit ancestry.

### Phase 3: Clean up `Documents` repo

After Phase 2 is verified:

- Commit the expected `Google Drive/*` deletions in `~/Documents` (all files migrated to `~/My Drive`).
- Keep `HoltzDotOrg/...` and other non-Drive content untouched.
- Push both repos.

Commit message for `~/Documents`:

```
chore: remove stale Google Drive path — files migrated to ~/My Drive repo
```

Also commit the blogtoc.js modification visible in the Source Control panel.

### Phase 4: Unified no-src workspace

Create `~/Workspaces-no-src.code-workspace` (local to laptop, not tracked in any repo):

```json
{
  "folders": [
    {
      "path": "/Users/brian/My Drive",
      "name": "gdrive"
    },
    {
      "path": "/Users/brian/Documents",
      "name": "Documents"
    },
    {
      "path": "/Users/brian/Library/CloudStorage/GoogleDrive-brianholtz1965@gmail.com/Shared drives/LP SCC Financial",
      "name": "lpscc"
    },
    {
      "path": "/Users/brian/bin",
      "name": "scripts"
    }
  ],
  "settings": {
    "git.autoRepositoryDetection": "openEditors"
  }
}
```

Notes:
- Absolute paths used throughout because LP SCC Financial lives outside `$HOME` and relative paths would be unreliable.
- LPSCC root is `LP SCC Financial/` (not `Admin/`); VS Code will detect the nested git repo in `Admin/` via autoRepositoryDetection.
- `src/*` intentionally excluded.
- `wiki` not listed as a root — it is nested inside `Documents/` so it appears as a subfolder in Explorer and as a separate section in Source Control automatically.

### Phase 5: Back up lpscc to GitHub

The gitdir survived at `~/.git-lpscc-admin` (23 commits, no remote). First move it to the canonical location, then push.

```bash
WORKTREE="/Users/brian/Library/CloudStorage/GoogleDrive-brianholtz1965@gmail.com/Shared drives/LP SCC Financial/Admin"

# 1) Move gitdir to canonical location.
mkdir -p ~/gitdirs
mv ~/.git-lpscc-admin ~/gitdirs/lpscc

# 2) Update core.worktree in the moved gitdir.
git --git-dir=~/gitdirs/lpscc config core.worktree "$WORKTREE"

# 3) Validate.
git --git-dir=~/gitdirs/lpscc --work-tree="$WORKTREE" status

# 4) Create private GitHub repo and push full history.
gh repo create lpscc --private
git --git-dir=~/gitdirs/lpscc remote add origin git@github.com:BrianHoltz/lpscc.git
git --git-dir=~/gitdirs/lpscc push -u origin main
```

Note: the git worktree is currently `Admin/` (matching all tracked file paths). The VS Code workspace root is one level up at `LP SCC Financial/` — these are independent and both correct.

## Operating Rules (Carry Forward)

- Always push every repo to GitHub (no local-only history).
- Drive-hosted working trees use separate git dirs under `~/gitdirs/*`.
- `.git` pointer files are expected to break across usernames; fix by rewriting the pointer.
- Treat Drive and laptops as caches; GitHub is the durable source of truth.

## Execution Order

1. ✅ Phase 5: push lpscc to GitHub
2. ✅ Phase 1: repair `~/My Drive` git pointer
3. ✅ Phase 2: import history from `Documents` into `~/My Drive`
4. ✅ Validated: `git log --follow -- FamilyDocuments/FamilyEncyclopedia.md` traces back continuously
5. ✅ Phase 3: cleanup commit in `~/Documents`, push both repos
6. ✅ Phase 4: create `~/Workspaces-no-src.code-workspace`
7. ✅ wiki: re-cloned from `BrianHoltz/wiki` after corruption

All phases complete as of 2026.05.02.
