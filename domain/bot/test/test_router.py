import pytest

import router
import main
import exceptions as ex
import copy


def test__resolve_template_args(
    handler_params: dict = {"event": 0},
    event: dict = {"event": 0},
    path: str = "/chat/session_id",
    template: str = "/chat/{session_id}",
):
    assert router._resolve_template_args(
        handler_params=handler_params, event=event, path=path, template=template
    ) == [event, "session_id"]


def test__resolve_kwargs(
    event_body: str = '{"text": "text123"}', keyword_only_params={"text": "default"}
):
    assert router._resolve_kwargs(event_body, keyword_only_params) == {
        "text": "text123"
    }


def test__prefix_match(a: str = "/chat/session_id", b: str = "/chat/{session_id}"):
    assert router._prefix_match(a, b)


def test__route__match(a: str = "/chat/session_id", b: str = "/chat/{session_id}"):
    assert router._route_match(a, b)


def test_route_malformed():
    with pytest.raises(ValueError, match="Routes must start with /"):
        router.route("chat/{session_id}", method="POST")(lambda x: x)


def test_route_invalid_method():
    with pytest.raises(ValueError, match="Methods must be POST or GET"):
        router.route("/chat/{session_id}", method="PUT")(lambda x: x)


def test__extract_vars(chat_event):
    event_method, event_path, event_body = router._extract_vars(chat_event)
    assert event_method == chat_event["requestContext"]["http"]["method"]
    assert event_path == chat_event["requestContext"]["http"]["path"]
    assert event_body == chat_event["body"]


def test__resolve_handler(chat_event: dict, init_event: dict, event_event: dict):
    handler, _ = router._resolve_handler(chat_event)
    assert handler.__name__ == main.chat.__name__

    handler, _ = router._resolve_handler(init_event)
    assert handler.__name__ == main.init.__name__

    handler, _ = router._resolve_handler(event_event)
    assert handler.__name__ == main.event.__name__


def test_chat_route_dispatch(chat_event):
    chat_event["body"] = '{"text": "text123"}'
    chat_event["requestContext"]["http"]["path"] = "/chat/session_id"

    def chat(session_id: str, *, text=""):
        return {"session_id": session_id, "text": "text123"}

    router.route("/chat/{session_id}", method="POST")(chat)

    assert router.dispatch(chat_event) == {
        "session_id": "session_id",
        "text": "text123",
    }


def test_init_and_event_route_dispatch(init_event: dict):
    def init():
        return {"hello": "world"}

    _ = router.route("/init", method="POST")(init)

    def event(event: dict):
        return event

    _ = router.route("/event", method="GET")(event)

    assert router.dispatch(init_event) == {"hello": "world"}

    event = copy.deepcopy(init_event)
    event["requestContext"]["http"]["path"] = "/event"
    event["requestContext"]["http"]["method"] = "GET"

    assert router.dispatch(event) == event


def test_route_not_found(init_event):
    init_event["requestContext"]["http"]["path"] = "/unknown"

    with pytest.raises(ex.RoutingError, match="Route not found"):
        router.dispatch(init_event)


def test_no_route(init_event):
    init_event["requestContext"]["http"]["path"] = "/"
    with pytest.raises(ex.RoutingError, match="Route not found"):
        router.dispatch(init_event)


def test_route_assembly():
    def init():
        return 1

    wrapped = router.route("/init")(init)
    assert wrapped() == 1

