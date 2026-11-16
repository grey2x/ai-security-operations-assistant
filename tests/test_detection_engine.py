
from pathlib import Path

from app.services.log_parser import parse_authentication_logs
from app.services.detection_engine import detect_repeated_failed_logins


SAMPLE_FILE = (
    Path(__file__).parent.parent
    / "data"
    / "samples"
    / "authentication_events.json"
)


def test_detects_repeated_failed_logins():
    events = parse_authentication_logs(SAMPLE_FILE)

    alerts = detect_repeated_failed_logins(events)

    assert len(alerts) == 1
    assert alerts[0]["source_ip"] == "192.0.2.15"
    assert alerts[0]["failed_attempts"] == 5
    assert alerts[0]["severity"] == "high"


def test_does_not_alert_below_threshold():
    events = parse_authentication_logs(SAMPLE_FILE)

    alerts = detect_repeated_failed_logins(events[:4])

    assert alerts == []


def test_successful_logins_do_not_trigger_alerts():
    events = parse_authentication_logs(SAMPLE_FILE)

    successful_events = [
        event for event in events if event["event_id"] == 4624
    ]

    alerts = detect_repeated_failed_logins(successful_events)

    assert alerts == []
