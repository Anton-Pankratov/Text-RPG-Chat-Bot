from aiogram.enums import ChatType
from aiogram.filters import Filter
from aiogram.types import Message

from utils.parser_env_properties import get_chats, get_players


def is_rpg_chat(message: Message) -> bool:
    chats = get_chats()
    for chat_id, chat in chats.items():
        if message.chat.id == chat.id:
            allowed_topic_id = chat.topic_id
            message_topic_id = message.message_thread_id
            return allowed_topic_id == -1 or allowed_topic_id == message_topic_id
    return False


def is_allowed_user(message: Message) -> bool:
    players = get_players()
    if message.from_user.id in players.keys():
        return True
    else:
        return False


def is_allowed_message(message: Message) -> bool:
    return is_rpg_chat(message) & is_allowed_user(message)


class FilterIsPrivateChat(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type == ChatType.PRIVATE
