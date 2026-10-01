import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import db


def setup_function():
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    db.DB_PATH = tmp.name
    db.init_db()


def teardown_function():
    os.remove(db.DB_PATH)


def test_seed_events_are_created():
    events = db.get_events()
    assert len(events) == 3
    assert all(e["registered"] == [] for e in events)


def test_register_participant_success():
    event_id = db.get_events()[0]["id"]
    success, message = db.register_participant(event_id, "John Doe", "john@example.com")
    assert success is True
    assert "John Doe" in message
    assert len(db.get_events()[0]["registered"]) == 1


def test_register_participant_persists_across_calls():
    event_id = db.get_events()[0]["id"]
    db.register_participant(event_id, "John Doe", "john@example.com")
    # Simulate a fresh request by re-reading from the database.
    events = db.get_events()
    assert events[0]["registered"][0]["email"] == "john@example.com"


def test_register_participant_rejects_duplicate_email():
    event_id = db.get_events()[0]["id"]
    db.register_participant(event_id, "John Doe", "john@example.com")
    success, message = db.register_participant(event_id, "John Doe", "John@Example.com")
    assert success is False
    assert len(db.get_events()[0]["registered"]) == 1


def test_register_participant_rejects_when_full():
    event_id = db.get_events()[1]["id"]  # capacity 2
    db.register_participant(event_id, "Anna", "a@example.com")
    db.register_participant(event_id, "Bob", "b@example.com")
    success, message = db.register_participant(event_id, "Carl", "c@example.com")
    assert success is False
    assert "full" in message.lower()


def test_register_participant_rejects_unknown_event():
    success, message = db.register_participant(9999, "John Doe", "john@example.com")
    assert success is False
