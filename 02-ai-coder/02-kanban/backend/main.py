"""FastAPI app: REST API for the board, the chat endpoint, and the static UI at /."""

import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Iterator, Literal

import openai
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import chat, db, service

PROJECT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = PROJECT_DIR / "frontend"

load_dotenv(PROJECT_DIR / ".env")


class CardCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=5000)
    column: str | None = None
    position: int | None = Field(default=None, ge=0)


class CardUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)


class CardMove(BaseModel):
    column: str
    position: int | None = Field(default=None, ge=0)


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(max_length=4000)


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1)


class ChatResponse(BaseModel):
    reply: str
    board_changed: bool
    actions: list[dict[str, Any]]


def get_conn(request: Request) -> Iterator[sqlite3.Connection]:
    conn = db.connect(request.app.state.db_path)
    try:
        yield conn
    finally:
        conn.close()


def get_llm_client() -> Any:
    try:
        return chat.make_client()
    except chat.ChatUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


def create_app(
    db_path: str | Path | None = None,
    columns: list[str] | None = None,
    seed: bool | None = None,
) -> FastAPI:
    path = Path(db_path) if db_path else db.db_path_from_env()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        db.init_db(
            path,
            columns or db.columns_from_env(),
            db.seed_from_env() if seed is None else seed,
        )
        yield

    app = FastAPI(title="Kanban Chat", lifespan=lifespan)
    app.state.db_path = path

    @app.exception_handler(service.NotFoundError)
    async def not_found(_: Request, exc: service.NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(ValueError)
    async def bad_value(_: Request, exc: ValueError) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.get("/api/health")
    def health() -> dict:
        return {"status": "ok"}

    @app.get("/api/board")
    def board(conn: sqlite3.Connection = Depends(get_conn)) -> dict:
        return service.get_board(conn)

    @app.get("/api/cards")
    def cards(column: str | None = None, q: str | None = None, conn=Depends(get_conn)) -> list[dict]:
        return service.list_cards(conn, column=column, query=q)

    @app.post("/api/cards", status_code=201)
    def create(body: CardCreate, conn=Depends(get_conn)) -> dict:
        return service.create_card(conn, **body.model_dump())

    @app.get("/api/cards/{card_id}")
    def read(card_id: int, conn=Depends(get_conn)) -> dict:
        return service.get_card(conn, card_id)

    @app.patch("/api/cards/{card_id}")
    def update(card_id: int, body: CardUpdate, conn=Depends(get_conn)) -> dict:
        return service.update_card(conn, card_id, **body.model_dump(exclude_unset=True))

    @app.delete("/api/cards/{card_id}", status_code=204)
    def delete(card_id: int, conn=Depends(get_conn)) -> Response:
        service.delete_card(conn, card_id)
        return Response(status_code=204)

    @app.post("/api/cards/{card_id}/move")
    def move(card_id: int, body: CardMove, conn=Depends(get_conn)) -> dict:
        return service.move_card(conn, card_id, body.column, body.position)

    @app.post("/api/chat", response_model=ChatResponse)
    def chat_endpoint(
        body: ChatRequest,
        conn=Depends(get_conn),
        client: Any = Depends(get_llm_client),
    ) -> dict:
        history = [m.model_dump() for m in body.messages]
        try:
            return chat.run_chat(conn, client, history)
        except openai.APIError as exc:
            raise HTTPException(status_code=502, detail=f"Model call failed: {exc}") from exc

    # Last, so the /api routes above win.
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
    return app


app = create_app()
