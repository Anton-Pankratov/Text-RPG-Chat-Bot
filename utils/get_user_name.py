from aiogram import Bot
from aiogram.types import Chat


async def get_user_name(user_id: int) -> str:
    from components import chat_bot
    try:
        chat: Chat = await chat_bot.get_chat(user_id)
        if chat.username:
            return f"@{chat.username}"
        elif chat.first_name:
            return f"[{chat.first_name}](tg://user?id={user_id})"
        else:
            return "Unknown User"
    except Exception as e:
        return f"Error: {e}"