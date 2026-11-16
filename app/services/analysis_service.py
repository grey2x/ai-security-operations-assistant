
from app.services.log_parser import parse_authentication_logs
from app.services.detection_engine import detect_repeated_failed_logins


def analyse_log_file(file_path):
    """Load authentication logs and analyse them for suspicious activity."""

    events = parse_authentication_logs(file_path)

    alerts = detect_repeated_failed_logins(events)

    return {
        "total_events": len(events),
        "total_alerts": len(alerts),
        "events": events,
        "alerts": alerts,
    }
