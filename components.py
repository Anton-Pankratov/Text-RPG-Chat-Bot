from aiogram import F, Dispatcher
from aiogram.filters import Command

from chat_bot import ChatBot
from commands.start import start, handle_show_user_messages_button_click
from features.keyboard.keyboard_checklist import update_checklist_after_click, ChecklistCallback
from features.keyboard.keyboard_click_handler import handle_keyboard_clicks

from features.message_handle.incoming_user_message import handle_incoming_user_message

from src.properties import CHAT_BOT_COMMAND_START, BUTTON_CALLBACK_COMMON_TAG, CHECKLIST_TAG_CHECK_UPDATE
from src.strings import TEXT_BUTTON_COMMAND_START_SHOW_USER_MESSAGES, \
    TEXT_BUTTON_COMMAND_START_SHOW_UNPROCESSED_MESSAGES, TEXT_BUTTON_COMMAND_START_CREATE_TASK_OF_NEED_BID
from utils.parser_env_properties import get_bot_token

chat_bot = ChatBot(token=get_bot_token())
dispatcher_chat_bot = Dispatcher()

dispatcher_chat_bot.message.register(start, Command(CHAT_BOT_COMMAND_START))  # , FilterIsPrivateChat())
dispatcher_chat_bot.message.register(handle_show_user_messages_button_click,
                                     F.text.contains(TEXT_BUTTON_COMMAND_START_SHOW_USER_MESSAGES) |
                                     F.text.contains(
                                         TEXT_BUTTON_COMMAND_START_SHOW_UNPROCESSED_MESSAGES) | F.text.contains(
                                         TEXT_BUTTON_COMMAND_START_CREATE_TASK_OF_NEED_BID))

dispatcher_chat_bot.message.register(handle_incoming_user_message, F.text)

dispatcher_chat_bot.callback_query.register(update_checklist_after_click, F.data.contains(CHECKLIST_TAG_CHECK_UPDATE))

dispatcher_chat_bot.callback_query.register(handle_keyboard_clicks, F.data.contains(BUTTON_CALLBACK_COMMON_TAG))
