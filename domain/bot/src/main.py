"""Lambda entry point for the chatbot domain."""

from __future__ import annotations

import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Mapping

import boto3
from botocore.exceptions import ClientError

import router


LOGGER = logging.getLogger(__name__)


_DDB = boto3.resource("dynamodb")
_PRODUCTS_TABLE_NAME = os.environ.get("PRODUCTS_TABLE", "products")
_CHATS_TABLE_NAME = os.environ.get("CHATS_TABLE", "chats")
_PRODUCTS_TABLE = _DDB.Table(_PRODUCTS_TABLE_NAME)
_CHATS_TABLE = _DDB.Table(_CHATS_TABLE_NAME)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_session_id() -> str:
    return uuid.uuid4().hex


def _display_name(product: Mapping[str, Any]) -> str:
    for key in ("name", "title", "product_id"):
        if product.get(key):
            return str(product[key])
    return str(product.get("product_id", "unknown"))


def _generate_reply(user_text: str, products: Iterable[Mapping[str, Any]]) -> str:
    product_list = list(products)
    if not product_list:
        return f"Thanks for your message: '{user_text}'."

    names = ", ".join(_display_name(product) for product in product_list[:3])
    if len(product_list) > 3:
        names += f" and {len(product_list) - 3} more"
    return f"Thanks for your message: '{user_text}'. I can help you with {names}."


def _list_products(limit: int = 5) -> Iterable[Mapping[str, Any]]:
    try:
        response = _PRODUCTS_TABLE.scan(Limit=limit)
    except ClientError:
        LOGGER.exception("Unable to scan products table")
        return []

    return response.get("Items", [])


@router.route("/init", method="POST")
def init() -> tuple[int, Dict[str, Any]]:
    session_id = _new_session_id()

    item = {
        "session_id": session_id,
        "messages": [],
        "created_at": _now(),
        "updated_at": _now(),
    }

    try:
        _CHATS_TABLE.put_item(Item=item)
    except ClientError as exc:  # pragma: no cover - depends on AWS env
        LOGGER.exception("Failed to create chat session")
        raise router.HTTPError(500, "Could not create session") from exc

    return 201, {"session_id": session_id}


@router.route("/chat/{session_id}", method="POST")
def chat(session_id: str, *, text: str = "") -> tuple[int, Dict[str, Any]]:
    if not text or not text.strip():
        raise router.HTTPError(400, "The 'text' field is required")

    try:
        chat_item = _CHATS_TABLE.get_item(Key={"session_id": session_id}).get("Item")
    except ClientError as exc:  # pragma: no cover - depends on AWS env
        LOGGER.exception("Error fetching chat session")
        raise router.HTTPError(500, "Could not load session") from exc

    if chat_item is None:
        raise router.HTTPError(404, "Unknown session")

    user_message = {
        "role": "user",
        "text": text,
        "timestamp": _now(),
    }

    products = list(_list_products())
    assistant_text = _generate_reply(text, products)
    assistant_message = {
        "role": "assistant",
        "text": assistant_text,
        "timestamp": _now(),
    }

    try:
        update_response = _CHATS_TABLE.update_item(
            Key={"session_id": session_id},
            UpdateExpression="SET messages = list_append(if_not_exists(messages, :empty), :messages), updated_at = :updated_at",
            ExpressionAttributeValues={
                ":messages": [user_message, assistant_message],
                ":empty": [],
                ":updated_at": _now(),
            },
            ConditionExpression="attribute_exists(session_id)",
            ReturnValues="ALL_NEW",
        )
    except ClientError as exc:  # pragma: no cover - depends on AWS env
        error_code = exc.response.get("Error", {}).get("Code") if hasattr(exc, "response") else None
        if error_code == "ConditionalCheckFailedException":
            raise router.HTTPError(404, "Unknown session") from exc
        LOGGER.exception("Failed to update chat session")
        raise router.HTTPError(500, "Could not persist message") from exc

    messages = update_response.get("Attributes", {}).get("messages", [])

    payload = {
        "session_id": session_id,
        "reply": assistant_text,
        "messages": messages,
        "products_used": [product.get("product_id") for product in products],
    }

    return 200, payload


def lambda_entrypoint(event: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """AWS Lambda handler."""

    return router.dispatch(event, context=context)
