


from importlib import import_module
from sys import breakpointhook

import pytest

import router 
import main
import exceptions as ex

def test_route():
    pass 

def test__dispatch_handler(chat_event, init_event, event_event):
    
    assert router._dispach_handler(chat_event).__name__==main.chat.__name__
    assert router._dispach_handler(init_event).__name__==main.init.__name__
    assert router._dispach_handler(event_event).__name__==main.event.__name__


def test_dispatch(chat_event, init_event):
    
    router.dispatch(chat_event)
    router.dispatch(init_event)




