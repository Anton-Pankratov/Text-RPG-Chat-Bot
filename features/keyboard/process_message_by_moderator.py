from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message

from data.data_message_user import MessageUserData
from db import db
from features.action_bid_status import get_all_messages_by_bid_status
from features.command_start.button_show_call_to_bid import show_players_in_selected_chat, \
    show_players_to_call_bid_periodic_message
from features.keyboard import checklist_points
from features.keyboard.keyboard_checklist import keyboard_checklist_select_messages, keys_checklist, user_tag
from features.task.check_running_task import check_running_task
from src.properties import BUTTON_CALLBACK_TAG_MODERATE_FORGET, BUTTON_CALLBACK_TAG_MODERATE_PROCESSED_FIX, \
    BUTTON_CALLBACK_TAG_MODERATE_PROCESSED_MARK, BUTTON_CALLBACK_TAG_MODERATE_IGNORE, \
    BUTTON_CALLBACK_CALL_PLAYERS_TO_BID_START, CHECKLIST_TAG_MESSAGES, BUTTON_CALLBACK_TAG_MODERATE_PLAYERS_SELECT, \
    BUTTON_CALLBACK_CALL_PLAYERS_TO_BID_STOP
from src.strings import TEXT_BUTTON_FORGET, TEXT_BUTTON_IGNORE, TEXT_BUTTON_PROCESSING
from utils.enums.status import BidStatus
from utils.form_all_user_messages_text import form_messages_text
from utils.parser_env_properties import get_players, get_chats


def keyboard_process_message_by_moderator(user_message_row_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=TEXT_BUTTON_IGNORE,
                                 callback_data=f'''{BUTTON_CALLBACK_TAG_MODERATE_IGNORE}{user_message_row_id}'''),
            InlineKeyboardButton(text=TEXT_BUTTON_FORGET,
                                 callback_data=f'''{BUTTON_CALLBACK_TAG_MODERATE_FORGET}{user_message_row_id}''')
        ], [
            InlineKeyboardButton(text=TEXT_BUTTON_PROCESSING,
                                 callback_data=f'''{BUTTON_CALLBACK_TAG_MODERATE_PROCESSED_MARK}{user_message_row_id}''')
        ]]
    )


async def show_user_messages_in_processing(message: Message):
    messages: list[MessageUserData] = await get_all_messages_by_bid_status(BidStatus.PROCESSING)
    text = await form_messages_text(messages=messages, use_details=True)
    keyboard = keyboard_checklist_select_messages(
        keyboard_tag=user_tag(CHECKLIST_TAG_MESSAGES, message.from_user.id),
        keys_tag=BUTTON_CALLBACK_TAG_MODERATE_PROCESSED_FIX,
        keyboard_key_states=keys_checklist(messages, lambda msg: msg.db_row_id,
                                           user_tag(CHECKLIST_TAG_MESSAGES, message.from_user.id)))
    await message.answer(text=text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN_V2)


async def process_keyboard_from_moderator_click(callback_query: CallbackQuery):
    if callback_query.data.startswith(BUTTON_CALLBACK_TAG_MODERATE_FORGET):
        actual_message_row_id = int(callback_query.data.removeprefix(BUTTON_CALLBACK_TAG_MODERATE_FORGET))
        await db.manager_msg_user.delete_user_message(row_id=actual_message_row_id)
        await db.manager_bid_handler.delete_bid_status(row_id=actual_message_row_id)

    elif callback_query.data.startswith(BUTTON_CALLBACK_TAG_MODERATE_PROCESSED_FIX):
        processed_message_row_ids = [key for inner_dict in checklist_points.values() for key, value in inner_dict.items() if value]
        for row_id in processed_message_row_ids:
            await db.manager_bid_handler.update_bid_status(message_row_id=row_id, status=BidStatus.FINISHED.code)

    elif callback_query.data.startswith(BUTTON_CALLBACK_TAG_MODERATE_PROCESSED_MARK):
        await show_user_messages_in_processing(callback_query.message)

    elif callback_query.data.startswith(BUTTON_CALLBACK_CALL_PLAYERS_TO_BID_START):
        chat_order = int(callback_query.data.removeprefix(BUTTON_CALLBACK_CALL_PLAYERS_TO_BID_START))
        players = get_players()
        in_chat_players = []

        for player_id, player in players.items():
            if chat_order in player.chats:
                in_chat_players.append(players.get(player_id))

        await show_players_in_selected_chat(message=callback_query.message, selected_chat_order=chat_order,
                                            players_in_chat=in_chat_players)

    elif callback_query.data.startswith(BUTTON_CALLBACK_CALL_PLAYERS_TO_BID_STOP):
        await check_running_task(tg_user_message=callback_query.message)

    elif callback_query.data.startswith(BUTTON_CALLBACK_TAG_MODERATE_PLAYERS_SELECT):
        chat_order = callback_query.data.removeprefix(BUTTON_CALLBACK_TAG_MODERATE_PLAYERS_SELECT)
        chat = get_chats()[int(chat_order)]
        players = get_players()

        selected_player_names = [
            key for inner_dict in checklist_points.values()
            for key, value in inner_dict.items() if value
        ]

        selected_player_ids = [
            player_id for player_id, player in players.items()
            if player.name in selected_player_names
        ]

        await show_players_to_call_bid_periodic_message(player_ids=selected_player_ids, chat_id=chat.id,
                                                        topic_id=chat.topic_id)
