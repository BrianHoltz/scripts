# GitScheme.md — Repo Organization Plan

## The Plan (TL;DR)

- Every repo has a GitHub remote. No local-only history, ever again.
- Drive holds **working trees only** — no git object stores inside Drive.
- Working trees that live in Drive use `--separate-git-dir` so Drive never touches `.git` objects.
- Separate git dirs live at `~/gitdirs/<name>/` (outside Drive, outside any synced folder).
- `~/My Drive/Workspaces-template.code-workspace` (relative paths) is the canonical all-laptops template; copy to `~/Workspaces.code-workspace` on each laptop and remove folders not present on that machine.
- `~/Documents/` is a private repo (in-tree `.git`, like `~/bin/`); must have a GitHub remote so history isn't lost again.

---

## Repo Census


| Repo Name   | Working tree                             | Git dir                 | Remote                  | State                                     |
| ------------- | ------------------------------------------ | ------------------------- | ------------------------- | ------------------------------------------- |
| `scripts`   | `~/bin/`                                 | `~/bin/.git/` (in-tree) | GitHub public           | ✅ cloned on both laptops                 |
| `gdrive`    | `~/My Drive/`                            | `~/gitdirs/gdrive/`     | GitHub private (create) | 🔲 needs init                             |
| `lpscc`     | shared GDrive "LP SCC Financial"         | `~/gitdirs/lpscc/`      | GitHub private (create) | ⚠️ history lost; needs re-init          |
| `Documents` | `~/Documents/`                           | `~/Documents/.git/` (in-tree) | GitHub private (create) | 🔲 needs init; lesson: always push to GitHub |
| `src/*`     | `~/src/<name>/`                          | in-tree                 | GitHub public           | 🔲 audit remotes                          |
| `wiki`      | `~/Documents/HoltzDotOrg/Thoughts/wiki/` | in-tree                 | GitHub public           | ✅                                        |

## North Star

```
~/
  bin/                  ← repo (in-tree .git), GitHub remote
  gitdirs/              ← separate git dirs for Drive-hosted working trees (GIT_DIR)
    personal-drive/
    lpscc/
  My Drive/             ← working tree; .git FILE points to ~/gitdirs/personal-drive
    .git                ← one-line pointer: "gitdir: ~/gitdirs/personal-drive"
    Workspaces-template.code-workspace  ← template; copy to ~/Workspaces.code-workspace per laptop
    ...files...
  Documents/            ← private repo (in-tree .git), GitHub remote
    HoltzDotOrg/        ← future public nested repo; parent won't track its contents
  src/
    <project>/          ← normal repos, GitHub remotes
```

Drive syncs: working files + tiny `.git` pointer files. Never syncs object stores.

---

## Incremental Migration

Step 1 — **`~/bin/`**: already done. ✅

Step 2 — **`~/My Drive/`** ← **do this next**:

```bash
mkdir -p ~/gitdirs
git init --separate-git-dir="$HOME/gitdirs/gdrive" "$HOME/My Drive"
cd ~/My\ Drive

# Whitelist only FamilyDocuments/Heather/2026 NYC for initial commit
# (must un-ignore each parent dir so git can descend into them)
cat > .gitignore << 'EOF'
# ignore everything
*
# un-ignore the path to 2026 NYC and its contents
!FamilyDocuments/
!FamilyDocuments/Heather/
!FamilyDocuments/Heather/2026 NYC/
!FamilyDocuments/Heather/2026 NYC/**
# and the standard git files
!.gitignore
EOF

git add "FamilyDocuments/Heather/2026 NYC" .gitignore
git commit -m "chore: initial commit — FamilyDocuments/Heather/2026 NYC"
gh repo create gdrive --private --source=. --remote=origin --push
```

Step 3 — **`Workspaces-template.code-workspace`** (do alongside step 2):

Create the template in Drive (tracks all possible folders across all laptops):

```bash
cat > "$HOME/My Drive/Workspaces-template.code-workspace" << 'EOF'
{
  // TEMPLATE — do not open this file directly as a workspace.
  // On each laptop:
  //   cp "$HOME/My Drive/Workspaces-template.code-workspace" "$HOME/Workspaces.code-workspace"
  // Then edit ~/Workspaces.code-workspace to remove folders not present on that machine.
  // ~/Workspaces.code-workspace is local-only (not in Drive, not in git).
  //
  // Laptop notes:
  //   work laptop:     keep My Drive + bin; remove Documents (not set up here)
  //   personal laptop: keep My Drive + bin + Documents
  "folders": [
    { "path": "My Drive",   "name": "My Drive" },  // ~ relative; adjust if Drive mounts elsewhere
    { "path": "bin",        "name": "bin" },
    { "path": "Documents",  "name": "Documents" }   // personal laptop only
  ]
}
EOF
```

Then create your local copy for this laptop (work — omit Documents):

```bash
cp "$HOME/My Drive/Workspaces-template.code-workspace" "$HOME/Workspaces.code-workspace"
# then edit ~/Workspaces.code-workspace: remove the Documents entry
```

Step 4 — **`~/Documents/`** (simple — no separate-git-dir needed):

```bash
cd ~/Documents
git init
# add .gitignore (see below), then:
git add -A && git commit -m "chore: initial commit"
gh repo create documents --private --source=. --remote=origin --push
```

`.gitignore` starting point — whitelist approach:

```
# ignore everything by default
*
# then un-ignore what matters
!*.md
!*.txt
!*.json
!*.yaml
!*.yml
!*.py
!*.sh
!.gitignore
!*/
# silence nested repos (e.g. HoltzDotOrg when it gets its own remote)
/HoltzDotOrg/
```

