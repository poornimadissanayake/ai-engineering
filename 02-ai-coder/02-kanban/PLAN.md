# PLAN.md

Plan first, scaffold second, then one feature at a time — each step small enough to check
before moving on. Every step ends with the tests green and the app still starting.

## 0. Decide the shape

- [x] One FastAPI process serves the API and the UI, so Docker is a single image
- [x] SQLite through `sqlite3`: one file, no server, easy to put in a volume
- [x] Plain HTML/CSS/JS front end with no build step
- [x] The assistant uses the same service functions as the REST API — one code path
- [x] Write `AGENTS.md` so any coding agent starts with the same context

## 1. Scaffold

- [x] `pyproject.toml` for this folder only (uv, Python 3.12), dev group with pytest + httpx
- [x] `backend/` package with an app factory, `GET /api/health`
- [x] `frontend/index.html` served at `/`
- [x] `tests/conftest.py` with a per-test SQLite file
- [x] `uv sync && uv run pytest -q` passes on an empty suite

## 2. Database and board read

- [x] Schema: `columns` (id, name, position) and `cards` (id, title, description, column,
      position, created_at)
- [x] Columns from `KANBAN_COLUMNS` (default To Do / In Progress / Done), written once
- [x] Sample cards on an empty database, switchable with `KANBAN_SEED`
- [x] `GET /api/board` returns columns with their cards in order
- [x] Tests: default columns, custom columns, seeding doesn't duplicate

## 3. Card CRUD

- [x] `POST /api/cards` — first column by default, append by default, optional position
- [x] `GET /api/cards` (filter by column, text search) and `GET /api/cards/{id}`
- [x] `PATCH /api/cards/{id}` — title and/or description
- [x] `DELETE /api/cards/{id}` — closes the gap in the column
- [x] Column accepted by id or name in any case; unknown column is a 400 listing the valid ones
- [x] Tests for each, plus validation and 404s

## 4. Move and reorder

- [x] `POST /api/cards/{id}/move` with `{column, position?}`
- [x] Lift the card out, close the gap, open a gap at the target, drop it in — one
      transaction, same logic for same-column and cross-column moves
- [x] Out-of-range position appends; negative position is a 422
- [x] Tests: down and up within a column, own position, last slot, empty column, middle of
      another column, append, out of range, there-and-back, errors leave the board unchanged

## 5. Board UI

- [x] Render columns and cards from `/api/board`
- [x] Add a card per column, edit/delete in a dialog
- [x] HTML5 drag and drop with a drop marker; the drop index skips the dragged card so it
      matches the API's position rule
- [x] Drag-and-drop debugging: `dragover` must `preventDefault()` or `drop` never fires;
      `dragleave` fires on child elements, so only clear when actually leaving the column;
      empty columns need a minimum height to be a drop target
- [x] Reload the board from the server after every change instead of patching the DOM

## 6. Assistant

- [x] `POST /api/chat` takes the conversation, returns `{reply, board_changed, actions}`
- [x] OpenRouter through the `openai` SDK; model from `OPENROUTER_MODEL`, cheap default
- [x] Five tools: `list_cards`, `create_card`, `move_card`, `update_card`, `delete_card`
- [x] Loop: call the model, run any tool calls, feed results back, stop when it answers in
      text or after 6 rounds
- [x] Tool errors go back to the model as `{"error": ...}` so it can recover
- [x] Missing key → 503 with a clear message; the board keeps working
- [x] Chat sidebar; refresh the board when `board_changed` is true
- [x] Tests with a fake client: tools offered, lookup → move → answer, read-only turns,
      several calls in one turn, bad arguments and unknown tools, the round cap, history trim

## 7. Ship

- [x] Dockerfile: one image, uv-installed deps, SQLite at `/data`
- [x] `docker-compose.yml` with a named volume and optional `.env`
- [x] `.env.example`
- [x] README with run instructions, example chat commands and a cost note

## Later, maybe

- [ ] Rename, add and reorder columns from the UI
- [ ] Keyboard moves for cards (accessibility, and no mouse needed)
- [ ] Stream the assistant's reply
- [ ] Undo for the last assistant action
