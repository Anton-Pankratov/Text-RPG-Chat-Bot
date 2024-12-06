from src.properties import TELEGRAM_LINK_START_POINT
from src.strings import TEXT_SHOW_USER_MESSAGE_LINK


def form_message_link(chat_id: int, topic_id: int, message_id: int) -> str:
    if topic_id is None:
        return f"{TELEGRAM_LINK_START_POINT}c/{chat_id}/{message_id}"

    return f"{TELEGRAM_LINK_START_POINT}c/{chat_id}/{topic_id}/{message_id}"

def form_message_link_target(chat_id: int, topic_id: int, message_id: int) -> str:
    return f"[{TEXT_SHOW_USER_MESSAGE_LINK}]({form_message_link(chat_id=chat_id, topic_id=topic_id, message_id=message_id)})"