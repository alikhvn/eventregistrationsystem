"""Pure data logic for the Event Registration System (no Flask dependency, easy to unit-test)."""

import re
from dataclasses import dataclass, field

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


@dataclass
class Event:
    id: str
    title: str
    date: str
    capacity: int
    registered: list = field(default_factory=list)

    @property
    def is_full(self):
        return len(self.registered) >= self.capacity

    def is_already_registered(self, email):
        normalized = email.strip().lower()
        return any(p["email"].strip().lower() == normalized for p in self.registered)


def validate_name(name):
    return isinstance(name, str) and len(name.strip()) >= 2


def validate_email(email):
    return isinstance(email, str) and bool(EMAIL_RE.match(email.strip()))


def seed_events():
    return [
        Event(id="1", title="Web Development Workshop", date="2026-10-15", capacity=3),
        Event(id="2", title="AI & Machine Learning Meetup", date="2026-10-22", capacity=2),
        Event(id="3", title="Startup Pitch Night", date="2026-11-05", capacity=4),
    ]


def register_participant(event, name, email):
    """Validates and registers a participant. Returns (success, message)."""
    if not validate_name(name):
        return False, "Please enter a valid name (at least 2 characters)."
    if not validate_email(email):
        return False, "Please enter a valid email address."
    if event.is_full:
        return False, "This event is already full."
    if event.is_already_registered(email):
        return False, "This email is already registered for this event."

    event.registered.append({"name": name.strip(), "email": email.strip()})
    return True, f'{name.strip()} successfully registered for "{event.title}".'
