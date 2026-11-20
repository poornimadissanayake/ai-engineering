"""The board assistant: an OpenRouter model with tool calling, looping until it stops asking for tools."""

import json
import os
import sqlite3
from typing import Any, Callable

from openai import OpenAI

from . import service

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "openai/gpt-4o-mini"
MAX_TOOL_ROUNDS = 6
MAX_HISTORY = 20

MUTATING_TOOLS = {"create_card", "move_card", "update_card", "delete_card"}


class ChatUnavailableError(RuntimeError):
    pass


def model_name() -> str:
    return os.getenv("OPENROUTER_MODEL") or DEFAULT_MODEL


def make_client() -> OpenAI:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ChatUnavailableError(
            "The assistant is off: OPENROUTER_API_KEY is not set. Add it to .env and restart. "
            "The board itself works without it."
        )
    return OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)


def _function(name: str, description: str, properties: dict, required: list[str]) -> dict:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
                "additionalProperties": False,
            },
        },
    }


CARD_ID = {"type": "integer", "description": "The card's id, from list_cards."}
COLUMN = {"type": "string", "description": "Column name or id, e.g. 'In Progress' or 'in-progress'."}

TOOLS = [
    _function(
        "list_cards",
        "List cards on the board, in board order. Filter by column and/or a text search on "
        "title and description. Use this to find a card's id before changing it.",
        {
            "column": COLUMN,
            "query": {"type": "string", "description": "Case-insensitive text to search for."},
        },
        [],
    ),
    _function(
        "create_card",
        "Create a card. It goes to the bottom of the column (the first column if none given).",
        {
            "title": {"type": "string"},
            "description": {"type": "string"},
            "column": COLUMN,
        },
        ["title"],
    ),
    _function(
        "move_card",
        "Move a card to a column. position is 0-based (0 = top); leave it out to put the card "
        "at the bottom.",
        {"card_id": CARD_ID, "column": COLUMN, "position": {"type": "integer", "minimum": 0}},
        ["card_id", "column"],
    ),
    _function(
        "update_card",
        "Change a card's title and/or description.",
        {"card_id": CARD_ID, "title": {"type": "string"}, "description": {"type": "string"}},
        ["card_id"],
    ),
    _function("delete_card", "Delete a card permanently.", {"card_id": CARD_ID}, ["card_id"]),
]

ToolFn = Callable[..., Any]

TOOL_FUNCTIONS: dict[str, ToolFn] = {
    "list_cards": lambda conn, **a: {"cards": service.list_cards(conn, **a)},
    "create_card": lambda conn, **a: {"created": service.create_card(conn, **a)},
    "move_card": lambda conn, **a: {"moved": service.move_card(conn, **a)},
    "update_card": lambda conn, **a: {"updated": service.update_card(conn, **a)},
    "delete_card": lambda conn, **a: {"deleted": service.delete_card(conn, **a)},
}


def run_tool(conn: sqlite3.Connection, name: str, raw_arguments: str) -> tuple[dict, bool]:
    """Run one tool call. Returns (result for the model, whether it succeeded).

    Errors go back to the model as {"error": ...} so it can correct itself, rather than
    failing the whole request.
    """
    fn = TOOL_FUNCTIONS.get(name)
    if fn is None:
        return {"error": f"Unknown tool '{name}'."}, False
    try:
        arguments = json.loads(raw_arguments or "{}")
        if not isinstance(arguments, dict):
            raise ValueError("arguments must be a JSON object")
    except ValueError as exc:
        return {"error": f"Could not parse arguments: {exc}"}, False
    try:
        return fn(conn, **arguments), True
    except TypeError as exc:  # wrong or missing argument names
        return {"error": f"Bad arguments for {name}: {exc}"}, False
    except (service.NotFoundError, ValueError) as exc:
        return {"error": str(exc)}, False


def system_prompt(conn: sqlite3.Connection) -> str:
    columns = ", ".join(f"{c['name']} (id: {c['id']})" for c in service.list_columns(conn))
    return (
        "You help manage a Kanban board. Its columns, left to right, are: "
        f"{columns}.\n"
        "Use the tools to read and change the board. Never guess a card id: call list_cards "
        "(a text query is fine) and use the id it returns. If more than one card matches and "
        "it is unclear which the user means, ask instead of changing anything. "
        "After making changes, say briefly what you did. Keep replies short and plain."
    )


def _assistant_message(message: Any) -> dict:
    return {
        "role": "assistant",
        "content": message.content,
        "tool_calls": [
            {
                "id": call.id,
                "type": "function",
                "function": {"name": call.function.name, "arguments": call.function.arguments},
            }
            for call in message.tool_calls
        ],
    }


def run_chat(
    conn: sqlite3.Connection,
    client: Any,
    history: list[dict],
    model: str | None = None,
    max_rounds: int = MAX_TOOL_ROUNDS,
) -> dict:
    """Send the conversation to the model and execute tool calls until it answers in text.

    Returns {"reply", "board_changed", "actions"}.
    """
    messages: list[dict] = [{"role": "system", "content": system_prompt(conn)}]
    messages += history[-MAX_HISTORY:]
    actions: list[dict] = []
    board_changed = False

    for _ in range(max_rounds):
        response = client.chat.completions.create(
            model=model or model_name(),
            messages=messages,
            tools=TOOLS,
        )
        message = response.choices[0].message
        if not message.tool_calls:
            reply = (message.content or "").strip() or "Done."
            return {"reply": reply, "board_changed": board_changed, "actions": actions}

        messages.append(_assistant_message(message))
        for call in message.tool_calls:
            result, ok = run_tool(conn, call.function.name, call.function.arguments)
            if ok and call.function.name in MUTATING_TOOLS:
                board_changed = True
            actions.append({"tool": call.function.name, "arguments": call.function.arguments, "ok": ok})
            messages.append(
                {"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)}
            )

    return {
        "reply": (
            f"I stopped after {max_rounds} rounds of tool calls without finishing. "
            "Check the board, then try a narrower request."
        ),
        "board_changed": board_changed,
        "actions": actions,
    }
