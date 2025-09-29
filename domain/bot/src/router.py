import functools
from inspect import signature
import json
import typing as tp

import exceptions as ex

JSONStr: tp.TypeAlias = str


__routes__: tp.Dict[tp.Tuple[str, str], tp.Callable] = {}

# raises malformed
def _resolve_template_args(
    handler_params: dict, event: dict, path: str, template: str
) -> str:
    args: list[str] = []
    if "event" in handler_params:
        args.append(event)

    template_tokens: list[str] = template.split("/")
    path_tokens: list[str] = path.split("/")

    if len(template_tokens) != len(path_tokens):
        raise ex.RoutingError("Could not resolve route template args")


    for i, token in enumerate(template_tokens):
        if token.startswith("{") and token.endswith("}"):
            args.append(path_tokens[i])

    return args


def _resolve_kwargs(event_body: JSONStr, keyword_only_params: dict) -> str:
    body: dict = json.loads(event_body)
    return dict(keyword_only_params) | body


def _is_template(path: str) -> bool:
    return "{" in path and "}" in path


def _prefix_match(a: str, b: str, radix=4) -> bool:
    return a[:radix] == b[:radix]


def _route_match(event_path: str, def_path: str) -> bool:
    if _is_template(def_path):
        return _prefix_match(event_path, def_path)
    return event_path == def_path


def route(path: str, method: str = "POST"):
    def wrapper(func):
        if not path.startswith("/"):
            raise ValueError("Routes must start with /")

        if not isinstance(method, str) or method not in ("POST", "GET"):
            raise ValueError("Methods must be POST or GET")

        __routes__[(path, method)] = func

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapped

    return wrapper


Path = tp.TypeVar("Path", str, str)
Method = tp.TypeVar("Method", str, str)
Body = tp.TypeVar("Body", dict, None)


def _extract_vars(event: dict[str, tp.Any]) -> tp.Tuple[Method, Path, Body]:
    request_context = event.get("requestContext")
    http = request_context.get("http")
    event_path = http.get("path")
    event_method = http.get("method")
    event_body = event.get("body")
    return event_method, event_path, event_body


def _resolve_handler(event: dict[str, tp.Any]) -> tp.Callable:
    event_method, event_path, _ = _extract_vars(event)

    for def_path, def_method in __routes__:
        if _route_match(event_path, def_path) and event_method == def_method:
            return __routes__[(def_path, def_method)], def_path

    raise ex.RoutingError(f"Route not found: {event_path} {event_method}")


def dispatch(event: dict[str, tp.Any]) -> dict[str, tp.Any]:
    # init dispatcher
    handler, def_path = _resolve_handler(event)
    event_method, event_path, event_body = _extract_vars(event)
    parameters = signature(handler).parameters

        # resolve template args
    args = _resolve_template_args(parameters, event, event_path, def_path)

    # resolve keyword args
    kwargs = {}
    if event_body is not None:
        kwargs = _resolve_kwargs(
            event_body,
            keyword_only_params={
                name: param
                for name, param in parameters.items()
                if param.kind == param.KEYWORD_ONLY
            },
        )



    return handler(*args, **kwargs)
