import logging
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP

from google_cloud_mcp.auth import get_calendar_service

# Suppress Google client libraries from polluting stdout (breaks MCP stdio protocol)
logging.getLogger("googleapiclient.discovery_cache").setLevel(logging.ERROR)
logging.getLogger("googleapiclient").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

mcp = FastMCP("Google Calendar")


def _format_attendee(attendee: dict) -> str:
    name = attendee.get("displayName", "")
    email = attendee.get("email", "")
    status = attendee.get("responseStatus", "unknown")
    if name:
        return f"{name} <{email}> ({status})"
    return f"{email} ({status})"


def _format_event_summary(event: dict) -> str:
    start = event["start"].get("dateTime", event["start"].get("date", ""))
    end = event["end"].get("dateTime", event["end"].get("date", ""))
    title = event.get("summary", "(No title)")
    event_id = event.get("id", "")

    lines = [f"- {title}", f"  Start: {start}", f"  End: {end}", f"  ID: {event_id}"]

    attendees = event.get("attendees", [])
    if attendees:
        lines.append("  Attendees:")
        for a in attendees:
            lines.append(f"    - {_format_attendee(a)}")

    description = event.get("description")
    if description:
        lines.append(f"  Notes: {description}")

    return "\n".join(lines)


def _format_event_detail(event: dict) -> str:
    start = event["start"].get("dateTime", event["start"].get("date", ""))
    end = event["end"].get("dateTime", event["end"].get("date", ""))
    title = event.get("summary", "(No title)")

    lines = [
        f"Title: {title}",
        f"Start: {start}",
        f"End: {end}",
    ]

    location = event.get("location")
    if location:
        lines.append(f"Location: {location}")

    organizer = event.get("organizer", {})
    org_name = organizer.get("displayName", organizer.get("email", ""))
    if org_name:
        lines.append(f"Organizer: {org_name}")

    status = event.get("status")
    if status:
        lines.append(f"Status: {status}")

    attendees = event.get("attendees", [])
    if attendees:
        lines.append("Attendees:")
        for a in attendees:
            lines.append(f"  - {_format_attendee(a)}")

    description = event.get("description")
    if description:
        lines.append(f"\nNotes:\n{description}")

    html_link = event.get("htmlLink")
    if html_link:
        lines.append(f"\nLink: {html_link}")

    return "\n".join(lines)


@mcp.tool()
def list_calendar_events(date: str) -> str:
    """List all Google Calendar events for a specific day.

    Args:
        date: ISO date string, e.g. "2026-02-19"
    """
    logger.info("list_calendar_events called with date=%s", date)

    day = datetime.fromisoformat(date).date()
    time_min = datetime(day.year, day.month, day.day, tzinfo=timezone.utc).isoformat()
    time_max = datetime(
        day.year, day.month, day.day, 23, 59, 59, tzinfo=timezone.utc
    ).isoformat()

    try:
        service = get_calendar_service()
        result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
    except Exception:
        logger.exception("Failed to list calendar events for %s", date)
        raise

    events = result.get("items", [])
    logger.info("Found %d events for %s", len(events), date)

    if not events:
        return f"No events found for {date}."

    formatted = [f"Events for {date} ({len(events)} total):\n"]
    for event in events:
        formatted.append(_format_event_summary(event))

    return "\n\n".join(formatted)


@mcp.tool()
def get_calendar_event(event_id: str) -> str:
    """Get full details of a specific Google Calendar event.

    Args:
        event_id: The event ID (from list_calendar_events results)
    """
    logger.info("get_calendar_event called with event_id=%s", event_id)

    try:
        service = get_calendar_service()
        event = service.events().get(calendarId="primary", eventId=event_id).execute()
    except Exception:
        logger.exception("Failed to get calendar event %s", event_id)
        raise

    logger.info("Retrieved event: %s", event.get("summary", "(No title)"))
    return _format_event_detail(event)


def main():
    logger.info("Starting Google Calendar MCP server")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
