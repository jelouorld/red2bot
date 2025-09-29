from curses import unctrl
from sys import breakpointhook
from urllib.parse import urljoin
import requests


# def _valid_uuid(string: str):
#     import uuid

#     try:
#         uuid.UUID(string)
#         return True
#     except ValueError:
#         return False

HTTP_BAD_REQUEST: int = 400
HTTP_CREATED: int = 201
HTTP_OK: int = 200
HTTP_SERVER_ERROR: int = 500


def url_for(*paths):
    return "/".join(paths)


def test_get_fails_on_init(init_url: str):
    response = requests.get(init_url)
    breakpoint()
    assert response.status_code == HTTP_BAD_REQUEST


def test_get_fails_on_chat(chat_url: str, chat_session_id):
    response = requests.get(urljoin(chat_url, chat_session_id))
    assert response.status_code == HTTP_BAD_REQUEST


def test_post_succeeds_on_init(init_url: str):
    response = requests.post(init_url)
    assert response.status_code == HTTP_CREATED


def test_post_fails_on_non_existent_chat(chat_url: str, chat_session_id):
    response = requests.post(
        url_for(chat_url, chat_session_id+"suffix"),
        json={"text": "hello"},
    )
    assert response.status_code == HTTP_BAD_REQUEST


def test_post_succeeds_on_chat(chat_url: str, chat_session_id: str):
    breakpointhook()
    response = requests.post(
        url_for(chat_url, chat_session_id),
        json={"text": "hello"},
    )
    breakpointhook()
    assert response.status_code == HTTP_OK


def test_bad_request_because_not_text_provided(chat_url, chat_session_id):
    response = requests.post(
        url_for(chat_url, chat_session_id),
        json={},
    )
    assert response.status_code >= HTTP_BAD_REQUEST



def test_end_to_end_conversation(init_url, chat_url):
    # init: 
    response = requests.post(init_url)
    session_id = response.json()["session_id"]
    assert response.status_code == HTTP_CREATED

    # message 
    response = requests.post(
        url_for(chat_url, session_id),
        json={"text": "hello"},
    )
    assert response.status_code == HTTP_OK
    assert response.json()["ai_response"] == 'AI RESPONSE'


    response = requests.post(
        url_for(chat_url, session_id),
        json={"text": "how are you"},
    )
    assert response.status_code == HTTP_OK
    assert response.json()["ai_response"] == 'AI RESPONSE'
