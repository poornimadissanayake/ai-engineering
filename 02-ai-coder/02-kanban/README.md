# Project 2 — Kanban board you can chat with

AI Coder, week 1 (days 3 and 5) · FastAPI · SQLite · plain JS · Docker · OpenRouter

A Kanban board with three columns — To Do, In Progress, Done — and an assistant in a sidebar
that can read and change the board. I drag cards between columns, add, edit and delete them,
or I type "move the login bug to done" and it does it.

The assistant isn't scripted. It gets five tools — `list_cards`, `create_card`, `move_card`,
`update_card`, `delete_card` — and decides which to call. Those tools are the same functions
the REST API uses, so a card moved by chat and a card moved by drag and drop go through exactly
the same code.

## Running this

Needs [uv](https://docs.astral.sh/uv/). Everything runs from this folder.

```bash
cd 02-ai-coder/02-kanban
cp .env.example .env        # then add OPENROUTER_API_KEY to use the chat
uv sync
uv run uvicorn backend.main:app --reload
```

Then open <http://127.0.0.1:8000>. The first start creates `data/kanban.db` with a few sample
cards. Without a key the board works and the chat says it's switched off.

Tests, no network and no key needed:

```bash
uv run pytest -q
```

### With Docker

```bash
docker compose up --build
```

Same app on port 8000. The SQLite file lives in a named volume (`kanban-data`), so cards
survive `docker compose down` and a rebuild. `docker compose down -v` wipes them.

### Settings

All in `.env`:

| variable | what it does |
|---|---|
| `OPENROUTER_API_KEY` | turns the assistant on |
| `OPENROUTER_MODEL` | any OpenRouter model with tool calling; blank means `openai/gpt-4o-mini` |
| `KANBAN_COLUMNS` | comma-separated column names, e.g. `Backlog,Doing,Review,Shipped` |
| `KANBAN_DB` | where the SQLite file goes |
| `KANBAN_SEED` | `0` to start with an empty board |

Columns are written when the database is first created. To change them later I delete the
`.db` file (or the Docker volume) and start again.

## Things to say to it

- "move the login bug to done"
- "what's still in progress?"
- "add a card called 'Write release notes' to In Progress"
- "put the README card at the top of To Do"
- "rename 'Add due dates to cards' to 'Due dates and reminders'"
- "delete everything in Done"
- "what's on the board?"

If two cards match what I said, it's told to ask which one rather than guess.

## How the tool loop works

`POST /api/chat` gets the conversation so far. The server adds a short system prompt that
names the columns, then:

1. Sends the messages plus the five tool definitions to the model.
2. If the reply contains tool calls, runs each one against the database, appends the call and
   its JSON result to the messages, and goes back to step 1.
3. If the reply is plain text, that's the answer.

It stops after 6 rounds either way, so a confused model can't loop forever. A typical move
takes three: `list_cards` with a search for "login" to get the id, `move_card`, then the reply.

Errors don't break the request. If the model asks for card 999 or sends bad arguments, the tool
returns `{"error": "Card 999 not found."}` and the model gets to try again or explain. The
response tells the page whether anything changed (`board_changed`), and the page only reloads
the board when it did.

The chat history lives in the browser, not on the server. Refresh the page and the
conversation starts fresh; the board doesn't.

## Cost

Only the chat costs anything. Each round resends the system prompt, the tool definitions and
the conversation, so a three-round move is roughly 3,000 input tokens and a few hundred output.
On a small model like `gpt-4o-mini` that's a fraction of a cent per request — check the current
price on the model's OpenRouter page. A bigger model costs more per round and usually needs
fewer of them. Either way, the round cap puts a ceiling on a single request.

## What I'd add next

Column editing from the UI, keyboard moves for cards, streaming replies, and an undo for the
assistant's last change. The build plan and what's ticked off is in [PLAN.md](PLAN.md);
[AGENTS.md](AGENTS.md) is the context file I give coding agents working on it.
