from aiogram import types

from features.action_bid_status import save_bid_status
from features.message_handle.save_user_message import save_user_message_aiogram
from features.message_moderation.show import show_moderation_message
from filters import is_allowed_message
from utils.enums.status import BidStatus
from utils.parser_env_properties import get_moderator_id


async def handle_incoming_user_message(message: types.Message):
    is_moderator_message = message.from_user.id == get_moderator_id()
    if is_allowed_message(message) or is_moderator_message:
        message_row_id = await save_user_message_aiogram(message)
        await show_moderation_message(message=message, user_message_row_id=message_row_id)

        if not is_moderator_message:
            if message.from_user.id != get_moderator_id():
                await save_bid_status(user_id=message.from_user.id, actual_message_row_id=message_row_id,
                                      status_code=BidStatus.CREATED.code)