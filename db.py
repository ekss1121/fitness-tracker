import sqlite3
from typing import List

from config import DB_PATH, TABLE_NAME


def _ensure_table_exists(connection: sqlite3.Connection) -> None:
    connection.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            name TEXT NOT NULL,
            calories REAL NOT NULL,
            event_date TEXT NOT NULL
        )
        """
    )
    _ensure_user_column(connection)


def _ensure_user_column(connection: sqlite3.Connection) -> None:
    """Add the required user column if upgrading from a legacy schema."""
    cursor = connection.execute(f"PRAGMA table_info({TABLE_NAME})")
    column_names = [row[1] for row in cursor.fetchall()]
    if "user" in column_names:
        return

    connection.execute(
        f"ALTER TABLE {TABLE_NAME} ADD COLUMN user TEXT NOT NULL DEFAULT ''"
    )


def insert_event(user: str, name: str, calories: float, event_date: str) -> None:
    """Persist a single event row to SQLite."""
    with sqlite3.connect(DB_PATH) as connection:
        _ensure_table_exists(connection)
        connection.execute(
            f"INSERT INTO {TABLE_NAME} (user, name, calories, event_date) VALUES (?, ?, ?, ?)",
            (user, name, calories, event_date),
        )
        connection.commit()


def fetch_events(user: str | None = None) -> List[tuple[str, str, float, str]]:
    """Return all event rows ordered by insertion, optionally filtered by user."""
    with sqlite3.connect(DB_PATH) as connection:
        _ensure_table_exists(connection)
        query = f"SELECT user, name, calories, event_date FROM {TABLE_NAME}"
        params: tuple[str, ...] = ()
        if user is not None:
            query += " WHERE user = ?"
            params = (user,)
        query += " ORDER BY id"
        cursor = connection.execute(query, params)
        rows = cursor.fetchall()
    return [(row[0], row[1], float(row[2]), row[3]) for row in rows]
