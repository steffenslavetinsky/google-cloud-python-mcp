# Google Cloud MCP

MCP server for Google Calendar integration.

## Setup

### 1. Google Cloud credentials

Create an OAuth `credentials.json` via the Google Cloud Console:

1. **Create a Google Cloud project** (if you don't have one) at [console.cloud.google.com](https://console.cloud.google.com)
2. **Enable the Google Calendar API** — use [this direct link](https://console.cloud.google.com/flows/enableapi?apiid=calendar-json.googleapis.com), select your project, and click **Enable**
3. **Configure the OAuth consent screen** at [Auth Branding](https://console.cloud.google.com/auth/branding):
   - Choose **External** for personal Gmail accounts (add yourself as a test user under **Audience**) or **Internal** for Google Workspace
   - Fill in app name, support email, and contact info
4. **Create OAuth credentials** at [Auth Clients](https://console.cloud.google.com/auth/clients):
   - Click **Create Client** → Application type **Desktop app** → **Create**
   - Click **Download JSON** and save the file as `credentials.json`

> **Note:** The `credentials.json` contains your Client ID and Secret — do not commit it to version control.

See the [Google Calendar API Python quickstart](https://developers.google.com/workspace/calendar/api/quickstart/python) for the full official guide.

Place the `credentials.json` in a known location.

### 2. Initial token generation

Run the server once interactively to complete the OAuth flow and generate `token.json`:

```bash
GOOGLE_MCP_CREDENTIALS_PATH=/path/to/credentials.json uv run google-cloud-mcp
```

This opens a browser for Google sign-in. After authorizing, a `token.json` is saved next to your credentials file.

### 3. Configure as MCP server

Add the following to your `.mcp.json`:

```json
{
  "mcpServers": {
    "google-calendar": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/google-cloud-python-mcp", "google-cloud-mcp"],
      "env": {
        "GOOGLE_MCP_CREDENTIALS_PATH": "/path/to/credentials.json"
      }
    }
  }
}
```

The token path defaults to `token.json` next to the credentials file. Override with `GOOGLE_MCP_TOKEN_PATH` if needed.

## Tools

- **list_calendar_events** — List all events for a given date
- **get_calendar_event** — Get full details of a specific event by ID

## Example: Claude Code skill for Obsidian meeting notes

The [`examples/skills/meeting-notes/`](examples/skills/meeting-notes/) directory contains a Claude Code [skill](https://docs.anthropic.com/en/docs/claude-code/skills) that creates Obsidian meeting notes from Google Calendar events.

Usage: type `/meeting-notes` (or `/meeting-notes tomorrow`) in Claude Code. It lists your events, lets you pick one, and creates a pre-filled Obsidian note with attendees, agenda, and sections for notes and action items.

To use it, copy the skill into your Obsidian vault's `.claude/skills/` directory:

```
your-vault/
  .claude/
    skills/
      meeting-notes/
        SKILL.md
```
