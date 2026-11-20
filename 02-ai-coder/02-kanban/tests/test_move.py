import pytest


@pytest.fixture
def todo(add):
    """Four cards in To Do: A, B, C, D. Returns {title: card}."""
    return {title: add(title) for title in "ABCD"}


def move(client, card, column, position=None):
    body = {"column": column}
    if position is not None:
        body["position"] = position
    return client.post(f"/api/cards/{card['id']}/move", json=body)


def test_move_down_within_same_column(client, todo, titles):
    response = move(client, todo["A"], "to-do", 2)
    assert response.status_code == 200
    assert response.json()["position"] == 2
    assert titles("to-do") == ["B", "C", "A", "D"]


def test_move_up_within_same_column(client, todo, titles):
    move(client, todo["D"], "to-do", 0)
    assert titles("to-do") == ["D", "A", "B", "C"]


def test_move_to_own_position_is_a_no_op(client, todo, titles):
    move(client, todo["B"], "to-do", 1)
    assert titles("to-do") == ["A", "B", "C", "D"]


def test_move_to_last_slot_within_same_column(client, todo, titles):
    move(client, todo["A"], "to-do", 3)
    assert titles("to-do") == ["B", "C", "D", "A"]


def test_move_to_empty_column(client, todo, titles):
    response = move(client, todo["B"], "done", 0)
    assert response.json()["column"] == "done"
    assert titles("done") == ["B"]
    assert titles("to-do") == ["A", "C", "D"]  # gap closed


def test_move_into_middle_of_other_column(client, todo, add, titles):
    add("X", column="done")
    add("Y", column="done")
    move(client, todo["C"], "done", 1)
    assert titles("done") == ["X", "C", "Y"]
    assert titles("to-do") == ["A", "B", "D"]


def test_move_without_position_appends(client, todo, add, titles):
    add("X", column="done")
    move(client, todo["A"], "Done")
    assert titles("done") == ["X", "A"]


def test_out_of_range_position_appends(client, todo, add, titles):
    add("X", column="in-progress")
    move(client, todo["A"], "in-progress", 99)
    assert titles("in-progress") == ["X", "A"]
    move(client, todo["B"], "to-do", 99)  # same column, past the end
    assert titles("to-do") == ["C", "D", "B"]


def test_move_by_column_name_any_case(client, todo, titles):
    assert move(client, todo["A"], "In progress").status_code == 200
    assert titles("in-progress") == ["A"]


def test_move_there_and_back(client, todo, titles):
    move(client, todo["B"], "done")
    move(client, todo["B"], "to-do", 1)
    assert titles("to-do") == ["A", "B", "C", "D"]
    assert titles("done") == []


def test_move_errors(client, todo, titles):
    assert move(client, {"id": 999}, "done").status_code == 404
    assert move(client, todo["A"], "nowhere").status_code == 400
    assert move(client, todo["A"], "done", -1).status_code == 422
    assert titles("to-do") == ["A", "B", "C", "D"]  # nothing changed
