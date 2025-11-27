## Fitness Tracker

A simple calorie tracker that logs food and activities to a local SQLite database and reports daily totals. Includes a Click-based CLI for quick logging and summaries.
Now also exposes a small FastAPI server for logging activities and retrieving summaries.

### Features
- Log food (positive calories) and activities (negative calories) to `main.db`, scoped per user.
- View totals for food, activities, and net calories via CLI.
- Python modules split into config (`config.py`), DB access (`db.py`), and event helpers (`events.py`).
- Pytest coverage for DB and event logging (`tests/`).

### Requirements
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) for dependency management

### Setup
```bash
uv venv
uv sync
```
This installs dependencies and the console script `fitness-tracker`.

### CLI Usage
- Show summary (default user `default`): `uv run fitness-tracker`
- Explicit summary: `uv run fitness-tracker show --user alice`
- Log entry: `uv run fitness-tracker log "Apple" 95 --user alice`
- Log negative calories (activities): `uv run fitness-tracker log "Running 5K" -- -300 --user alice`
  - The `--` separates options from a negative number.
- Custom date: `uv run fitness-tracker log "Yoga" -150 --date 2025-01-05`

### API Usage
- Start the server: `uv run uvicorn api:app --reload`
- List activities: `GET /activities?user=alice`
- Daily summary for a date: `GET /summary?user=alice&date=2024-06-01` (date defaults to today)
- Log an activity: `POST /activities` with JSON body `{ "user": "alice", "name": "Swim", "calories": -250, "date": "2024-06-01" }`

### Development
- Run app directly: `uv run python main.py`
- Run tests: `uv run pytest`
- SQLite file: `main.db` (ignored by git). Remove it locally to start clean.

### Project Structure
- `main.py` — prints totals from logged events.
- `cli/` — Click CLI entrypoint (`fitness-tracker`).
- `events.py` — `Event` dataclass, log and read helpers.
- `db.py` — SQLite access layer.
- `config.py` — shared DB constants.
- `tests/` — pytest suite with temp DB usage.
