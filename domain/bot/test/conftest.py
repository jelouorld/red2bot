import pytest
import os
import json
from urllib.parse import urljoin

from requests import session


def _load_json_file(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


@pytest.fixture
def base_url():
    yield os.environ["RED2BOT_URL"]


@pytest.fixture
def init_url(base_url):
    
    yield urljoin(base_url, "init")


@pytest.fixture
def chat_url(base_url):
    yield urljoin(base_url, "chat")


@pytest.fixture
def init_event():
    
    yield _load_json_file("events/init.json")


@pytest.fixture
def chat_event():
    
    yield _load_json_file("events/chat.json")


@pytest.fixture
def event_event():
    
    return _load_json_file("events/event.json")


@pytest.fixture
def chat_session_id():
    
    import os
    import dataaccess

    session_id: dataaccess.UUID4 = os.getenv('CHAT_SESSION_ID')
    if not session_id:
        raise ValueError("please set the fucking CHAT_SESSIO_ID for fixture purposes")
    
    dataaccess._chats._add_entry(session_id, role="system", content="[INIT]") # this interface is private, but it's ok for testing, i guess, i dunno 

    yield session_id
