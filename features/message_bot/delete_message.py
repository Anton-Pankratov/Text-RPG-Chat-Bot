async def delete_bot_message(chat_id: int, message_id: int):
    from components import chat_bot

    await chat_bot.delete_message(chat_id=chat_id, message_id=message_id)