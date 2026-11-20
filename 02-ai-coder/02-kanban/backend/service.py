"""Board operations. The REST API and the chat tools both call these, so they behave the same.

Positions are 0-based and always contiguous within a column (0, 1, 2, ...). Every write that
changes a column's membership shifts its siblings to keep it that way.
"""

import sqlite3

from .db import now_iso, slugify


class NotFoundError(LookupError):
    pass


class InvalidColumnError(ValueError):
    pass


def _card(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "column": row["column_id"],
        "position": row["position"],
        "created_at": row["created_at"],
    }


def _clean_title(title: str) -> str:
    title = (title or "").strip()
    if not title:
        raise ValueError("Card title must not be empty.")
    return title


def _column_size(conn: sqlite3.Connection, column_id: str) -> int:
    return conn.execute("SELECT COUNT(*) FROM cards WHERE column_id = ?", (column_id,)).fetchone()[0]


def _clamp(position: int | None, size: int) -> int:
    """None or anything past the end means 'append'; negatives go to the top."""
    if position is None or position > size:
        return size
    return max(position, 0)


def list_columns(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute("SELECT id, name, position FROM columns ORDER BY position")
    return [dict(row) for row in rows]


def resolve_column(conn: sqlite3.Connection, value: str) -> str:
    """Accept a column id ('in-progress') or its name in any case ('In progress')."""
    wanted = slugify(value or "")
    for column in list_columns(conn):
        if wanted in (column["id"], slugify(column["name"])):
            return column["id"]
    names = ", ".join(c["name"] for c in list_columns(conn))
    raise InvalidColumnError(f"Unknown column '{value}'. Valid columns: {names}.")


def get_board(conn: sqlite3.Connection) -> dict:
    columns = [{**column, "cards": []} for column in list_columns(conn)]
    by_id = {column["id"]: column for column in columns}
    for row in conn.execute("SELECT * FROM cards ORDER BY position, id"):
        by_id[row["column_id"]]["cards"].append(_card(row))
    return {"columns": columns}


def list_cards(conn: sqlite3.Connection, column: str | None = None, query: str | None = None) -> list[dict]:
    sql = (
        "SELECT cards.* FROM cards JOIN columns ON columns.id = cards.column_id"
        " WHERE 1 = 1"
    )
    params: list = []
    if column:
        sql += " AND cards.column_id = ?"
        params.append(resolve_column(conn, column))
    if query:
        sql += " AND (cards.title LIKE ? OR cards.description LIKE ?)"
        params += [f"%{query}%", f"%{query}%"]
    sql += " ORDER BY columns.position, cards.position"
    return [_card(row) for row in conn.execute(sql, params)]


def get_card(conn: sqlite3.Connection, card_id: int) -> dict:
    row = conn.execute("SELECT * FROM cards WHERE id = ?", (card_id,)).fetchone()
    if row is None:
        raise NotFoundError(f"Card {card_id} not found.")
    return _card(row)


def create_card(
    conn: sqlite3.Connection,
    title: str,
    description: str = "",
    column: str | None = None,
    position: int | None = None,
) -> dict:
    title = _clean_title(title)
    column_id = resolve_column(conn, column) if column else list_columns(conn)[0]["id"]
    with conn:
        position = _clamp(position, _column_size(conn, column_id))
        conn.execute(
            "UPDATE cards SET position = position + 1 WHERE column_id = ? AND position >= ?",
            (column_id, position),
        )
        cursor = conn.execute(
            "INSERT INTO cards (title, description, column_id, position, created_at)"
            " VALUES (?, ?, ?, ?, ?)",
            (title, description or "", column_id, position, now_iso()),
        )
    return get_card(conn, cursor.lastrowid)


def update_card(
    conn: sqlite3.Connection,
    card_id: int,
    title: str | None = None,
    description: str | None = None,
) -> dict:
    card = get_card(conn, card_id)
    new_title = _clean_title(title) if title is not None else card["title"]
    new_description = description if description is not None else card["description"]
    with conn:
        conn.execute(
            "UPDATE cards SET title = ?, description = ? WHERE id = ?",
            (new_title, new_description, card_id),
        )
    return get_card(conn, card_id)


def delete_card(conn: sqlite3.Connection, card_id: int) -> dict:
    card = get_card(conn, card_id)
    with conn:
        conn.execute("DELETE FROM cards WHERE id = ?", (card_id,))
        conn.execute(
            "UPDATE cards SET position = position - 1 WHERE column_id = ? AND position > ?",
            (card["column"], card["position"]),
        )
    return card


def move_card(
    conn: sqlite3.Connection,
    card_id: int,
    column: str,
    position: int | None = None,
) -> dict:
    """Move a card to `column` at `position` (counted with the card already taken out).

    Works the same within one column and across columns: lift the card out and close the gap,
    then open a gap at the target and drop it in. An out-of-range position appends.
    """
    card = get_card(conn, card_id)
    target = resolve_column(conn, column)
    with conn:
        conn.execute(
            "UPDATE cards SET position = position - 1 WHERE column_id = ? AND position > ?",
            (card["column"], card["position"]),
        )
        # The card still sits in its old column, so leave it out of the target's count.
        size = conn.execute(
            "SELECT COUNT(*) FROM cards WHERE column_id = ? AND id != ?", (target, card_id)
        ).fetchone()[0]
        position = _clamp(position, size)
        conn.execute(
            "UPDATE cards SET position = position + 1"
            " WHERE column_id = ? AND position >= ? AND id != ?",
            (target, position, card_id),
        )
        conn.execute(
            "UPDATE cards SET column_id = ?, position = ? WHERE id = ?",
            (target, position, card_id),
        )
    return get_card(conn, card_id)
