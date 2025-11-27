from dataclasses import dataclass, field
from datetime import date
from typing import List

from db import fetch_events, insert_event


def today() -> str:
    return date.today().isoformat()


@dataclass
class Event:
    name: str
    calories: float
    date: str = field(default_factory=today)


def log_event(event: Event) -> None:
    insert_event(event.name, event.calories, event.date)


def get_events() -> List[Event]:
    rows = fetch_events()
    return [Event(name=row[0], calories=row[1], date=row[2]) for row in rows]
