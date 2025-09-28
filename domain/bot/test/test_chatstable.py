



from src.data import chats



def test_add_fetch():
    session_id = chats.add_init_entry(session_id='xxxxx')
    entries = chats.load_conversation(session_id)
    assert len(entries)







