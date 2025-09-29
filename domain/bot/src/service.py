

from dataaccess import chats, products
from ai import generate_response

class ChatService:

    
    def init_conversation(self):
        return chats.init_conversation()
    

    def send_message(self, session_id: str, text: str | None):
        if not chats.exists(session_id):
            raise ValueError("Conversation not found")
        
        if not text:
            raise ValueError("No text provided")
        

        chats.add_message(session_id, role="user", content=text)

        try:
            assistant_response: str = generate_response(
                chats.load_conversation(session_id),
                products.load,
            )
        except Exception as ex:
            raise ValueError("Error generating response: " + str(ex))

        chats.add_message(session_id, role="assistant", content=assistant_response)

        return assistant_response