Confirm whitelist with user before first commit.

Step 5 — **LPSCC** (when you have access to the shared folder again):

```bash
git init --separate-git-dir="$HOME/gitdirs/lpscc" "/path/to/LP SCC Financial"
# commit, push to private GitHub repo
```

Step 6 — **`~/src/*` audit**: for each, verify `git remote -v` shows a GitHub remote. Add one if missing.

---

## Cross-Laptop Protocol

**Normal repos** (`~/bin/`, `~/src/*`): push on laptop A, pull on laptop B. Independent, no coordination.

**Drive-hosted working trees** (`~/My Drive/`, LPSCC): baton handoff:

1. Commit + push to GitHub
2. Wait for Drive to finish syncing
3. On new laptop: recreate `.git` pointer file (stale path after sync), then `git pull`

Pointer file rebuild on new laptop:

```bash
mkdir -p ~/gitdirs
git clone --bare git@github.com:BrianHoltz/gdrive.git ~/gitdirs/gdrive
echo "gitdir: $HOME/gitdirs/gdrive" > "$HOME/My Drive/.git"
git --git-dir="$HOME/gitdirs/gdrive" --work-tree="$HOME/My Drive" pull
```

---

## Key Decisions

- **No `.git` folders inside Drive** — eliminates corruption risk entirely.
- **`~/Documents/` is a private repo** — the old instance was lost because it had no remote, not because the pattern is bad. Always push to GitHub before the laptop dies.
- **Public-inside-private nesting is safe** — when `~/Documents/HoltzDotOrg/` has its own `.git`, the parent repo never indexes its contents; the two remotes are fully independent. Add a `.gitignore` entry in the parent to silence the "untracked directory" noise.
- **`~/gitdirs/` is ephemeral** — if lost, `git clone --bare` from GitHub reconstructs it in minutes.
- **GitHub is the only durable store** — Drive, local disk, laptops are all caches.

---

## Agent Handoff Context

**As of 2026.04.25** — plan designed, nothing executed yet beyond `~/bin/`.

### Environment

- **Work laptop**: macOS, username `b0h0166`, hostname unknown
- **Personal laptop**: macOS, different username (unknown) — same `~/bin/` repo via GitHub
- **Google Drive**: mounted at `~/Library/CloudStorage/GoogleDrive-brianholtz1965@gmail.com/My Drive/`; also accessible as `~/My Drive/` (symlink/alias). Gmail: `brianholtz1965@gmail.com`.
- **GitHub**: personal account `BrianHoltz` (public). Use `gh` CLI — already authenticated.
- **`~/bin/`**: public GitHub repo `BrianHoltz/scripts`. Do NOT put private paths or credentials here.
- **`~/gitdirs/`**: does not exist yet — `mkdir -p ~/gitdirs` is the first command of step 2.
- **`~/My Drive/`**: not a git repo yet. No `.git` file or folder present.
- **`~/My Drive/Workspaces.code-workspace`**: does not exist yet.

### What's in ~/My Drive/ worth tracking

User hasn't specified a final whitelist yet. Known high-value files (from `~/.claude/CLAUDE.md`):

- `FamilyDocuments/FamilyEncyclopedia.md` — authoritative family reference
- `FamilyDocuments/Genealogy/FamilyTree.md` — tree structure
- `README.md` — exists at Drive root

Other top-level items visible (mostly Google Workspace files that git can't usefully diff, skip these):
`.gdoc`, `.gsheet`, `.gdraw`, `.gprj` — these are just stubs/shortcuts, not real content; exclude from git.

Suggested `.gitignore` strategy: whitelist by extension — track `*.md`, `*.txt`, `*.json`, `*.yaml`, `*.py`, etc.; ignore `*.gdoc`, `*.gsheet`, `*.gdraw`, `*.gprj`, `*.mp3`, binary media. **Ask user to confirm whitelist before first commit.**

### ~/src/ repos found

```
~/src/GHE-Scripts, LogExample, QualityServiceHiveDump, ai-registry-marketplace,
apache-tomcat-7.0.96, bvconfig, centaurus-core, centaurus-managed-dag-resources,
docker, examples, facet-creation-service, gcp_project_definitions,
genai-shoppable-lists, idea, linked-fee-spark, mms-config, old, pm-copilot,
product-canonical-lib, product-group-common  (+ more)
```

Step 5 (remote audit) not started. Run `for d in ~/src/*/; do echo "$d: $(git -C "$d" remote -v 2>/dev/null | head -1 || echo NO REMOTE)"; done`.

### LPSCC shared folder

Actual path unknown — user needs to locate it. It will be somewhere under
`~/Library/CloudStorage/GoogleDrive-brianholtz1965@gmail.com/` in a shared drives subfolder,
or under `~/My Drive/` if it was added as a shortcut. History is lost (never pushed to GitHub).
Re-init from scratch when the user has access.

### Write rules for this doc

This file (`~/bin/docs/GitScheme.md`) is a git-tracked markdown file. Use `fhold` before editing:

```bash
~/bin/fhold status ~/bin/docs/GitScheme.md
~/bin/fhold review register ~/bin/docs/GitScheme.md --agent <your-agent-name>
# ... edit with IDE Edit tool (inode-preserving) ...
~/bin/fhold review release ~/bin/docs/GitScheme.md --agent <your-agent-name>
```

Last updated: 2026.04.25 (Documents repo reinstated; public-inside-private nesting documented)
