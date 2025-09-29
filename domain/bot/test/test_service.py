


from service import ChatService


def test_full_conversation():
    chatservice = ChatService()
    session_id = chatservice.init_conversation()
    response = chatservice.send_message(session_id, "hello")
    assert response

    response = chatservice.send_message(session_id, "how are you")
    assert response

    
