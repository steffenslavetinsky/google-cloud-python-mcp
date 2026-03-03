# /meeting-notes — Create Meeting Notes in Obsidian from Google Calendar

Create or open an Obsidian meeting note pre-filled with attendees and agenda from a Google Calendar event.

## Arguments

`$ARGUMENTS` is an optional date string (e.g., "tomorrow", "2026-02-20", "next monday"). Default: today.

## Instructions

### Step 1: Determine the date

Parse `$ARGUMENTS` to get the target date. If empty or unrecognizable, use today's date. Use `date` to resolve relative dates. Format as `YYYY-MM-DD`.

### Step 2: List events for that date

Use the Google Calendar MCP tools to list events for the target date. If no Google Calendar MCP tools are available, tell the user to set up the Google Calendar MCP server first and stop.

### Step 3: Let the user pick an event

Present events in a numbered list with time and title:

```
Events for 2026-02-18:
1. 09:00 - 09:30  Daily Standup
2. 10:00 - 11:00  Project Kickoff
3. 14:00 - 15:00  1on1 Alice <> Bob
```

Ask the user to pick one (by number). If there is only one event, confirm it with the user before proceeding.

### Step 4: Get event details

Fetch the selected event's full details:
- **Attendees**: list of names and email addresses
- **Description/body**: the invite text (if any)
- **Title**: the event summary

### Step 5: Determine file path and check for existing note

Meeting notes path: `Meetings/YYYY-MM/YYYY-MM-DD Title.md`

Example: `Meetings/2026-02/2026-02-18 Project Kickoff.md`

**Check for existing notes:**

1. Check if a file already exists at the exact expected path.
2. Also glob for `YYYY-MM-DD*` in the same directory to catch notes with slightly different titles.

**If a note already exists:**
- Tell the user: "A note already exists for this meeting: {path}"
- Read the existing file and proceed directly to **Step 7** (work on the note).
- Do NOT overwrite or recreate the note.

**If no note exists:**
- Create the parent directory if it doesn't exist (`mkdir -p`).
- Proceed to **Step 6** to write a new note.

### Step 6: Write the note

Use this template:

```markdown
---
tags:
---
# Meeting Notes - YYYY-MM-DD

**Attendees:**

- Attendee 1
- Attendee 2

## Agenda
**Purpose**: {event title}

1.
2.
3.

## Preparation

{invite description/body text here, or leave empty if none}

## Notes
-

## Action Items
- [ ]
```

After writing the note, tell the user:
- The file path that was created
- The attendees

Then proceed to **Step 7**.

### Step 7: Work on the note

Ask the user what they'd like to do with the note:

- **Add/edit agenda items** — user dictates agenda points, update the Agenda section
- **Add preparation notes** — user provides prep content, update the Preparation section
- **Add meeting notes** — user dictates notes, append to the Notes section
- **Add action items** — user provides action items, append as `- [ ] ...` to the Action Items section
- **Done** — stop

When editing an existing note, **always preserve existing content** — append to or update sections, never clear them unless the user explicitly asks.

After completing each edit, read back a short confirmation of what was changed and ask again what they'd like to do next. Loop until the user picks "Done" or indicates they're finished.

## Allowed tools

```
Bash(date *), Bash(ls *), Bash(mkdir *), Read, Write, Edit, Glob, Grep, AskUserQuestion
```

Plus all Google Calendar MCP tools (e.g., `mcp__google-calendar__*`).
