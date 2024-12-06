import asyncio

from client import client_telethon
from db import db
from features.message_handle.save_user_message import form_message_user_data_telethon

async def fetch_messages(chat_id: int, topic_id: int):
    await db.init_db()

    messages = client_telethon.iter_messages(chat_id, reply_to=topic_id, reverse=True)

    async for message in messages:
        print(message.id)
        await db.manager_msg_user.save_user_message(form_message_user_data_telethon(message))

        await asyncio.sleep(1)
