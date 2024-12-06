from aiogram.types import Message as AiogramMessage
from pyrogram.types import Message as PyrogramMessage
from telethon.tl.patched import Message as TelethonMessage

from data.data_message_user import MessageUserData
from db import db

def form_message_user_data_aiogram(message: AiogramMessage) -> MessageUserData:
    return MessageUserData(
        chat_id=message.chat.id,
        topic_id=message.message_thread_id,
        message_id=message.message_id,
        user_id=message.from_user.id,
        message_text=message.text
    )

def form_message_user_data_telethon(message: TelethonMessage):
    user_id = message.sender_id if message.sender_id else None
    topic_id = message.reply_to.reply_to_top_id if message.reply_to and message.reply_to.reply_to_top_id else None

    return MessageUserData(
        chat_id=message.chat_id if message.chat_id else None,
        topic_id=topic_id,
        message_id=message.id if message.id else None,
        user_id=user_id,
        message_text=message.text if message.text else None,
    )

async def save_user_message_aiogram(message: AiogramMessage) -> int:
    return await db.manager_msg_user.save_user_message_aiogram(form_message_user_data_aiogram(message))

async def save_user_message_pyrogram(message: PyrogramMessage):
    if message:
        await db.manager_msg_user.save_user_message(form_message_user_data_pyrogram(message))
