from aiogram.types import CallbackQuery

from features.keyboard.process_message_by_moderator import process_keyboard_from_moderator_click
from features.keyboard.process_message_by_player import process_keyboard_by_player_click


async def delete_message_after_click(callback_query: CallbackQuery):
    from components import chat_bot
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    await callback_query.answer()
    await chat_bot.delete_message(chat_id=chat_id, message_id=message_id)


async def handle_keyboard_clicks(callback_query: CallbackQuery):
    await delete_message_after_click(callback_query)
    await process_keyboard_by_player_click(callback_query)
    await process_keyboard_from_moderator_click(callback_query)
