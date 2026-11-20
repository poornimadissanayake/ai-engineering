from fastapi.testclient import TestClient

from backend.main import create_app


def test_empty_board_has_default_columns(client):
    board = client.get("/api/board").json()
    assert [c["name"] for c in board["columns"]] == ["To Do", "In Progress", "Done"]
    assert [c["id"] for c in board["columns"]] == ["to-do", "in-progress", "done"]
    assert all(c["cards"] == [] for c in board["columns"])


def test_columns_are_configurable(tmp_path):
    app = create_app(db_path=tmp_path / "custom.db", columns=["Backlog", "Doing", "Review", "Shipped"], seed=False)
    with TestClient(app) as client:
        names = [c["name"] for c in client.get("/api/board").json()["columns"]]
    assert names == ["Backlog", "Doing", "Review", "Shipped"]


def test_seed_cards_only_on_empty_database(tmp_path):
    path = tmp_path / "seeded.db"
    for _ in range(2):  # second start must not duplicate the samples
        with TestClient(create_app(db_path=path, seed=True)) as client:
            cards = client.get("/api/cards").json()
    assert len(cards) == 5
    assert any(c["title"] == "Fix the login bug" and c["column"] == "in-progress" for c in cards)


def test_create_defaults_to_first_column_and_appends(client, add, titles):
    first = add("One")
    second = add("Two", description="details")
    assert first["column"] == "to-do" and first["position"] == 0
    assert second["position"] == 1 and second["description"] == "details"
    assert first["created_at"]
    assert titles("to-do") == ["One", "Two"]


def test_create_by_column_name_and_at_position(client, add, titles):
    add("A", column="Done")
    add("B", column="done")
    add("Top", column="DONE", position=0)
    assert titles("done") == ["Top", "A", "B"]


def test_create_with_out_of_range_position_appends(client, add, titles):
    add("A")
    add("B", position=50)
    assert titles("to-do") == ["A", "B"]


def test_create_validation(client):
    assert client.post("/api/cards", json={"title": ""}).status_code == 422
    assert client.post("/api/cards", json={"title": "   "}).status_code == 400
    response = client.post("/api/cards", json={"title": "X", "column": "Nowhere"})
    assert response.status_code == 400
    assert "Valid columns" in response.json()["detail"]


def test_get_card_and_404(client, add):
    card = add("Read me")
    assert client.get(f"/api/cards/{card['id']}").json() == card
    assert client.get("/api/cards/999").status_code == 404


def test_update_title_and_description(client, add):
    card = add("Old", description="keep me")
    updated = client.patch(f"/api/cards/{card['id']}", json={"title": "New"}).json()
    assert updated["title"] == "New" and updated["description"] == "keep me"
    updated = client.patch(f"/api/cards/{card['id']}", json={"description": ""}).json()
    assert updated["title"] == "New" and updated["description"] == ""
    assert updated["column"] == card["column"] and updated["position"] == card["position"]


def test_update_errors(client, add):
    card = add("Card")
    assert client.patch("/api/cards/999", json={"title": "X"}).status_code == 404
    assert client.patch(f"/api/cards/{card['id']}", json={"title": ""}).status_code == 422


def test_delete_closes_the_gap(client, add, titles):
    add("A")
    middle = add("B")
    add("C")
    assert client.delete(f"/api/cards/{middle['id']}").status_code == 204
    assert titles("to-do") == ["A", "C"]
    assert client.get(f"/api/cards/{middle['id']}").status_code == 404
    assert client.delete(f"/api/cards/{middle['id']}").status_code == 404


def test_list_cards_filters(client, add):
    add("Fix login bug", column="in-progress")
    add("Write docs", description="mention the login page")
    add("Ship it", column="done")
    assert [c["title"] for c in client.get("/api/cards", params={"column": "In Progress"}).json()] == ["Fix login bug"]
    found = client.get("/api/cards", params={"q": "LOGIN"}).json()
    assert {c["title"] for c in found} == {"Fix login bug", "Write docs"}
    # Board order: columns left to right.
    assert [c["title"] for c in client.get("/api/cards").json()] == ["Write docs", "Fix login bug", "Ship it"]


def test_ui_is_served_at_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "<html" in response.text.lower()
    assert client.get("/app.js").status_code == 200
