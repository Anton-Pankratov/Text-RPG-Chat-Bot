from aiogram.types import Message

from db import db

async def delete_existing_messages(tg_chat_message: Message):
    from components import chat_bot

    existing_bot_msgs = await db.manager_msg_bot.get_bot_messages(chat_id=tg_chat_message.chat.id,
                                                                  topic_id=tg_chat_message.message_thread_id)

    for message in existing_bot_msgs:
        try:
            await chat_bot.delete_message(chat_id=tg_chat_message.chat.id, message_id=message.message_id)
        finally:
            continue
