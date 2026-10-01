"""Minimal SQLite persistence layer for the Event Registration System."""

import os
import sqlite3

from models import validate_email, validate_name

DB_PATH = os.path.join(os.path.dirname(__file__), "event_registration.db")

SEED_EVENTS = [
    ("Web Development Workshop", "2026-10-15", 3),
    ("AI & Machine Learning Meetup", "2026-10-22", 2),
    ("Startup Pitch Night", "2026-11-05", 4),
]


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            capacity INTEGER NOT NULL
        )"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL REFERENCES events(id),
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            UNIQUE(event_id, email COLLATE NOCASE)
        )"""
    )
    count = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    if count == 0:
        conn.executemany(
            "INSERT INTO events (title, date, capacity) VALUES (?, ?, ?)",
            SEED_EVENTS,
        )
        conn.commit()
    conn.close()


def get_events():
    conn = get_connection()
    events = conn.execute("SELECT * FROM events ORDER BY date").fetchall()

    result = []
    for event in events:
        registered = conn.execute(
            "SELECT name, email FROM registrations WHERE event_id = ?",
            (event["id"],),
        ).fetchall()
        result.append(
            {
                "id": event["id"],
                "title": event["title"],
                "date": event["date"],
                "capacity": event["capacity"],
                "registered": [dict(r) for r in registered],
                "is_full": len(registered) >= event["capacity"],
            }
        )

    conn.close()
    return result


def register_participant(event_id, name, email):
    """Validates and persists a registration. Returns (success, message)."""
    if not validate_name(name):
        return False, "Please enter a valid name (at least 2 characters)."
    if not validate_email(email):
        return False, "Please enter a valid email address."
    if event_id is None:
        return False, "Please select an event."

    conn = get_connection()
    event = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
    if event is None:
        conn.close()
        return False, "Please select an event."

    registered_count = conn.execute(
        "SELECT COUNT(*) FROM registrations WHERE event_id = ?", (event_id,)
    ).fetchone()[0]
    if registered_count >= event["capacity"]:
        conn.close()
        return False, "This event is already full."

    try:
        conn.execute(
            "INSERT INTO registrations (event_id, name, email) VALUES (?, ?, ?)",
            (event_id, name.strip(), email.strip()),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False, "This email is already registered for this event."

    conn.close()
    return True, f'{name.strip()} successfully registered for "{event["title"]}".'
