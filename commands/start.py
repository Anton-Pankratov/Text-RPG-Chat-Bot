from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message

from features.command_start.button_show_all_messages import process_show_all_messages_button_click
from features.command_start.button_show_unprocessed_messages import process_show_unprocessed_messages
from features.command_start.button_show_call_to_bid import show_message_call_to_bid
from features.message_bot.delete_message import delete_bot_message
from features.message_handle.delete_existing_bot_message import delete_existing_messages

from src.strings import TEXT_BUTTON_COMMAND_START_SHOW_USER_MESSAGES, TEXT_GREETINGS_AFTER_START, \
    TEXT_BUTTON_COMMAND_START_SHOW_UNPROCESSED_MESSAGES, TEXT_BUTTON_COMMAND_START_CREATE_TASK_OF_NEED_BID
from utils.parser_env_properties import get_moderator_id


async def start(message: Message) -> None:
    btn_show_messages = KeyboardButton(text=TEXT_BUTTON_COMMAND_START_SHOW_USER_MESSAGES)
    btn_show_unprocessed_messages = KeyboardButton(text=TEXT_BUTTON_COMMAND_START_SHOW_UNPROCESSED_MESSAGES)

    if message.chat.id == get_moderator_id():
        btn_create_bid_need_task = KeyboardButton(text=TEXT_BUTTON_COMMAND_START_CREATE_TASK_OF_NEED_BID)
        buttons = [[btn_show_messages], [btn_show_unprocessed_messages], [btn_create_bid_need_task]]
    else:
        buttons = [[btn_show_messages], [btn_show_unprocessed_messages]]

    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer(TEXT_GREETINGS_AFTER_START, reply_markup=keyboard)


async def handle_show_user_messages_button_click(message: Message):
    await delete_bot_message(chat_id=message.chat.id, message_id=message.message_id)
    await delete_existing_messages(tg_chat_message=message)

    if message.text == TEXT_BUTTON_COMMAND_START_SHOW_USER_MESSAGES:
        await process_show_all_messages_button_click(message)

    elif message.text == TEXT_BUTTON_COMMAND_START_SHOW_UNPROCESSED_MESSAGES:
        await process_show_unprocessed_messages(message)

    elif message.text == TEXT_BUTTON_COMMAND_START_CREATE_TASK_OF_NEED_BID:
        await show_message_call_to_bid(message=message)
