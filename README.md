# Google Cloud MCP

MCP server for Google Calendar integration.

## Setup

### 1. Google Cloud credentials

Place your OAuth `credentials.json` from the Google Cloud Console in a known location.

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
