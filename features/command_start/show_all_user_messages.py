from typing import Optional

from aiogram.enums import ParseMode
from aiogram.types import Message

from features.message_bot.save_message import save_bot_message
from src.properties import MESSAGE_POST_SYMBOLS_LIMIT
from utils.enums.tag import Tags
from utils.escape_markdown import escape_markdown_text


async def show_all_user_messages(tg_user_message: Message, user_msg_text: str, bot_msg_tag: Tags,
                                 keyboard: Optional = None):
    from components import chat_bot

    for i in range(0, len(user_msg_text), MESSAGE_POST_SYMBOLS_LIMIT):

        bot_message = await chat_bot.send_message(chat_id=tg_user_message.chat.id,
                                                  text=user_msg_text[i:i + MESSAGE_POST_SYMBOLS_LIMIT],
                                                  parse_mode=ParseMode.MARKDOWN_V2,
                                                  reply_markup=keyboard)

        await save_bot_message(tg_user_message=tg_user_message, tg_bot_message_id=bot_message.message_id, message_tag=bot_msg_tag)
