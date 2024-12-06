from typing import Optional

from aiogram.enums import ParseMode
from aiogram.types import Message, InlineKeyboardMarkup

from data.data_registred_player import Player
from features.keyboard.keyboard_chats import keyboard_chats
from features.keyboard.keyboard_checklist import keyboard_checklist_select_messages, user_tag, keys_checklist
from features.message_bot.save_message import save_bot_message
from features.task import task_manager
from src.properties import BUTTON_CALLBACK_CALL_PLAYERS_TO_BID_START, CHECKLIST_TAG_PLAYERS, \
    BUTTON_CALLBACK_TAG_MODERATE_PLAYERS_SELECT, BUTTON_CALLBACK_CALL_PLAYERS_TO_BID_STOP
from src.strings import TEXT_SHOW_CHAT_SELECT, TEXT_SHOW_USER_SELECT, TEXT_WRITE_YOUR_BID, \
    TEXT_BUTTON_COMMAND_START_STOP_TASK_OF_NEED_BID
from utils.enums.tag import Tags
from utils.get_user_name import get_user_name
from utils.parser_env_properties import get_moderator_id, get_players


async def show_by_button_click(message: Message, text: str, keyboard: InlineKeyboardMarkup):
    from components import chat_bot
    moderator_id = get_moderator_id()
    bot_message = await chat_bot.send_message(chat_id=moderator_id, text=text, reply_markup=keyboard)
    await save_bot_message(tg_user_message=message, tg_bot_message_id=bot_message.message_id,
                           message_tag=Tags.CALL_TO_BID)


async def show_message_call_to_bid(message: Message):
    await show_by_button_click(message=message, text=TEXT_SHOW_CHAT_SELECT,
                               keyboard=keyboard_chats(callback_tag=BUTTON_CALLBACK_CALL_PLAYERS_TO_BID_START,
                                                       add_button_tag=BUTTON_CALLBACK_CALL_PLAYERS_TO_BID_STOP,
                                                       add_button_text=TEXT_BUTTON_COMMAND_START_STOP_TASK_OF_NEED_BID))


async def show_players_in_selected_chat(message: Message, selected_chat_order: int,
                                        players_in_chat: list[Optional[Player]]):
    await show_by_button_click(message=message, text=TEXT_SHOW_USER_SELECT,
                               keyboard=keyboard_checklist_select_messages(
                                   keyboard_tag=user_tag(CHECKLIST_TAG_PLAYERS, message.from_user.id),
                                   keys_tag=f"{BUTTON_CALLBACK_TAG_MODERATE_PLAYERS_SELECT}{selected_chat_order}",
                                   keyboard_key_states=keys_checklist(
                                       items=players_in_chat,
                                       key_extractor=lambda player: player.name,
                                       checklist_tag=user_tag(CHECKLIST_TAG_PLAYERS, message.from_user.id))))


async def show_players_to_call_bid_periodic_message(player_ids: list[int], chat_id: int, topic_id: int):
    from components import chat_bot

    usernames = f"{TEXT_WRITE_YOUR_BID}"
    for player_id in player_ids:
        name = await get_user_name(int(player_id))
        usernames += f"\n\n{name}"

    if usernames:
        await task_manager.cancel_task()
        await task_manager.create_task(chat_bot.send_message, chat_id=chat_id, message_thread_id=topic_id,
                                       text=usernames, parse_mode=ParseMode.MARKDOWN_V2)
