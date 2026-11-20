# AGENTS.md

Context for coding agents working in this folder. Read this first, then `PLAN.md`.

## What this is

A Kanban board (columns + cards) with a chat assistant that can read and change the board
through tool calling. One FastAPI process serves the REST API, the chat endpoint and the static UI.

## Stack

- Python 3.12, managed with **uv** (this folder has its own `pyproject.toml` and `.venv`)
- FastAPI + uvicorn, SQLite through the standard-library `sqlite3` (no ORM)
- `openai` SDK pointed at OpenRouter (`https://openrouter.ai/api/v1`)
- Front end: plain HTML, CSS and JavaScript in `frontend/`. No framework, no build step
- pytest + FastAPI `TestClient`

## Layout

```
backend/db.py       schema, connections, first-run columns and sample cards
backend/service.py  every board operation; the only code that writes to the database
backend/chat.py     tool schemas, tool dispatch, the model loop
backend/main.py     FastAPI app factory (create_app), routes, static mount
frontend/           index.html, app.js, styles.css
tests/              pytest; conftest.py has the client / add / titles fixtures
```

## Commands

```bash
uv sync                                         # install, including dev deps
uv run pytest -q                                # all tests, no network
uv run uvicorn backend.main:app --reload        # http://127.0.0.1:8000
docker compose up --build                       # same app, SQLite in a named volume
```

## Conventions

- **One code path per operation.** REST routes and chat tools both call `backend/service.py`.
  A new board action means a service function first, then a route and/or a tool that wrap it.
- Positions are 0-based and contiguous per column. Any write that adds, removes or moves a
  card must leave every column as 0..n-1. `titles()` in `tests/conftest.py` asserts this.
- `move_card` position is counted with the moving card already lifted out. Out-of-range
  positions append; the API rejects negatives (422).
- Columns are referenced by id (`in-progress`) or name in any case (`In Progress`);
  `service.resolve_column` does the matching.
- Errors: `NotFoundError` → 404, `ValueError` (incl. `InvalidColumnError`) → 400, missing
  `OPENROUTER_API_KEY` → 503, upstream model failure → 502. Inside the chat loop, tool errors
  are returned to the model as `{"error": ...}`, never raised.
- Config is environment only: `OPENROUTER_API_KEY`, `OPENROUTER_MODEL`, `KANBAN_DB`,
  `KANBAN_COLUMNS`, `KANBAN_SEED`. `.env` is loaded from this folder.
- Front end builds DOM with `textContent`, never `innerHTML` with user or model text.

## Testing rules

- Tests never hit the network. Chat tests replace the client with `FakeClient` via
  `app.dependency_overrides[get_llm_client]` and build real `ChatCompletion` objects.
- Each test gets a fresh SQLite file under `tmp_path`, created with `seed=False`.
- Add a test with every behaviour change, especially anything touching positions.

## Don'ts

- Don't commit `.env`, `*.db` or `.venv`.
- Don't call OpenRouter from tests or add a paid call to any default path.
- Don't add a front-end build step or framework without a reason written in `PLAN.md`.
- Don't write SQL outside `db.py` and `service.py`.
- Don't raise `MAX_TOOL_ROUNDS` to paper over a prompt problem.
