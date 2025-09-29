import dataaccess


def test_generate_conversation():
    session_id = dataaccess.chats.init_conversation()
    dataaccess.chats.add_message(
        session_id, role="user", content="hello, how are you today"
    )
    dataaccess.chats.add_message(
        session_id, role="assistant", content="I'm good, how about you?"
    )
    dataaccess.chats.add_message(session_id, role="user", content="I'm fine, thanks")
    dataaccess.chats.add_message(
        session_id, role="assistant", content="Great, I'm glad to hear that."
    )

    dataaccess.chats.end_conversation(session_id)

    conversation = dataaccess.chats.load_conversation(session_id)
    assert isinstance(conversation, list)
    assert all(isinstance(e, dict) for e in conversation)
    assert len(conversation) == 4 + 2  # 4 messages + init + end messages1


def test_chat_exists():
    session_id = dataaccess.chats.init_conversation()
    breakpoint()
    assert dataaccess.chats.exists(session_id)


def test_load_products():
    products = dataaccess.products.load()
    breakpoint()
    assert len(products) > 0
    assert all(isinstance(p, dict) for p in products)
    assert "product_id" in products[0]
    assert "description" in products[0]
    assert "price" in products[0]
    assert "client_id" in products[0]
