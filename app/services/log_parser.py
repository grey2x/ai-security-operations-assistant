
import json
from datetime import datetime
from pathlib import Path


REQUIRED_FIELDS = {
    "event_id",
    "timestamp",
    "computer",
    "username",
    "source_ip",
    "logon_type",
    "status",
}


def parse_authentication_logs(file_path):
    """Load and validate authentication events from a JSON file."""

    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        events = json.load(file)

    if not isinstance(events, list):
        raise ValueError("The log file must contain a JSON list.")

    parsed_events = []

    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise ValueError(f"Event {index} must be a JSON object.")

        missing_fields = REQUIRED_FIELDS - event.keys()

        if missing_fields:
            raise ValueError(
                f"Event {index} is missing fields: {', '.join(sorted(missing_fields))}"
            )

        parsed_event = event.copy()

        parsed_event["event_id"] = int(event["event_id"])
        parsed_event["timestamp"] = datetime.fromisoformat(
            event["timestamp"]
        )

        parsed_events.append(parsed_event)

    return parsed_events
