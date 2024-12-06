from aiogram import Bot, types

from src.properties import CHAT_BOT_COMMAND_START, CHAT_BOT_COMMAND_HELP
from src.strings import TEXT_BUTTON_COMMAND_START, TEXT_BUTTON_COMMAND_HELP

COMMAND_START = types.BotCommand(command=f"/{CHAT_BOT_COMMAND_START}", description=TEXT_BUTTON_COMMAND_START)
COMMAND_HELP = types.BotCommand(command=f"/{CHAT_BOT_COMMAND_HELP}", description=TEXT_BUTTON_COMMAND_HELP)

async def set_commands(bot: Bot):
    await bot.set_my_commands([COMMAND_START])