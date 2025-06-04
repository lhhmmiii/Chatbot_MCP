from langchain_community.chat_message_histories import SQLChatMessageHistory

class ChatHistoryService:
    """
    A service for managing chat history using SQL-based storage.

    This service provides methods to add user and AI messages to the chat history,
    retrieve the entire chat history or the last message, and clear the chat history.

    Attributes:
        chat_message_history (SQLChatMessageHistory): An instance of SQLChatMessageHistory
            for storing and managing chat messages.

    Methods:
        add_user_message(message): Adds a user message to the chat history.
        add_ai_message(message): Adds an AI message to the chat history.
        get_chat_history(): Retrieves the entire chat history.
        get_last_message(): Retrieves the last message from the chat history.
        clear_chat_history(): Clears the chat history.
    """
    def __init__(self, user_id: str = "1323"):
        """
        Initializes the ChatHistoryService with a specific user ID.

        Args:
            user_id (str): The ID of the user for whom the chat history is managed.
        """
        self.chat_message_history = SQLChatMessageHistory(
            session_id=user_id, connection_string="sqlite:///sqlite.db"
        )

    def add_user_message(self, message):
        """
        Adds a user message to the chat history.

        Args:
            message: The user message to be added.
        """
        self.chat_message_history.add_user_message(message)

    def add_ai_message(self, message):
        """
        Adds an AI message to the chat history.

        Args:
            message: The AI message to be added.
        """
        self.chat_message_history.add_ai_message(message)

    def get_chat_history(self):
        """
        Retrieves the entire chat history.

        Returns:
            list: A list of all messages in the chat history.
        """
        return self.chat_message_history.messages
    
    def get_last_message(self):
        """
        Retrieves the last message from the chat history.

        Returns:
            The last message in the chat history.
        """
        return self.chat_message_history.messages[-1].content

    def clear_chat_history(self):
        """
        Clears the chat history.
        """
        self.chat_message_history.clear()

if __name__ == "__main__":
    chat_history_service = ChatHistoryService(user_id="1323")
    print(chat_history_service.get_last_message())
