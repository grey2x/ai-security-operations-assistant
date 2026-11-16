
from pathlib import Path

from app.services.log_parser import parse_authentication_logs


SAMPLE_FILE = (
    Path(__file__).parent.parent
    / "data"
    / "samples"
    / "authentication_events.json"
)


def test_parse_authentication_logs():
    events = parse_authentication_logs(SAMPLE_FILE)

    assert len(events) == 6
    assert events[0]["event_id"] == 4625
    assert events[0]["username"] == "admin"
    assert events[0]["timestamp"].year == 2026


def test_timestamp_is_datetime():
    events = parse_authentication_logs(SAMPLE_FILE)

    assert events[0]["timestamp"].__class__.__name__ == "datetime"
