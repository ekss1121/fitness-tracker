import sqlite3

import db
from config import TABLE_NAME
from events import Event, get_events, log_event


def _use_temp_db(monkeypatch, tmp_path):
    """Point DB_PATH at a temporary SQLite file for isolated tests."""
    test_db = tmp_path / "test_events.db"
    monkeypatch.setattr(db, "DB_PATH", test_db)
    return test_db


def test_insert_and_fetch_events(monkeypatch, tmp_path):
    test_db = _use_temp_db(monkeypatch, tmp_path)

    db.insert_event("alice", "Apple", 95, "2024-01-02")
    db.insert_event("bob", "Sandwich", 450, "2024-01-02")

    rows = db.fetch_events(user="alice")

    assert test_db.exists()
    assert rows == [("alice", "Apple", 95.0, "2024-01-02")]


def test_log_event_and_get_events(monkeypatch, tmp_path):
    _use_temp_db(monkeypatch, tmp_path)

    log_event(Event(user="alice", name="Banana", calories=105.5, date="2024-01-03"))
    log_event(Event(user="alice", name="Running 5K", calories=-300, date="2024-01-04"))
    log_event(Event(user="bob", name="Yoga", calories=-120, date="2024-01-03"))

    events = get_events(user="alice")

    assert [e.name for e in events] == ["Banana", "Running 5K"]
    assert events[0].calories == 105.5
    assert events[1].calories == -300


def test_migrates_legacy_schema(monkeypatch, tmp_path):
    test_db = _use_temp_db(monkeypatch, tmp_path)

    with sqlite3.connect(test_db) as connection:
        connection.execute(
            f"""
            CREATE TABLE {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                calories REAL NOT NULL,
                event_date TEXT NOT NULL
            )
            """
        )
        connection.execute(
            f"INSERT INTO {TABLE_NAME} (name, calories, event_date) VALUES (?, ?, ?)",
            ("Soup", 150, "2024-01-01"),
        )

    db.insert_event("alice", "Salad", 200, "2024-01-02")

    with sqlite3.connect(test_db) as connection:
        columns = [row[1] for row in connection.execute(f"PRAGMA table_info({TABLE_NAME})")]

    assert "user" in columns
    assert db.fetch_events() == [
        ("", "Soup", 150.0, "2024-01-01"),
        ("alice", "Salad", 200.0, "2024-01-02"),
    ]
