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
import typing

"""
    (path, http_method) -> handler funciton
"""
__routes__: typing.Dict[typing.Tuple[str, str], typing.Callable] = {}


def route(path: str, method: str = "POST"):
    def wrapper(func):

        __routes__[(path, method)] = func

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapped

    return wrapper



def dispatch(event: dict):

    breakpoint()
    # main dispatch logic:
    path = event["path"]
