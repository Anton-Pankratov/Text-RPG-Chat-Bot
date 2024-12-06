from utils.enums.tag import Tags


class MessageBotData:

    def __init__(self, chat_id: int, topic_id: int, user_id: int, message_tag: str, message_id: int):
        self.chat_id = chat_id
        self.topic_id = topic_id
        self.user_id = user_id
        self.message_tag = message_tag
        self.message_id = message_id