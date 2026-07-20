# Recovery RCA — July 2026 Data Loss Incident

## Executive Summary: 102 Files Deleted by HoltzBot Mirror Agent

**Date:** July 11, 2026, 16:37 PDT  
**Agent:** Copilot (gpt-5.4-mini)  
**Commit:** `eed4187` ("Keep only HoltzBot.md in HoltzBot folder")  
**Scope:** 102 files deleted from working tree (exist only in git history)  
**Severity:** CRITICAL — Files also deleted from Google Drive via sync

**Backup created:** 2026-07-15 23:53 PDT (`~/tmp/gdrive.20260715.tar`, 6.7G, 5,257 files verified)

## Timeline of Events

### July 11, 2026 — 12:18-12:41 PDT: Mirroring Phase

Copilot executes mirroring to populate HoltzBot folder for ChatGPT project:

| Time | Commit | Action | Files Added |
|------|--------|--------|-------------|
| 12:18:04 | 4ab2e98 | Move HoltzBot.md to HoltzBot/ | 1 |
| 12:24:36 | **7863264** | **Mirror 9 Log files + PHWD.md** | **11** |
| 12:28:20 | 7520f13 | Mirror Kay Holtz books + Financial | 3 |
| 12:34:45 | 0e31e79 | Mirror 11 wiki files | 11 |

**Status:** All files successfully committed to git, present on disk. ✅

### July 11, 2026 — 16:35 PDT: Bundle Publication

Commit `3914c0b`: "Publish HoltzBot compilation bundles"
- Finalizes all mirrored files in HoltzBot folder
- **All 18 mirrored files confirmed in working tree** ✅

### July 11, 2026 — 16:37 PDT: **THE DELETION** 🚨

Commit `eed4187`: "Keep only HoltzBot.md in HoltzBot folder"  
**Author:** Copilot (gpt-5.4-mini)

**Deleted files:**
```
My Drive/HoltzBot/MedicalHistory.md              (930 lines)
My Drive/HoltzBot/FamilyEncyclopedia.md          (558 lines)
My Drive/HoltzBot/FamilyLogs.md                  (5736 lines)
My Drive/HoltzBot/FamilyTree.md                  (1856 lines)
My Drive/HoltzBot/HumanKnowledgeWiki.md          (1785 lines)
My Drive/HoltzBot/FamilyHistory.md               (5262 lines)
My Drive/HoltzBot/PHWD.md                        (505 lines)
(+ 11 wiki file deletes)
```

**Decision logic:**
- "Keep only HoltzBot.md in HoltzBot folder" (reasonable)
- Original files should still exist in FamilyDocuments (WRONG)

## Root Cause Analysis

### Primary Issue: Agent Assumption Without Verification

Copilot did NOT verify that original files existed on disk before deleting the mirrors.

**What actually happened:**
1. Original files in `My Drive/FamilyDocuments/` were ALREADY missing from disk
2. Copilot deleted the mirrors, exposing the underlying problem
3. Google Drive sync saw files missing from disk and auto-deleted from cloud
4. Result: Both original + mirror files gone from disk AND Google Drive

**Files disappeared BEFORE mirror deletion.** The originals were already gone when eed4187 ran.

### Secondary Issue: Google Drive Sync is Not a Backup

**Critical misunderstanding:** Google Drive sync is bidirectional mirror, not backup.

**How sync works:**
- Files on Mac → upload to Google Drive
- Files deleted from Mac → DELETE from Google Drive (automatic, instant)
- No recovery window, no trash, no "undo"

**When the originals disappeared from disk** (unknown cause, unknown date), Google Drive sync propagated the deletion globally. The deletion appeared on:
- All other Mac devices (if any)
- Google Drive web interface
- Google Drive mobile apps
- Any other synced devices

**This is NOT backup.** This is live synchronization. If the local source is deleted, the cloud copy is deleted automatically.

## The 102 Missing Files

### Breakdown

| Category | Count | Examples |
|----------|-------|----------|
| FamilyDocuments/Logs | 17 | family logs and journals |
| Personal documents | 40 | agreements, lease docs, income verification |
| HoltzBot mirrors | 18 | Copies of logs, genealogy, wiki |
| Genealogy/FamilyTree | 13 | tree data, variants, cleanup logs |
| FamilyEncyclopedia | 6 | encyclopedia sources and support files |
| Other | 8 | root files and misc references |

**Most critical:** the main family journal log — a multi-decade record

## Agent Behavior Analysis

### What Copilot Did (Intentionally)

1. ✅ Mirrored 18+ files to HoltzBot folder (reasonable)
2. ✅ Documented the plan (reasonable)
3. ❌ Deleted mirrors from HoltzBot folder without verification (risky)
4. ❌ Assumed originals were safe (unverified assumption)
5. ❌ Committed deletion automatically (no user review)

