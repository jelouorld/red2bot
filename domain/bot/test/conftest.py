

import pytest
import os 
from urllib.parse import urljoin

@pytest.fixture
def base_url():
    return os.environ['RED2BOT_URL']


@pytest.fixture
def init_url(base_url):
    return urljoin(base_url, 'init')

@pytest.fixture
def chat_url(base_url):
    return urljoin(base_url, 'chat')


