from math import e
import uuid
import time
import boto3


from typing import TypeAlias


UUID4: TypeAlias = str
RawDDBEntry: TypeAlias = dict
CleanDDBEntry: TypeAlias = dict


# don't implement repository pattern; keep it simple


# low level chats access layer.
# in future could be replaced by any other storage
# obeying the same implicit contract. Please, NOTICE the word "IMPLICIT"


# TODO:
# 1. Add guarded writes
# 2. _chats._add_entry idempotent; at least in:
#       a - init convercsation
#       b - end conversation


class _chats:
    TABLE = boto3.resource("dynamodb").Table("chats")

    @staticmethod
    def _add_entry(session_id: UUID4, role: str, content: str) -> None:
        item = {
            "session_id": session_id,
            "timestamp": int(time.time() * 1000),  # ms precision
            "role": role,
            "content": content,
            "message_id": str(uuid.uuid4()),  # optional, for uniqueness
        }
        _chats.TABLE.put_item(Item=item)
        return item

    @staticmethod
    def _load_entries(session_id: UUID4) -> list[RawDDBEntry]:
        result = _chats.TABLE.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("session_id").eq(
                session_id
            ),
            ScanIndexForward=True,  # ascending by timestamp
        )
        return result.get("Items", [])

    @staticmethod
    def exists(session_id: UUID4) -> bool:
        response = _chats.TABLE.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("session_id").eq(
                session_id
            ),
            Limit=1,
        )
        return len(response["Items"]) > 0


class chats:
    @staticmethod
    def init_conversation() -> UUID4:
        session_id: UUID4 = str(uuid.uuid4())
        _chats._add_entry(session_id, role="system", content="[INIT]")
        return session_id

    @staticmethod
    def add_message(session_id: UUID4, role: str, content: str) -> None:
        _chats._add_entry(session_id, role=role, content=content)

    @staticmethod
    def load_conversation(session_id: UUID4) -> list[dict]:
        entries: list[RawDDBEntry] = _chats._load_entries(session_id)
        return entries

    @staticmethod
    def end_conversation(session_id: UUID4) -> None:
        _chats._add_entry(session_id, role="system", content="[END]")

    @staticmethod
    def exists(session_id: UUID4) -> bool:
        return _chats.exists(session_id)


# low level products access layer
class _products:
    TABLE = boto3.resource("dynamodb").Table("products")

    @staticmethod
    def load() -> list[dict]:
        return _products.TABLE.scan()["Items"]


class products:
    @staticmethod
    def load() -> list[dict]:
        return _products.load()
