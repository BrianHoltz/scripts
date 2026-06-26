---
name: ftm
description: "Use this skill whenever the user asks you to do anything in Family Tree Maker — navigating to a person, editing facts, deleting facts, adding sources, or any other operation in the app. Triggers include: 'Family Tree Maker', 'FTM', 'my tree', 'ancestor', 'genealogy app', or any mention of a specific person in the family tree."
---

# Family Tree Maker Skill

## Environment

- This skill is for **Claude Desktop** (computer-use via screenshot + mouse/keyboard).
- The app is **"Family Tree Maker 2019"** on this Mac. Open it via Spotlight or the Dock if not already running.
- The tree file in use is **Holtz Lusin.ftm** — it should already be open. If not, open it from File → Recent.
- Changes are auto-saved; no explicit save step is needed.

---

## Navigating to a Person

- Open the **People** workspace (left sidebar or View menu).
- In the **Find** box (top of the index panel), type the **last name only** — full names do not filter reliably. Example: type `Hermsen`, not `Bernard Hermsen`.
- Press Enter; use the forward/back arrows to step through matches.
- Click the person's name in the index list to select them.
- Switch to the **Person** tab (top of main panel) to view and edit facts.

---

## Working with Facts

### Viewing facts
On the **Person** tab, facts appear in the "Individual & Shared Facts" table with columns: Fact | Date | Place/Description.

### Editing an existing fact value
1. Navigate to the person → Person tab.
2. Click the fact row to select it.
3. Edit the value directly in the detail panel on the right (Description field for custom events, or the standard field for built-in facts).

### Adding a new fact
1. Click **Add Fact** (bottom of the facts table, or right-click → Add Fact).
2. Choose the fact type from the list, or choose **Event** for a custom type.
3. Fill in the value and (for custom events) the Type field.

### Deleting a fact
1. Click the fact row to select it (highlights blue).
2. Right-click → **Delete Fact**.
3. Confirm if prompted.
4. Verify the correct row was removed — after deletion, selection moves to the next row automatically.

---

## Native Language Facts (for 2324 language task)

### How FTM stores Native Language
Native Language appears as its own labeled row in the facts table — the Fact column reads **"Native Language"** and the Place/Description column holds the value (e.g. `German`, `English`, `German, English`).

### Setting or updating a Native Language value
1. If a Native Language row already exists: click it, edit the Description value in the right panel.
2. If none exists: click **Add Fact** (or the `+` button) → select **Native Language** from the fact type list → enter the language value in the Description field.
3. Never create two separate Native Language rows for one person — use a single comma-separated value like `German, English`.

### Data hygiene — persons with duplicate/conflicting rows
These two people have multiple Native Language rows that must be consolidated:
- **Maria Anna Pasker**: has both `German` and `English` rows → delete both, add one `German, English` row.
- **Rose Recker**: has two duplicate `German` rows → delete both, add one `German, English` row.

### Mary Emma Stuhr — skip
Leave Mary Emma Stuhr with **no Native Language fact**. Do not add one. Research is pending.

---

## Tips & Gotchas

- The "Preferred" label marks the canonical name/fact used for display.
- The person panel (right side) shows a FamilySearch ID (e.g. `K8B6-Z6D`) useful for cross-referencing.
- After any edit, take a screenshot to confirm the value saved correctly before moving to the next person.
