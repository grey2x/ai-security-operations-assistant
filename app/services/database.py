
import sqlite3
import json
from pathlib import Path


DATABASE_PATH = (
    Path(__file__).parent.parent.parent
    / "data"
    / "incidents.db"
)


def init_db():
    """Create the incidents database and table if they don't exist."""

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_id TEXT NOT NULL,
                title TEXT NOT NULL,
                severity TEXT NOT NULL,
                source_ip TEXT NOT NULL,
                failed_attempts INTEGER NOT NULL,
                threshold INTEGER NOT NULL,
                window_minutes INTEGER NOT NULL,
                usernames TEXT NOT NULL,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_incident(alert):
    """Save a detected security alert as an incident."""

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("""
            INSERT INTO incidents (
                rule_id, title, severity, source_ip,
                failed_attempts, threshold, window_minutes,
                usernames, first_seen, last_seen
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            alert["rule_id"],
            alert["title"],
            alert["severity"],
            alert["source_ip"],
            alert["failed_attempts"],
            alert["threshold"],
            alert["window_minutes"],
            json.dumps(alert["usernames"]),
            alert["first_seen"],
            alert["last_seen"]
        ))


def get_incidents():
    """Retrieve saved incidents from the database."""

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            "SELECT * FROM incidents ORDER BY id DESC"
        ).fetchall()

    incidents = []

    for row in rows:
        incident = dict(row)
        incident["usernames"] = json.loads(incident["usernames"])
        incidents.append(incident)

    return incidents


def save_incident(alert):
    """Save a detected alert only if it doesn't already exist."""

    with sqlite3.connect(DATABASE_PATH) as connection:

        existing = connection.execute("""
            SELECT id FROM incidents
            WHERE rule_id = ?
            AND source_ip = ?
            AND first_seen = ?
            AND last_seen = ?
        """, (
            alert["rule_id"],
            alert["source_ip"],
            alert["first_seen"],
            alert["last_seen"]
        )).fetchone()

        if existing:
            return

        connection.execute("""
            INSERT INTO incidents (
                rule_id, title, severity, source_ip,
                failed_attempts, threshold, window_minutes,
                usernames, first_seen, last_seen
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            alert["rule_id"],
            alert["title"],
            alert["severity"],
            alert["source_ip"],
            alert["failed_attempts"],
            alert["threshold"],
            alert["window_minutes"],
            json.dumps(alert["usernames"]),
            alert["first_seen"],
            alert["last_seen"]
        ))
