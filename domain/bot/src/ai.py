from ast import Call
from collections.abc import Callable

from typing import Callable, List, Dict


def generate_response(
    conversation: List[Dict], products_getter: Callable[[], List[Dict]]
) -> str:
    return "AI RESPONSE"
