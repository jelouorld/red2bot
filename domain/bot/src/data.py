

import uuid 
import time 

from typing import TypeAlias

from src import CHATS_TABLE
from src import PRODUCTS_TABLE

UUID4: TypeAlias = str
RawDDBEntry: TypeAlias = dict
CleanDDBEntry: TypeAlias = dict



class chats:

    @staticmethod
    def _add_entry(session_id:UUID4, role: str, content: str) -> None:
        CHATS_TABLE.put_item(Item={
            'session_id': session_id,
            'role': role,
            'content': content,
            'timestamp': int(time.time())
        })

    @staticmethod
    def _load_entries(session_id:UUID4) -> list[RawDDBEntry]:
        entries: list[RawDDBEntry]= CHATS_TABLE.get_item(Key={'session_id': session_id})
        breakpoint() 

    
    @staticmethod
    def _clean_entries(entries: list[RawDDBEntry]) -> list[CleanDDBEntry]:
        return list(map(
                lambda entry: {
                    'role': entry['role'],
                    'content': entry['content'],
                    'timestamp': entry['timestamp']
                },
                entries['Items']
            )
        )

    @staticmethod
    def add_init_entry(session_id=None) -> UUID4:
        session_id: UUID4= session_id or str(uuid.uuid4())
        chats._add_entry(session_id, role='system', content='[INIT]')
        return session_id

    @staticmethod
    def add_user_entry(session_id:UUID4, content: str) -> None:
        chats._add_entry(session_id, role='user', content=content)

    @staticmethod
    def add_assistant_entry(session_id:UUID4, content: str) -> None:
        chats._add_entry(session_id, role='assistant', content=content)


    @staticmethod
    def load_conversation(session_id:UUID4) -> list[dict]:

        return chats._clean_entries(chats._load_entries(session_id))

