import pytest
import pytest_cov
import requests
from requests.models import Response
import boto3

from src import CHATS_TABLE


def test_get_fails_on_init(init_url: str):
    response = requests.get(init_url)
    assert response.status_code != 200


def test_get_fails_on_chat(chat_url: str):
    response = requests.get(chat_url)
    assert response.status_code != 200


def test_post_succeeds_on_init(init_url: str):
    response = requests.post(init_url)
    assert response.status_code == 201


def post_succeeds_on_chat(chat_url: str):
    response = requests.post(chat_url)
    assert response.status_code == 200


def _valid_uuid(string: str):
    import uuid

    try:
        uuid.UUID(string)
        return True
    except ValueError:
        return False


def test_init_chat(init_url: str):
    response: Response = requests.post(init_url)


    assert response.status_code == 201

    session_id = response.json()["session_id"]

    assert _valid_uuid(session_id)

    entry: dict = CHATS_TABLE.get_item(Key={"session_id": session_id})

    item: dict = entry["Item"]

    assert "session_id" in item
    assert item["session_id"] == session_id
