# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py

# Run CLI demo (main.py)
python main.py

# Run all tests
pytest

# Run a single test class or method
pytest tests/test_pawpal.py::TestTaskCompletion
pytest tests/test_pawpal.py::TestTaskCompletion::test_mark_complete_changes_status_to_true
```

## Architecture

The project has two layers: a backend system (`pawpal_system.py`) and a Streamlit UI (`app.py`).

### Backend — `pawpal_system.py`

Four classes with a clear ownership hierarchy:

- **`Owner`** — holds `_time_available` (hours) and a list of `Pet` objects. `get_time_available()` raises `ValueError` for negative values.
- **`Pet`** — holds a list of `Task` objects. Duplicate tasks are silently ignored in `add_task()`.
- **`Task`** — attributes: `name`, `duration` (hours), `priority` (int, higher = more urgent), `category`, `description`, `completed` (bool). Priority is the scheduling key.
- **`Scheduler`** — takes an `Owner`, aggregates tasks from all pets via `get_all_tasks()`, and runs a greedy algorithm in `generate_plan(date)`: sorts by priority descending, then packs tasks until `time_available` is exhausted. `get_plan_explanation()` returns a human-readable summary.

### UI — `app.py`

Thin Streamlit shell. Imports `Owner`, `Pet`, `Task`, `Scheduler` from `pawpal_system`. Task data is stored in `st.session_state.tasks`. The "Generate schedule" button is where the scheduler should be wired up — it currently shows a placeholder warning.

### Tests — `tests/test_pawpal.py`

Uses `pytest`. Adds the project root to `sys.path` at the top so imports work without installation. Three test classes cover `Task` completion, `Pet.add_task()` behavior, and integration between the two.
