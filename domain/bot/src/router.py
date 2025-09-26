"""Minimal HTTP router used by the bot lambda.

The real project uses AWS Lambda Powertools with FastAPI, but that would add
too many dependencies for the kata.  The goal of this module is to offer a
thin wrapper with a similar DX so that the handlers in ``main.py`` stay close
to production while still being easy to test locally.

The router supports:

* ``@route(path, method)`` decorator to register handlers.
* Path parameters using ``/resource/{identifier}`` syntax.
* Automatic JSON body decoding (including base64 payloads).
* Automatic wiring of path/query/body parameters to handler keyword
  arguments.
* Graceful error handling producing API Gateway compatible responses.

The module intentionally keeps the surface small and dependency free so it can
be vendored inside the kata without extra tooling.
"""

from __future__ import annotations

import base64
import functools
import inspect
import json
import logging
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, Mapping, Optional, Tuple


LOGGER = logging.getLogger(__name__)


RouteKey = Tuple[str, str]
Handler = Callable[..., Any]


__routes__: Dict[RouteKey, Handler] = {}


@dataclass
class HTTPError(Exception):
    """Raised when a handler wants to return an HTTP error response."""

    status_code: int
    message: str = ""
    headers: Optional[Mapping[str, str]] = None

    def to_response(self) -> Dict[str, Any]:
        """Return an API Gateway compatible response."""

        return _build_response(
            self.status_code,
            {"message": self.message} if self.message else None,
            headers=self.headers,
        )


def route(path: str, method: str = "POST") -> Callable[[Handler], Handler]:
    """Register ``func`` as the handler for ``method path``."""

    normalized_path = _normalize_path(path)
    normalized_method = method.upper()

    def wrapper(func: Handler) -> Handler:
        __routes__[(normalized_path, normalized_method)] = func

        @functools.wraps(func)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        return wrapped

    return wrapper


