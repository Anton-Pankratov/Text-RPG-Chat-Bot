from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from db import db
from features.action_bid_status import update_bid_status
from features.command_start.button_show_all_messages import collect_data_to_show_user_messages
from src.properties import BUTTON_CALLBACK_TAG_PLAYER_MESSAGES, BUTTON_CALLBACK_TAG_PLAYER_FORGET, \
    BUTTON_CALLBACK_TAG_PLAYER_PROCESSING, BUTTON_CALLBACK_TAG_PLAYER_IGNORE
from src.strings import TEXT_BUTTON_IGNORE, TEXT_BUTTON_FORGET, TEXT_BUTTON_PROCESSING
from utils.enums.status import BidStatus
from utils.enums.tag import Tags


def keyboard_process_message_by_player(user_message_row_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=TEXT_BUTTON_IGNORE,
                                 callback_data=f'''{BUTTON_CALLBACK_TAG_PLAYER_IGNORE}{user_message_row_id}'''),
            InlineKeyboardButton(text=TEXT_BUTTON_FORGET,
                                 callback_data=f'''{BUTTON_CALLBACK_TAG_PLAYER_FORGET}{user_message_row_id}''')
        ], [
            InlineKeyboardButton(text=TEXT_BUTTON_PROCESSING,
                                 callback_data=f'''{BUTTON_CALLBACK_TAG_PLAYER_PROCESSING}{user_message_row_id}''')
        ]]
    )


async def process_keyboard_by_player_click(callback_query: CallbackQuery):
    # Смотреть start.py
    if callback_query.data.startswith(BUTTON_CALLBACK_TAG_PLAYER_MESSAGES):
        select_user_id = callback_query.data.removeprefix(BUTTON_CALLBACK_TAG_PLAYER_MESSAGES)
        await collect_data_to_show_user_messages(message=callback_query.message, tag=Tags.ALL_MESSAGES,
                                         select_user_id=int(select_user_id))



    elif callback_query.data.startswith(BUTTON_CALLBACK_TAG_PLAYER_FORGET):
        actual_message_row_id = int(callback_query.data.removeprefix(BUTTON_CALLBACK_TAG_PLAYER_FORGET))
        await db.manager_msg_user.delete_user_message(row_id=actual_message_row_id)
        await db.manager_bid_handler.delete_bid_status(row_id=actual_message_row_id)

    elif callback_query.data.startswith(BUTTON_CALLBACK_TAG_PLAYER_PROCESSING):
        actual_message_row_id = callback_query.data.removeprefix(BUTTON_CALLBACK_TAG_PLAYER_PROCESSING)
        await update_bid_status(status=BidStatus.PROCESSING.code, actual_message_row_id=int(actual_message_row_id))
