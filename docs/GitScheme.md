# GitScheme.md - Repo Organization Plan

## Snapshot (2026.05.02)

What is true right now:

- `~/Documents` is a git repo on `main` with `origin=git@github.com:BrianHoltz/Documents.git`.
- The many `D` entries under `Google Drive/...` are expected path deletions because `~/Documents/Google Drive` no longer exists.
- Every one of those deleted tracked files exists in `~/My Drive/...` at the same relative path minus the `Google Drive/` prefix.
- `~/My Drive` contains a `.git` pointer file, but it points to `/Users/b0h0166/gitdirs/gdrive` (old laptop username path), which does not exist here.
- `BrianHoltz/gdrive` exists on GitHub.

Interpretation:

- This is not content loss. It is a path migration plus a stale `--separate-git-dir` pointer after laptop restore.

## Requirements (Confirmed)

- Establish the new long-term git scheme.
- Preserve and migrate history for prior `~/Documents/Google Drive/*` tracked files into the `~/My Drive` repo.
- Keep `~/Documents` history intact.
- Use a `.code-workspace` setup so one VS Code window can see all repos in this census except `~/src/*`.

## Repo Census (Target)

- `scripts`: `~/bin` (in-tree `.git`), remote `BrianHoltz/scripts`.
- `Documents`: `~/Documents` (in-tree `.git`), remote `BrianHoltz/Documents`.
- `gdrive`: working tree `~/My Drive`, git dir `~/gitdirs/gdrive` (separate git dir), remote `BrianHoltz/gdrive`.
- `lpscc`: shared Drive folder (path TBD), git dir `~/gitdirs/lpscc` (separate git dir), private remote.
- `wiki`: nested repo at `~/Documents/HoltzDotOrg/Thoughts/wiki`.
- `src/*`: intentionally excluded from the unified workspace file.

## Plan

### Phase 1: Reconnect `~/My Drive` to its git dir

Repair the stale pointer first so `~/My Drive` is a working repo again:

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

### Phase 2: Migrate history from `Documents` old root to `My Drive`

Goal: preserve commit ancestry for former `Google Drive/*` files while making `~/My Drive/*` canonical.

```bash
# 1) In Documents repo, create a history branch only for the old subdir.
cd ~/Documents
git subtree split --prefix='Google Drive' -b migrate/gdrive-history

# 2) In My Drive repo, import that history branch.
cd ~/My\ Drive
git remote add documents-local ~/Documents 2>/dev/null || true
git fetch documents-local migrate/gdrive-history

# 3) Merge histories; prefer current My Drive content on conflicts.
git merge --allow-unrelated-histories -X ours --no-ff documents-local/migrate/gdrive-history \
  -m 'chore: import legacy Google Drive history from Documents repo'
```

Notes:

- `-X ours` keeps current `~/My Drive` file content if conflicts occur while still bringing in history graph.
- After this, `git log --follow -- <path>` in `~/My Drive` should show legacy ancestry for migrated files.

### Phase 3: Clean up `Documents` repo

After Phase 2 is verified:

- Keep non-Drive files in `~/Documents` as-is (for example `HoltzDotOrg/...`).
- Commit expected `Google Drive/*` removals in `~/Documents` with a clear migration message.
- Push `~/Documents` and `~/My Drive`.

Suggested commit message in `~/Documents`:

- `chore: remove obsolete Google Drive path after migration to ~/My Drive`

### Phase 4: Unified no-src workspace

Create one workspace file (local to laptop) that includes all census repos except `~/src/*`.

Recommended location: `~/Workspaces-no-src.code-workspace`

```json
{
  "folders": [
    { "path": "bin", "name": "scripts" },
    { "path": "Documents", "name": "Documents" },
    { "path": "My Drive", "name": "gdrive" },
    { "path": "My Drive/LP SCC Financial", "name": "lpscc" },
    { "path": "Documents/HoltzDotOrg/Thoughts/wiki", "name": "wiki" }
  ],
  "settings": {
    "git.autoRepositoryDetection": "openEditors"
  }
}
```

If `LP SCC Financial` is not mounted on a given laptop, remove that folder entry from the local copy.

## Operating Rules (Carry Forward)

- Always push every repo to GitHub (no local-only history).
- Drive-hosted working trees use separate git dirs under `~/gitdirs/*`.
- `.git` pointer files are expected to break across usernames; fix by rewriting the pointer.
- Treat Drive and laptops as caches; GitHub is the durable source of truth.

## Execution Order

Do this in order:

1. Phase 1 pointer repair for `~/My Drive`.
2. Phase 2 history import from `~/Documents` into `~/My Drive`.
3. Validate history on representative files.
4. Phase 3 cleanup commit in `~/Documents`.
5. Build/update `~/Workspaces-no-src.code-workspace`.

Last updated: 2026.05.02
