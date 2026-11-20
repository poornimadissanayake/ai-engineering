"""The chat tool loop, with the OpenAI client replaced by a scripted fake. No network."""

import json

import pytest
from openai.types.chat import ChatCompletion

from backend import chat
from backend.main import get_llm_client


def completion(content=None, tool_calls=None) -> ChatCompletion:
    """Build a real ChatCompletion object, the same type the SDK returns."""
    calls = [
        {
            "id": f"call_{i}",
            "type": "function",
            "function": {"name": name, "arguments": args if isinstance(args, str) else json.dumps(args)},
        }
        for i, (name, args) in enumerate(tool_calls or [])
    ]
    message = {"role": "assistant", "content": content}
    if calls:
        message["tool_calls"] = calls
    return ChatCompletion.model_validate(
        {
            "id": "cmpl",
            "object": "chat.completion",
            "created": 0,
            "model": "fake",
            "choices": [
                {
                    "index": 0,
                    "finish_reason": "tool_calls" if calls else "stop",
                    "message": message,
                }
            ],
        }
    )


class FakeClient:
    """Mimics client.chat.completions.create, replaying scripted responses and recording calls."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.requests: list[dict] = []
        self.chat = self
        self.completions = self

    def create(self, **kwargs):
        # Copy the messages: the loop keeps appending to the same list.
        self.requests.append({**kwargs, "messages": [dict(m) for m in kwargs["messages"]]})
        if callable(self.responses[0]):
            return self.responses[0](kwargs)
        return self.responses.pop(0)


@pytest.fixture
def use_fake(app):
    def _use(*responses) -> FakeClient:
        fake = FakeClient(responses)
        app.dependency_overrides[get_llm_client] = lambda: fake
        return fake

    yield _use
    app.dependency_overrides.clear()


def say(client, text):
    return client.post("/api/chat", json={"messages": [{"role": "user", "content": text}]})


def test_missing_api_key_gives_503_and_board_still_works(client, monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    response = say(client, "hello")
    assert response.status_code == 503
    assert "OPENROUTER_API_KEY" in response.json()["detail"]
    assert client.get("/api/board").status_code == 200


def test_client_points_at_openrouter(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    assert str(chat.make_client().base_url).startswith("https://openrouter.ai/api/v1")


def test_plain_answer_without_tools(client, use_fake):
    fake = use_fake(completion("Hi there."))
    body = say(client, "hello").json()
    assert body == {"reply": "Hi there.", "board_changed": False, "actions": []}
    request = fake.requests[0]
    assert {t["function"]["name"] for t in request["tools"]} == {
        "list_cards", "create_card", "move_card", "update_card", "delete_card",
    }
    assert request["messages"][0]["role"] == "system"
    assert "In Progress (id: in-progress)" in request["messages"][0]["content"]
    assert request["messages"][-1] == {"role": "user", "content": "hello"}


def test_model_comes_from_env(client, use_fake, monkeypatch):
    monkeypatch.setenv("OPENROUTER_MODEL", "some/cheap-model")
    fake = use_fake(completion("ok"))
    say(client, "hi")
    assert fake.requests[0]["model"] == "some/cheap-model"


def test_default_model_when_env_unset(client, use_fake, monkeypatch):
    monkeypatch.delenv("OPENROUTER_MODEL", raising=False)
    fake = use_fake(completion("ok"))
    say(client, "hi")
    assert fake.requests[0]["model"] == chat.DEFAULT_MODEL


def test_lookup_then_move_then_answer(client, add, titles, use_fake):
    bug = add("Fix the login bug", column="in-progress")
    add("Other card", column="done")
    fake = use_fake(
        completion(tool_calls=[("list_cards", {"query": "login"})]),
        completion(tool_calls=[("move_card", {"card_id": bug["id"], "column": "Done", "position": 0})]),
        completion("Moved 'Fix the login bug' to Done."),
    )
    body = say(client, "move the login bug to done").json()

    assert body["reply"] == "Moved 'Fix the login bug' to Done."
    assert body["board_changed"] is True
    assert [a["tool"] for a in body["actions"]] == ["list_cards", "move_card"]
    assert titles("done") == ["Fix the login bug", "Other card"]
    assert titles("in-progress") == []

    # The second request carries the first tool call and its result back to the model.
    second = fake.requests[1]["messages"]
    assert second[-2]["role"] == "assistant"
    assert second[-2]["tool_calls"][0]["function"]["name"] == "list_cards"
    assert second[-1]["role"] == "tool" and second[-1]["tool_call_id"] == "call_0"
    assert json.loads(second[-1]["content"])["cards"][0]["id"] == bug["id"]


def test_read_only_tools_do_not_flag_a_board_change(client, add, use_fake):
    add("Something", column="in-progress")
    use_fake(
        completion(tool_calls=[("list_cards", {"column": "In Progress"})]),
        completion("One card is in progress: Something."),
    )
    body = say(client, "what's still in progress?").json()
    assert body["board_changed"] is False
    assert body["reply"].startswith("One card")


def test_several_tool_calls_in_one_turn(client, titles, use_fake):
    use_fake(
        completion(tool_calls=[
            ("create_card", {"title": "Write tests"}),
            ("create_card", {"title": "Deploy", "column": "in-progress"}),
        ]),
        completion("Added two cards."),
    )
    body = say(client, "add write tests and deploy").json()
    assert body["board_changed"] is True
    assert titles("to-do") == ["Write tests"]
    assert titles("in-progress") == ["Deploy"]


def test_update_and_delete_via_tools(client, add, titles, use_fake):
    card = add("Old name")
    doomed = add("Remove me")
    use_fake(
        completion(tool_calls=[
            ("update_card", {"card_id": card["id"], "title": "New name"}),
            ("delete_card", {"card_id": doomed["id"]}),
        ]),
        completion("Done."),
    )
    assert say(client, "rename and delete").json()["board_changed"] is True
    assert titles("to-do") == ["New name"]


def test_tool_errors_go_back_to_the_model(client, use_fake):
    fake = use_fake(
        completion(tool_calls=[
            ("move_card", {"card_id": 999, "column": "done"}),
            ("move_card", "{not json"),
            ("create_card", {"title": "x", "colour": "red"}),
            ("drop_table", {}),
        ]),
        completion("Sorry, I couldn't find that card."),
    )
    response = say(client, "move card 999")
    assert response.status_code == 200
    body = response.json()
    assert body["board_changed"] is False
    assert [a["ok"] for a in body["actions"]] == [False] * 4
    tool_results = [json.loads(m["content"]) for m in fake.requests[1]["messages"] if m["role"] == "tool"]
    assert "not found" in tool_results[0]["error"]
    assert "parse" in tool_results[1]["error"]
    assert "Bad arguments" in tool_results[2]["error"]
    assert "Unknown tool" in tool_results[3]["error"]


def test_loop_stops_at_the_cap(client, use_fake):
    fake = use_fake(lambda _: completion(tool_calls=[("list_cards", {})]))
    body = say(client, "loop forever").json()
    assert len(fake.requests) == chat.MAX_TOOL_ROUNDS
    assert "stopped after" in body["reply"]
    assert body["board_changed"] is False


def test_history_is_passed_through_and_trimmed(client, use_fake):
    fake = use_fake(completion("ok"))
    history = [
        {"role": "user" if i % 2 == 0 else "assistant", "content": f"m{i}"} for i in range(30)
    ]
    client.post("/api/chat", json={"messages": history})
    sent = fake.requests[0]["messages"]
    assert len(sent) == 1 + chat.MAX_HISTORY
    assert sent[-1]["content"] == "m29"


def test_chat_rejects_bad_roles(client, use_fake):
    use_fake(completion("ok"))
    response = client.post("/api/chat", json={"messages": [{"role": "system", "content": "x"}]})
    assert response.status_code == 422
