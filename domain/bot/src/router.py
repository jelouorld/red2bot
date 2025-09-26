"""
We will quickly write our own simple router.
In the future: replace with lambda powertools.

basic interaction:

$ curl url/init
    in the backend:
    route init
    create a new chat entry with an ID
    return an ID

$ curl url/chat/session_iod"
    params: message: str;
    # execute all the langchain thing and return the response
    return response
$

"""

import functools
from inspect import signature
import typing as tp

import exceptions as ex

"""
    (path, http_method) -> handler funciton
"""
__routes__: tp.Dict[tp.Tuple[str, str], tp.Callable] = {}


def _resolve_template_kwargs(path: str, template: str) -> str:
    path_tokens = path.split("/")
    template_tokens = template.split("/")

    kwargs: dict[str, str] = {}
    for i, token in enumerate(template_tokens):
        if token.startswith("{") and token.endswith("}"):
            kwargs[token[1:-1]] = path_tokens[i]
    return kwargs


def _is_template(path: str) -> bool:
    return "{" in path and "}" in path


def _starts_like(a: str, b: str, radix=4) -> bool:
    return a[:radix] == b[:radix]

    # for i in range(len(a)):
    #     if a[i] != b[i] and i<radix:
    #         return False
    # return True


def _route_match(event_path: str, def_path: str) -> bool:
    if _is_template(def_path):
        return _starts_like(event_path, def_path)
    return event_path == def_path


def route(path: str, method: str = "POST"):
    def wrapper(func):
        if not path.startswith("/"):
            raise ValueError("Routes must start with /")

        if not isinstance(method, str) or not method in ("POST", "GET"):
            raise ValueError("Methods must be POST or GET")

        __routes__[(path, method)] = func

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapped

    return wrapper


Path = tp.TypeVar("Path", str, str)
Method = tp.TypeVar("Method", str, str)
Body = tp.TypeVar("Body", str, None)


def _extract_vars(event: dict[str, tp.Any]) -> tp.Tuple[Method, Path, Body]:
    request_context = event.get("requestContext")
    http = request_context.get("http")
    event_path = http.get("path")
    event_method = http.get("method")
    event_body = request_context.get("body")
    return event_method, event_path, event_body


def _dispach_handler(event: dict[str, tp.Any]) -> tp.Callable:
    event_method, event_path, _ = _extract_vars(event)

    for def_path, def_method in __routes__:
        if _route_match(event_path, def_path) and event_method == def_method:
            return __routes__[(def_path, def_method)]
    raise ex.RoutingError(f"Route not found: {event_path} {event_method}")


def dispatch(event: dict[str, tp.Any]) -> dict[str, tp.Any]:
    handler = _dispach_handler(event)
    event_method, event_path, event_body = _extract_vars(event)

    parameters = signature(handler).parameters

    if not parameters:
        return handler()

    

    args:list=[]
    kwargs:dict={}

    


