import sqlite3
from typing import List, Tuple

from config import DB_PATH, TABLE_NAME


def _ensure_table_exists(connection: sqlite3.Connection) -> None:
    connection.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            calories REAL NOT NULL,
            event_date TEXT NOT NULL
        )
        """
    )


def insert_event(name: str, calories: float, event_date: str) -> None:
    """Persist a single event row to SQLite."""
    with sqlite3.connect(DB_PATH) as connection:
        _ensure_table_exists(connection)
        connection.execute(
            f"INSERT INTO {TABLE_NAME} (name, calories, event_date) VALUES (?, ?, ?)",
            (name, calories, event_date),
        )
        connection.commit()


def fetch_events() -> List[Tuple[str, float, str]]:
    """Return all event rows ordered by insertion."""
    with sqlite3.connect(DB_PATH) as connection:
        _ensure_table_exists(connection)
        cursor = connection.execute(
            f"SELECT name, calories, event_date FROM {TABLE_NAME} ORDER BY id"
        )
        rows = cursor.fetchall()
    return [(row[0], float(row[1]), row[2]) for row in rows]
