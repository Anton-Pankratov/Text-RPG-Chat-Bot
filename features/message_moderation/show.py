from aiogram.enums import ParseMode
from aiogram.types import Message

from features.keyboard.process_message_by_moderator import keyboard_process_message_by_moderator
from features.keyboard.process_message_by_player import keyboard_process_message_by_player
from utils.escape_markdown import escape_markdown_text, escape_markdown_link
from utils.form_message_link import form_message_link
from utils.parser_env_properties import get_moderator_id
from utils.remove_chat_id_prefix import handle_chat_id_text


def form_player_msg_to_moderate(message: Message):
    tg_username = message.from_user.username

    message_text = escape_markdown_text(message.text)

    if tg_username is not None:
        return tg_username + "\n\n" + message_text
    else:
        return (f"Пользователь: "
                f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                f"\n\n{message_text}\n\n"
                f"{escape_markdown_link(form_message_link(chat_id=handle_chat_id_text(message.chat.id), topic_id=message.message_thread_id, message_id=message.message_id))}")


async def show_moderation_message(message: Message, user_message_row_id: int):
    from components import chat_bot
    moderator_id = get_moderator_id()

    if message.from_user.id == moderator_id:
        keyboard = keyboard_process_message_by_moderator(user_message_row_id)
    else:
        keyboard = keyboard_process_message_by_player(user_message_row_id)

    await chat_bot.send_message(chat_id=moderator_id, text=form_player_msg_to_moderate(message),
                                parse_mode=ParseMode.MARKDOWN_V2,
                                reply_markup=keyboard)
