"""SQLite setup: schema, connections, first-run columns and sample cards."""

import os
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = PROJECT_DIR / "data" / "kanban.db"
DEFAULT_COLUMNS = ["To Do", "In Progress", "Done"]

SCHEMA = """
CREATE TABLE IF NOT EXISTS columns (
    id       TEXT PRIMARY KEY,
    name     TEXT NOT NULL,
    position INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS cards (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    column_id   TEXT NOT NULL REFERENCES columns(id),
    position    INTEGER NOT NULL,
    created_at  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_cards_column ON cards(column_id, position);
"""

# (column index, title, description). Index -1 is the last column.
SAMPLE_CARDS = [
    (0, "Write the README", "What it does, how to run it, example chat commands."),
    (0, "Add due dates to cards", ""),
    (1, "Fix the login bug", "Users get logged out when they refresh the page."),
    (1, "Design the chat sidebar", ""),
    (-1, "Set up the FastAPI project", "uv, FastAPI, SQLite, pytest."),
]


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def db_path_from_env() -> Path:
    return Path(os.getenv("KANBAN_DB") or DEFAULT_DB_PATH)


def columns_from_env() -> list[str]:
    raw = os.getenv("KANBAN_COLUMNS", "")
    names = [name.strip() for name in raw.split(",") if name.strip()]
    return names or DEFAULT_COLUMNS


def seed_from_env() -> bool:
    return os.getenv("KANBAN_SEED", "1").strip().lower() not in {"0", "false", "no"}


def connect(path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(path: str | Path, columns: list[str], seed: bool) -> None:
    """Create tables. Columns and sample cards are only written into an empty database."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = connect(path)
    try:
        with conn:
            conn.executescript(SCHEMA)
            if conn.execute("SELECT COUNT(*) FROM columns").fetchone()[0] == 0:
                ids = [slugify(name) for name in columns]
                if len(set(ids)) != len(ids) or not all(ids):
                    raise ValueError(f"Column names must be distinct and non-empty: {columns}")
                conn.executemany(
                    "INSERT INTO columns (id, name, position) VALUES (?, ?, ?)",
                    [(cid, name, i) for i, (cid, name) in enumerate(zip(ids, columns))],
                )
            if seed and conn.execute("SELECT COUNT(*) FROM cards").fetchone()[0] == 0:
                _seed_cards(conn)
    finally:
        conn.close()


def _seed_cards(conn: sqlite3.Connection) -> None:
    column_ids = [row["id"] for row in conn.execute("SELECT id FROM columns ORDER BY position")]
    next_position: dict[str, int] = {}
    for index, title, description in SAMPLE_CARDS:
        column_id = column_ids[index if index < len(column_ids) else -1]
        position = next_position.get(column_id, 0)
        conn.execute(
            "INSERT INTO cards (title, description, column_id, position, created_at)"
            " VALUES (?, ?, ?, ?, ?)",
            (title, description, column_id, position, now_iso()),
        )
        next_position[column_id] = position + 1
