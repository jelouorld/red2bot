


from main import lambda_entrypoint

def test_lambda_entrypoint():
    assert lambda_entrypoint(None, None)=={'cli_invocation': True}



def test_main_chat(chat_event):
    result=lambda_entrypoint(chat_event, None)

    assert 'session_id' in result
    assert 'text' in result

