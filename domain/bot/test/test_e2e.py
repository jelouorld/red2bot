from sys import breakpointhook
import requests


# def _valid_uuid(string: str):
#     import uuid

#     try:
#         uuid.UUID(string)
#         return True
#     except ValueError:
#         return False


def test_get_fails_on_init(init_url: str):
    response = requests.get(init_url)
    assert response.status_code != 200


def test_get_fails_on_chat(chat_url: str):
    response = requests.get(chat_url)
    assert response.status_code != 200


def test_post_succeeds_on_init(init_url: str):
    response = requests.post(init_url)
    breakpointhook()
    assert response.status_code == 201


def test_post_succeeds_on_chat(chat_url: str):
    breakpoint()
    response = requests.post(chat_url)
    breakpointhook()

    assert response.status_code == 200
