from langchain_community.chat_message_histories import SQLChatMessageHistory


class ChatHistoryService:
    def __init__(self, user_id: str = "1323"):
        self.chat_message_history = SQLChatMessageHistory(
            session_id=user_id, connection_string="sqlite:///sqlite.db"
        )

    def add_user_message(self, message):
        self.chat_message_history.add_user_message(message)

    def add_ai_message(self, message):
        self.chat_message_history.add_ai_message(message)

    def get_chat_history(self):
        return self.chat_message_history.messages

    def clear_chat_history(self):
        self.chat_message_history.clear()

    def save_chat_history(self):
        self.chat_message_history.save()

    def load_chat_history(self):
        self.chat_message_history.load()



if __name__ == "__main__":
    chat_history_service = ChatHistoryService(user_id="1323")
    print(chat_history_service.get_chat_history())
