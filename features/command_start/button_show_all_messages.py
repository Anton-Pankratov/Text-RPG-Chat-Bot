from aiogram.types import Message

from features.keyboard.keyboard_players import keyboard_players
from db import db
from features.command_start.show_all_user_messages import show_all_user_messages
from features.message_bot.save_message import save_bot_message
from src.strings import TEXT_SHOW_USER_SELECT
from utils.enums.tag import Tags
from utils.form_all_user_messages_text import form_messages_text
from utils.parser_env_properties import get_moderator_id

async def collect_data_to_show_user_messages(message: Message, tag: Tags, select_user_id: int = None):
    if select_user_id is None:
        db_messages = await db.manager_msg_user.get_all_user_messages(user_id=message.from_user.id)
    else:
        db_messages = await db.manager_msg_user.get_all_user_messages(user_id=select_user_id)

    user_message = await form_messages_text(messages=db_messages, use_details=False)
    await show_all_user_messages(tg_user_message=message, user_msg_text=user_message, bot_msg_tag=tag)

async def process_show_all_messages_button_click(message: Message):
    from components import chat_bot

    moderator_id = get_moderator_id()
    is_player_message = message.from_user.id != moderator_id
    is_moderator_chat = message.chat.id == moderator_id

    if is_moderator_chat:
        bot_message = await chat_bot.send_message(chat_id=message.chat.id, text=TEXT_SHOW_USER_SELECT,
                                                  reply_markup=keyboard_players())
        await save_bot_message(tg_user_message=message, tg_bot_message_id=bot_message.message_id, message_tag=Tags.ALL_MESSAGES)


    elif is_player_message:
        await collect_data_to_show_user_messages(message=message, tag=Tags.ALL_MESSAGES)