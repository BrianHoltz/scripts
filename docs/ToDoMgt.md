# ToDo Management — Pending Work Sources & Agent Capabilities

_Status: 2026.04.26 — initial exploration session._

## Pending Work Sources

### Apple Notes ✅ Full read/write confirmed

**Capabilities:**

- **Read:** find any note by title, search by keyword, list all note titles
- **Read:** read full text content of any note
- **Read:** identify checklist items and their checked/unchecked state
- **Edit:** reorder checklist items (e.g. move completed items to bottom)
- **Edit:** mark items done or undone
- **Edit:** create new notes, append or rewrite note body

**Access method:** Direct SQLite + protobuf — requires VS Code Full Disk Access.

**Setup required (one-time):** System Settings → Privacy & Security → Full Disk Access → add **Visual Studio Code**. Without this, all reads/writes fail with `authorization denied`.

**Implementation notes:**

- DB path: `~/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite`
- Note record: `ZICCLOUDSYNCINGOBJECT` — `ZISPINNED`, `ZTITLE`, `ZHASCHECKLIST`, `ZNOTEDATA` (FK)
- Note data: `ZICNOTEDATA.ZDATA` — gzip-compressed protobuf
- Protobuf structure: outer → field 2 (NoteData) → field 3 (TextData) → field 2 (text string UTF-8), field 5 repeated (attribute runs)
- Checklist items: attribute run field 2 (paragraph style) → field 1 = 103 means checklist item; field 5 (ChecklistItem) → field 2 = `isDone` (0/1), field 1 = UUID bytes
- All attribute runs use **Unicode code point counts** for length (not UTF-8 bytes)
- To edit: modify `ZDATA` + bump `ZMODIFICATIONDATE` on `ZICCLOUDSYNCINGOBJECT` to Apple epoch time (`time.time() - 978307200`)
- Must quit + reopen Notes for DB changes to take effect (`osascript -e 'tell application "Notes" to quit'`)
- Always backup DB before writes: `shutil.copy2(DB, "/tmp/NoteStore_backup_YYYYMMDD.sqlite")`
- AppleScript `body` property: readable without FDA, but **strips all checklist state** — useless for checked/unchecked

**Known limitations:**

- Encrypted notes (`ZISPASSWORDPROTECTED=1`): content is not readable
- Notes stored only in iCloud (`ZNEEDSTOBEFETCHEDFROMCLOUD=1`): ZDATA may be empty until synced locally
- Rich content (images, drawings, handwriting): present as attachment references, not modifiable via this method

---

### Outlook Tasks (Microsoft To Do)

**Capabilities:**

- **Read:** list all task lists and every task (title, due date, status, notes)
- **Read:** filter by status (not started, in progress, completed), due date, importance
- **Edit:** create tasks with title, due date, body, reminder
- **Edit:** mark complete, update due date, modify body
- **Edit:** move between lists, delete tasks

**Access method:** `msgraph` skill via MS Graph API — requires valid Microsoft 365 session.

---

### Slack: Later

### Outlook Email

### Pull Request Comments

### Jira

### Task Lists in Current Project Docs

### Outlook Calendar

---

## Personal

### Google Tasks

### Gmail

### Google Keep

### Google Calendar

### SMS

### Google Chat

### Discord

### YouTube Playlists

### Twitter Bookmarks

### LinkedIn Messages

---

## Both (Work & Personal)

### Browser Tabs

### Downloads Folder

### Desktop Files
