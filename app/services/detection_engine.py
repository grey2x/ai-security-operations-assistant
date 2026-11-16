
from collections import defaultdict
from datetime import timedelta


def detect_repeated_failed_logins(
    events,
    threshold=5,
    window_minutes=5
):
    """Detect repeated failed logins from the same source IP."""

    failed_logins = defaultdict(list)

    # Group failed login events by source IP.
    for event in events:
        if event["event_id"] == 4625:
            failed_logins[event["source_ip"]].append(event)

    alerts = []

    # Analyse each source IP separately.
    for source_ip, attempts in failed_logins.items():
        attempts.sort(key=lambda event: event["timestamp"])

        left = 0
        best_window = []

        # Find the largest group of attempts within the time window.
        for right in range(len(attempts)):
            while (
                attempts[right]["timestamp"] - attempts[left]["timestamp"]
                > timedelta(minutes=window_minutes)
            ):
                left += 1

            current_window = attempts[left:right + 1]

            if len(current_window) > len(best_window):
                best_window = current_window

        # Generate an alert if the threshold is reached.
        if len(best_window) >= threshold:
            alerts.append({
                "rule_id": "AUTH-001",
                "title": "Repeated failed login attempts",
                "severity": "high",
                "source_ip": source_ip,
                "failed_attempts": len(best_window),
                "threshold": threshold,
                "window_minutes": window_minutes,
                "usernames": sorted({
                    event["username"] for event in best_window
                }),
                "first_seen": best_window[0]["timestamp"].isoformat(),
                "last_seen": best_window[-1]["timestamp"].isoformat(),
            })

    return alerts
