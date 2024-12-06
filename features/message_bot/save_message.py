from aiogram.types import Message

from data.data_message_bot import MessageBotData
from db import db
from utils.enums.tag import Tags


async def save_bot_message(tg_user_message: Message, tg_bot_message_id: int, message_tag: Tags):
    await db.manager_msg_bot.save_bot_message(
        MessageBotData(
            chat_id=tg_user_message.chat.id,
            topic_id=tg_user_message.message_thread_id,
            user_id=tg_user_message.from_user.id,
            message_tag=message_tag.value,
            message_id=tg_bot_message_id
        )
    )