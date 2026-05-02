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
    { "path": "bin", "name": "scripts" },
    { "path": "Documents", "name": "Documents" },
    { "path": "My Drive", "name": "gdrive" },
    { "path": "Documents/HoltzDotOrg/Thoughts/wiki", "name": "wiki" }
  ],
  "settings": {
    "git.autoRepositoryDetection": "openEditors"
  }
}
```

Notes:
- Paths are relative to `$HOME`. VS Code resolves them from the workspace file location only when the file is at `~/`; otherwise use absolute paths.
- LPSCC omitted until the shared Drive folder path is confirmed on this laptop.
- `src/*` intentionally excluded per requirements.

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
