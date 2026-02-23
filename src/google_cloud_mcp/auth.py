import logging
import os
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

CREDENTIALS_PATH = Path(
    os.environ.get("GOOGLE_MCP_CREDENTIALS_PATH", "credentials.json")
)
TOKEN_PATH = Path(
    os.environ.get("GOOGLE_MCP_TOKEN_PATH", str(CREDENTIALS_PATH.parent / "token.json"))
)


def get_credentials() -> Credentials:
    creds = None

    logger.debug("Credentials path: %s (exists: %s)", CREDENTIALS_PATH, CREDENTIALS_PATH.exists())
    logger.debug("Token path: %s (exists: %s)", TOKEN_PATH, TOKEN_PATH.exists())

    if TOKEN_PATH.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
            logger.info("Loaded token from %s", TOKEN_PATH)
        except Exception:
            logger.exception("Failed to load token from %s", TOKEN_PATH)
            creds = None

    if creds and creds.expired and creds.refresh_token:
        try:
            logger.info("Token expired, refreshing...")
            creds.refresh(Request())
            logger.info("Token refreshed successfully")
        except Exception:
            logger.exception("Token refresh failed")
            creds = None

    if not creds or not creds.valid:
        if not CREDENTIALS_PATH.exists():
            raise FileNotFoundError(
                f"Credentials file not found: {CREDENTIALS_PATH.resolve()}. "
                f"Set GOOGLE_MCP_CREDENTIALS_PATH to the correct path."
            )

        if not sys.stdin.isatty():
            raise RuntimeError(
                "OAuth browser flow required but running in non-interactive mode. "
                "Run 'uv run google-cloud-mcp' in a terminal first to complete the OAuth flow "
                "and generate a token.json."
            )

        logger.info("Starting OAuth browser flow...")
        flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
        creds = flow.run_local_server(port=0)
        logger.info("OAuth flow completed")

    TOKEN_PATH.write_text(creds.to_json())
    logger.debug("Token saved to %s", TOKEN_PATH)
    return creds


def get_calendar_service():
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)
    logger.info("Calendar service built successfully")
    return service
