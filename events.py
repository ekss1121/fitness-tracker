from dataclasses import dataclass, field
from datetime import date
from typing import List

from db import fetch_events, insert_event


def today() -> str:
    return date.today().isoformat()


@dataclass
class Event:
    user: str
    name: str
    calories: float
    date: str = field(default_factory=today)


def log_event(event: Event) -> None:
    insert_event(event.user, event.name, event.calories, event.date)


def get_events(user: str | None = None) -> List[Event]:
    rows = fetch_events(user=user)
    return [Event(user=row[0], name=row[1], calories=row[2], date=row[3]) for row in rows]
