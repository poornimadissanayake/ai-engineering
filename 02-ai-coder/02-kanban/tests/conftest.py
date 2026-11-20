import pytest
from fastapi.testclient import TestClient

from backend.main import create_app


@pytest.fixture
def app(tmp_path):
    return create_app(db_path=tmp_path / "test.db", seed=False)


@pytest.fixture
def client(app):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def add(client):
    """Create a card and return it: add("Title", column="done")."""

    def _add(title: str, column: str | None = None, **extra) -> dict:
        body = {"title": title, **extra}
        if column:
            body["column"] = column
        response = client.post("/api/cards", json=body)
        assert response.status_code == 201, response.text
        return response.json()

    return _add


@pytest.fixture
def titles(client):
    """Titles in a column, top to bottom, with a check that positions are 0..n-1."""

    def _titles(column: str) -> list[str]:
        board = client.get("/api/board").json()
        cards = next(c for c in board["columns"] if c["id"] == column)["cards"]
        assert [card["position"] for card in cards] == list(range(len(cards)))
        return [card["title"] for card in cards]

    return _titles
