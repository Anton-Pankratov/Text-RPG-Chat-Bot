from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.parser_env_properties import get_chats


def keyboard_chats(callback_tag: str, add_button_tag: str = None, add_button_text: str = None) -> InlineKeyboardMarkup:
    chats = get_chats()
    keyboard = InlineKeyboardBuilder()

    for index, (order, chat) in enumerate(chats.items()):
        keyboard.row(InlineKeyboardButton(text=chat.name, callback_data=f"{callback_tag}{order}"))

        if add_button_tag and index == len(chats) - 1:
            keyboard.row(InlineKeyboardButton(text= add_button_text, callback_data=add_button_tag))

    return keyboard.as_markup()