import re

from data.data_message_user import MessageUserData
from src.strings import TEXT_SHOW_USER_MESSAGES_EMPTY
from utils.escape_markdown import escape_markdown_text, escape_markdown_link
from utils.form_message_link import form_message_link, form_message_link_target
from utils.parser_env_properties import get_players
from utils.remove_chat_id_prefix import handle_chat_id_text
from utils.shorten_text import shorten_text


async def form_messages_text(messages: list[MessageUserData], use_details: bool, title: str = None):
    players = get_players()
    result_text = ""

    for message in messages:
        short_text = escape_markdown_text(text=shorten_text(message.message_text))
        link_text = form_message_link_target(chat_id=handle_chat_id_text(message.chat_id), topic_id=message.topic_id, message_id=message.message_id)
        if use_details:
            result_text += f"{message.db_row_id}\\) {players.get(message.user_id).name}: {short_text} {link_text}\n\n"
        else:
            result_text += f"{short_text} {link_text}\n\n"

    if result_text == "":
        return TEXT_SHOW_USER_MESSAGES_EMPTY
    else:
        if title is not None:
            return title + "\n\n" + result_text
        else:
            return result_text