def dispatch(event: Mapping[str, Any], *, context: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
    """Dispatch the AWS Lambda event to the registered handler."""

    method = _extract_method(event)
    path = _normalize_path(_extract_path(event))

    LOGGER.debug("Dispatching request", extra={"method": method, "path": path})

    handler, path_params = _match_route(method, path)
    if handler is None:
        return _build_response(404, {"message": f"No route for {method} {path}"})

    try:
        result = handler(
            **_build_handler_kwargs(
                handler,
                path_params=path_params,
                event=event,
                context=context,
                body=_parse_body(event),
                query=_extract_query(event),
                headers=_extract_headers(event),
            )
        )
    except HTTPError as exc:
        LOGGER.info("Handler raised HTTPError: %s", exc)
        return exc.to_response()
    except Exception:  # pragma: no cover - defensive against handler bugs
        LOGGER.exception("Unhandled error while executing handler")
        return _build_response(500, {"message": "Internal server error"})

    return _normalize_handler_result(result)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _extract_method(event: Mapping[str, Any]) -> str:
    if "httpMethod" in event:
        return str(event["httpMethod"]).upper()

    request_context = event.get("requestContext") or {}
    http_info = request_context.get("http") or {}
    method = http_info.get("method")
    if method:
        return str(method).upper()

    return "GET"


def _extract_path(event: Mapping[str, Any]) -> str:
    for key in ("rawPath", "path"):
        path = event.get(key)
        if path:
            return str(path)

    request_context = event.get("requestContext") or {}
    http_info = request_context.get("http") or {}
    path = http_info.get("path")
    if path:
        return str(path)

    return "/"


def _extract_query(event: Mapping[str, Any]) -> Mapping[str, Any]:
    if "queryStringParameters" in event and event["queryStringParameters"]:
        return dict(event["queryStringParameters"])
    return {}


def _extract_headers(event: Mapping[str, Any]) -> Mapping[str, Any]:
    headers = event.get("headers") or {}
    if isinstance(headers, Mapping):
        return {str(k).lower(): v for k, v in headers.items()}
    return {}


def _normalize_path(path: str) -> str:
    if not path:
        return "/"
    segments = [segment for segment in path.split("/") if segment]
    return "/" + "/".join(segments)


def _match_route(method: str, path: str) -> Tuple[Optional[Handler], Dict[str, str]]:
    for (route_path, route_method), handler in __routes__.items():
        if route_method != method:
            continue

        params = _match_path_pattern(route_path, path)
        if params is not None:
            return handler, params

    return None, {}


def _match_path_pattern(pattern: str, path: str) -> Optional[Dict[str, str]]:
    pattern_segments = [segment for segment in pattern.split("/") if segment]
    path_segments = [segment for segment in path.split("/") if segment]

    if len(pattern_segments) != len(path_segments):
        return None

    params: Dict[str, str] = {}
    for expected, actual in zip(pattern_segments, path_segments):
        if expected.startswith("{") and expected.endswith("}"):
            params[expected[1:-1]] = actual
            continue

        if expected != actual:
            return None

    return params


def _parse_body(event: Mapping[str, Any]) -> Any:
    body = event.get("body")
    if body in (None, ""):
        return None

    if event.get("isBase64Encoded"):
        if isinstance(body, str):
            body_bytes = base64.b64decode(body)
        else:
            body_bytes = base64.b64decode(body)
        text = body_bytes.decode("utf-8")
    else:
        text = body if isinstance(body, str) else body.decode("utf-8")

    content_type = (_extract_headers(event).get("content-type") or "").split(";")[0].strip()

    if content_type == "application/json" or text.strip().startswith(("{", "[")):
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise HTTPError(400, f"Invalid JSON payload: {exc.msg}") from exc

    return text


def _build_handler_kwargs(
    handler: Handler,
    *,
    path_params: Mapping[str, str],
    event: Mapping[str, Any],
    context: Optional[Mapping[str, Any]],
    body: Any,
    query: Mapping[str, Any],
    headers: Mapping[str, Any],
) -> Dict[str, Any]:
    signature = inspect.signature(handler)
    kwargs: Dict[str, Any] = {}

    for name in signature.parameters:
        if name == "event":
            kwargs[name] = event
        elif name == "context":
            kwargs[name] = context
        elif name == "headers":
            kwargs[name] = headers
        elif name == "query":
            kwargs[name] = query
        elif name == "body":
            kwargs[name] = body
        elif name == "json_body":
            kwargs[name] = body if isinstance(body, Mapping) else None
        elif name == "raw_body":
            kwargs[name] = body if isinstance(body, str) else json.dumps(body) if body is not None else None
        elif name in path_params:
            kwargs[name] = path_params[name]
        elif isinstance(body, Mapping) and name in body:
            kwargs[name] = body[name]

    return kwargs


def _normalize_handler_result(result: Any) -> Dict[str, Any]:
    if result is None:
        return _build_response(204, None)

    if isinstance(result, dict) and "statusCode" in result:
        return result

    if isinstance(result, tuple):
        if len(result) == 2:
            status_code, payload = result
            headers = None
        elif len(result) == 3:
            status_code, payload, headers = result
        else:
            raise ValueError("Handler returned an unsupported tuple response")

        return _build_response(status_code, payload, headers=headers)

    return _build_response(200, result)


def _build_response(status_code: int, payload: Any, headers: Optional[Mapping[str, str]] = None) -> Dict[str, Any]:
    response_headers = {"Content-Type": "application/json"}
    if headers:
        response_headers.update(headers)

    if payload is None:
        body = ""
    elif isinstance(payload, str):
        body = payload
    else:
        body = json.dumps(payload, default=_json_default)

    return {
        "statusCode": status_code,
        "headers": response_headers,
        "body": body,
    }


def _json_default(value: Any) -> Any:
    try:
        import decimal

        if isinstance(value, decimal.Decimal):
            return float(value)
    except Exception:  # pragma: no cover - defensive
        pass

    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except Exception:  # pragma: no cover - defensive
            pass

    raise TypeError(f"Object of type {type(value)!r} is not JSON serialisable")

