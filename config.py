from pathlib import Path

# SQLite database file used by the calorie tracker application.
DB_PATH = Path(__file__).with_name("main.db")

# Table that stores all calorie events; keep consistent across migrations.
TABLE_NAME = "heath_tracker"