### What Copilot Didn't Do

❌ Check if originals still exist on disk  
❌ Pause and ask user before deleting  
❌ Examine git history to verify originals  
❌ Create a recovery branch or tag  
❌ Document why mirrors were temporary  

### System Vulnerabilities

❌ No pre-deletion verification required  
❌ No user review for large file deletions  
❌ Automatic git commits without pause  
❌ No monitoring of file deletions  
❌ No forced backups of recently-deleted files  

## Recovery Status

### 102 Files in Git History ✅

All files preserved in git via commits 7863264, 7520f13, 0e31e79, eed4187, and earlier historical commits.

**Earliest reference to Log Family.txt:** 2004 (git history spans 22 years)

### Physical Backup

Tarball created 2026-07-15 23:53 PDT:
- `~/tmp/gdrive.20260715.tar` (6.7G)
- 5,257 files verified and readable
- Created with GNU tar for compatibility

### Recovery Procedure

Once gdrive repo is merged into home monorepo:

```bash
# Restore all 102 missing files from git
git restore My\ Drive/FamilyDocuments/*
git restore My\ Drive/HoltzBot/*
git restore My\ Drive/README.md
git restore My\ Drive/.gitignore
git restore My\ Drive/Workspaces-template.code-workspace

# Verify files appeared on disk
find My\ Drive/FamilyDocuments -type f | wc -l
# Should show 102+ files

# Push to GitHub
git push origin main

# Google Drive sync will detect new files and upload automatically
# No manual intervention required
```

## Lessons Learned

### 1. Mirror Deletion Requires Redundancy Verification

**Before deleting any mirrored or copied files:**
- Verify originals exist on disk
- Check git history for both copies
- Confirm which is the "source of truth"

**Implementation:** Agent should always check:
```bash
git ls-files -- 'My Drive/FamilyDocuments/Logs/*'
# Before deleting copies in HoltzBot/
```

### 2. Google Drive Sync is Not Backup

**Real situation:**
- Sync mirrors current state, not archive
- Deletion on Mac → deletion on cloud (automatic)
- No "cloud backup" if local deletion occurs
- Recovery window: minutes at most

**Implication:** Never rely on Google Drive as backup for files you delete from your Mac.

### 3. Agent Deletion Needs Friction

**Current problem:**
- Agent writes files
- Agent commits to git
- Agent deletes files
- Agent commits deletion
- Result: Permanently gone (except git history)

**Better approach:**
- Agent requests user confirmation for deletions >100KB
- Dry-run showing affected files before deletion
- Require user review of git diff before commit
- Preserve deleted files in git (mark "deprecated" instead of full delete)

### 4. Mirrors Should Be Explicitly Documented

**What went wrong:**
- HoltzBot mirror purpose was unclear
- Temporary copies for ChatGPT project?
- Persistent redundancy?
- Unclear expiration date

**Solution:** Clear notation in git commit message or code:
```
# Mirror these files for ChatGPT HoltzBot project
# Source of truth: My Drive/FamilyDocuments/Logs/Log Family.txt
# Keep synced when either copy changes
```

## Detection Timeline

| Date | Event | Detection |
|------|-------|-----------|
| 2026-07-11 16:37 | Copilot deletes HoltzBot mirrors | None |
| 2026-07-11 16:37 | Google Drive sync propagates | None |
| 2026-07-12 | User notices missing files in IDE | Manual discovery |
| 2026-07-12 | Backup script run (60 files listed) | Manual analysis |
| 2026-07-15 23:35 | Full audit performed | **Root cause identified** |
| 2026-07-15 23:53 | Tarball created | **102 files verified safe** |

**Detection delay:** 4 days (96+ hours)

During this time, all 102 files were only in git history. Had sync run on another device, the deletion could have propagated further.

## Preventing Future Incidents

### Tier 1: Agent Design

- Require user confirmation for deletions >100KB
- Pre-deletion dry-run showing affected files
- Never assume files are safe elsewhere
- Always verify preconditions before destructive operations

### Tier 2: System Design

- Monthly backups of critical FamilyDocuments to separate storage
- Monitor for unexpected file deletions (alert if >50 files in one commit)
- Separate "sync" mechanism from "backup" mechanism
- Never use sync as backup

### Tier 3: User Practices

- Understand that Google Drive sync mirrors, not backs up
- Create separate offline backups for critical files
- Review git diffs before approving deletion commits
- Maintain multiple independent copies for family data

## Status

✅ Root cause identified: Copilot deletion + assumption failure  
✅ 102 files confirmed in git history  
✅ 102 files confirmed in tarball backup  
✅ Recovery path clear and documented  
⏳ Files NOT yet restored to disk (pending gdrive merge)  

**Next phase:** Merge gdrive history into monorepo and restore files to working tree.
