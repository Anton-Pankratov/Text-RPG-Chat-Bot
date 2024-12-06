from aiogram.types import Message

from db import db
from features.command_start.show_all_user_messages import show_all_user_messages
from features.keyboard.process_message_by_moderator import show_user_messages_in_processing
from utils.enums.status import BidStatus
from utils.enums.tag import Tags
from utils.form_all_user_messages_text import form_messages_text
from utils.parser_env_properties import get_moderator_id


async def process_show_unprocessed_messages(message: Message):
    moderator_id = get_moderator_id()
    is_player_message = message.from_user.id != moderator_id
    is_moderator_chat = message.chat.id == moderator_id

    if is_moderator_chat:
        await show_user_messages_in_processing(message=message)
    elif is_player_message:
        db_messages = await db.manager_bid_handler.get_user_messages_by_bid_status(user_id=message.from_user.id,
                                                                                   status=BidStatus.PROCESSING.value)
        user_message = await form_messages_text(messages=db_messages, use_details=False)
        await show_all_user_messages(tg_user_message=message, user_msg_text=user_message,
                                     bot_msg_tag=Tags.USER_UNPROCESSED_MESSAGES)