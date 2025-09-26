import pytest
import os 
import json
from urllib.parse import urljoin


def _load_json_file(path:str)->dict:
    with open(path) as f:
        return json.load(f)

@pytest.fixture
def base_url():
    return os.environ['RED2BOT_URL']


@pytest.fixture
def init_url(base_url):
    return urljoin(base_url, 'init')

@pytest.fixture
def chat_url(base_url):
    return urljoin(base_url, 'chat')

@pytest.fixture
def init_event():
    return _load_json_file('events/init.json')    

@pytest.fixture
def chat_event():
    return _load_json_file('events/chat.json')    


@pytest.fixture
def event_event():
    return _load_json_file('events/event.json')

