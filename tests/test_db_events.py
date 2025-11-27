import db
from events import Event, get_events, log_event


def _use_temp_db(monkeypatch, tmp_path):
    """Point DB_PATH at a temporary SQLite file for isolated tests."""
    test_db = tmp_path / "test_events.db"
    monkeypatch.setattr(db, "DB_PATH", test_db)
    return test_db


def test_insert_and_fetch_events(monkeypatch, tmp_path):
    test_db = _use_temp_db(monkeypatch, tmp_path)

    db.insert_event("Apple", 95, "2024-01-02")

    rows = db.fetch_events()

    assert test_db.exists()
    assert rows == [("Apple", 95.0, "2024-01-02")]


def test_log_event_and_get_events(monkeypatch, tmp_path):
    _use_temp_db(monkeypatch, tmp_path)

    log_event(Event(name="Banana", calories=105.5, date="2024-01-03"))
    log_event(Event(name="Running 5K", calories=-300, date="2024-01-04"))

    events = get_events()

    assert [e.name for e in events] == ["Banana", "Running 5K"]
    assert events[0].calories == 105.5
    assert events[1].calories == -300
