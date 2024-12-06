from aiogram.types import Message

from features.message_bot.save_message import save_bot_message
from features.task import task_manager
from src.strings import TEXT_MESSAGE_COMMAND_START_WARNING_TASK_IS_NOT_RUNNING
from utils.enums.tag import Tags
from utils.parser_env_properties import get_moderator_id


async def check_running_task(tg_user_message: Message):
    from components import chat_bot

    if task_manager.is_task_running():
        await task_manager.cancel_task()
    else:
        bot_message = await chat_bot.send_message(chat_id=get_moderator_id(),
                                                  text=TEXT_MESSAGE_COMMAND_START_WARNING_TASK_IS_NOT_RUNNING)
        await save_bot_message(tg_user_message=tg_user_message, tg_bot_message_id=bot_message.message_id,
                               message_tag=Tags.CALL_TO_BID)
