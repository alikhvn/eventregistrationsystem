import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from models import Event, register_participant, validate_email, validate_name


def test_validate_name():
    assert validate_name("Alikhan") is True
    assert validate_name("A") is False
    assert validate_name("  ") is False
    assert validate_name("") is False


def test_validate_email():
    assert validate_email("user@example.com") is True
    assert validate_email("not-an-email") is False
    assert validate_email("user@") is False


def test_event_is_full():
    event = Event(id="1", title="Test", date="2026-01-01", capacity=1)
    assert event.is_full is False
    event.registered.append({"name": "A", "email": "a@a.com"})
    assert event.is_full is True


def test_register_participant_success():
    event = Event(id="1", title="Test Event", date="2026-01-01", capacity=2)
    success, message = register_participant(event, "John Doe", "john@example.com")
    assert success is True
    assert "John Doe" in message
    assert len(event.registered) == 1


def test_register_participant_rejects_invalid_email():
    event = Event(id="1", title="Test Event", date="2026-01-01", capacity=2)
    success, message = register_participant(event, "John Doe", "not-an-email")
    assert success is False
    assert len(event.registered) == 0


def test_register_participant_rejects_duplicate():
    event = Event(id="1", title="Test Event", date="2026-01-01", capacity=2)
    register_participant(event, "John Doe", "john@example.com")
    success, message = register_participant(event, "John Doe", "John@Example.com")
    assert success is False
    assert len(event.registered) == 1


def test_register_participant_rejects_when_full():
    event = Event(id="1", title="Test Event", date="2026-01-01", capacity=1)
    register_participant(event, "First User", "first@example.com")
    success, message = register_participant(event, "Second User", "second@example.com")
    assert success is False
    assert "full" in message.lower()
