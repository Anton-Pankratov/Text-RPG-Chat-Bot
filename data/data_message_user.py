from dataclasses import dataclass


@dataclass(frozen=True)
class MessageUserData:
    chat_id: int
    topic_id: int
    user_id: int
    message_id: int
    message_text: str
    db_row_id: int = None

message_user_data_fields_order = [
    "db_row_id", "chat_id", "topic_id", "user_id", "message_id", "message_text"
]
