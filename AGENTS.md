# Repository Guidelines

## Project Structure & Module Organization

- `main.py`: entry point; prints calorie totals using aggregated events.
- `events.py`: `Event` dataclass plus `log_event` and `get_events` helpers.
- `db.py`: SQLite access layer (table creation, inserts, reads).
- `config.py`: shared constants like `DB_PATH` and `TABLE_NAME`.
- `fn_helper.py`: small functional helpers (e.g., `compose`).
- `main.db`: generated SQLite file beside the code; not checked in.
- Add new tests under `tests/` mirroring module names.

## Build, Test, and Development Commands

- `uv venv && uv sync`: create a virtual env and install dependencies from `pyproject.toml` / `uv.lock`.
- `uv run fitness-tracker`: run the CLI; defaults to showing current totals.
- `uv run python main.py`: ensure the database/table exists and print food vs activity totals.
- `uv run fitness-tracker log "Apple" 95`: log a sample food event; replace values per entry (negative calories for activities).
- `uv run pytest`: run the test suite.

## Coding Style & Naming Conventions

- Python 3.12; follow PEP 8 with 4-space indents and type hints for new functions.
- Use `snake_case` for modules/functions/variables, `PascalCase` for dataclasses like `Event`.
- Keep DB calls thin and reuse pure helpers; prefer small functions over inline logic.
- No formatter is configured; keep imports ordered and lines < 100 chars.

## Testing Guidelines

- Prefer `pytest`; place files under `tests/` as `test_<module>.py`.
- Favor in-memory SQLite (`sqlite3.connect(':memory:')`) or temp DB files to avoid mutating `main.db`.
- Target coverage: event logging, aggregation totals, and any new parsing or validation paths.

## Commit & Pull Request Guidelines

- Use imperative, concise commit subjects (<=72 chars); add bodies for rationale and testing notes.
- PRs should describe scope, testing performed (e.g., `python main.py`), and any DB touchpoints; include sample output if helpful.
- Avoid committing personal data in `main.db`; reset or recreate it locally before opening a PR.

## Data & Configuration Tips

- SQLite file lives at `main.db`; it is recreated automatically. Remove it locally to start clean.
- Table name is `heath_tracker`; keep consistent with queries/migrations until renamed deliberately.
- If adding settings, prefer environment variables over hardcoding secrets; document defaults in README.
