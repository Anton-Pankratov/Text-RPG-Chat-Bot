from random import randint
from typing import Iterable, Callable

from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from features.keyboard import checklist_points, checklist_callback_data, ChecklistCallback
from src.properties import T, CHECKLIST_TAG_CHECK_UPDATE
from src.strings import TEXT_BUTTON_PROCESSED_FIX
from utils.escape_markdown import escape_markdown_text


def keys_checklist(items: Iterable[T], key_extractor: Callable[[T], str], checklist_tag: str) -> dict[str, bool]:
    checklist_points.pop(checklist_tag, None)
    new_checklist = {key_extractor(item): False for item in items}
    checklist_points[checklist_tag] = new_checklist
    return new_checklist


def user_tag(base_tag: str, user_id: int):
    return f"{base_tag}{user_id}"


def keyboard_checklist_select_messages(keyboard_tag: str, keys_tag: str,
                                       keyboard_key_states: dict[str, bool]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for index, (order_id, completed) in enumerate(keyboard_key_states.items()):
        emoji = "✅" if completed else "⬜"

        generated_random_key = randint(1, 999999)
        checklist_callback_data[generated_random_key] = ChecklistCallback(keyboard_tag=keyboard_tag, keys_tag=keys_tag,
                                                                          order_id=order_id)

        builder.row(InlineKeyboardButton(text=f"{emoji} {order_id}",
                                         callback_data=f"{CHECKLIST_TAG_CHECK_UPDATE}{str(generated_random_key)}"))

        if index == len(keyboard_key_states) - 1:
            builder.row(InlineKeyboardButton(text=TEXT_BUTTON_PROCESSED_FIX, callback_data=keys_tag))

    return builder.as_markup()


async def update_checklist_after_click(callback_query: CallbackQuery):
    callback_checklist_key = int(callback_query.data.removeprefix(CHECKLIST_TAG_CHECK_UPDATE))
    callback_data = checklist_callback_data[callback_checklist_key]
    checklist_callback_data.clear()

    print(checklist_callback_data)

    keyboard_tag = callback_data.keyboard_tag
    keys_tag = callback_data.keys_tag
    order_id = callback_data.order_id

    if keyboard_tag in checklist_points:
        inner_dict = checklist_points[keyboard_tag]

        order_key = int(order_id) if order_id.isdigit() else order_id
        if order_key in inner_dict:
            inner_dict[order_key] = not inner_dict[order_key]

        current_message_text = escape_markdown_text(callback_query.message.text)
        keyboard = keyboard_checklist_select_messages(keyboard_tag=keyboard_tag, keys_tag=keys_tag,
                                                      keyboard_key_states=inner_dict)
        await callback_query.message.edit_text(text=current_message_text, reply_markup=keyboard,
                                               parse_mode=ParseMode.MARKDOWN_V2)
