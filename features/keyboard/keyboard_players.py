from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.data_registred_player import Player
from src.properties import BUTTON_CALLBACK_TAG_PLAYER_MESSAGES
from utils.parser_env_properties import get_players


def keyboard_players() -> InlineKeyboardMarkup:
    players = get_players()
    builder = InlineKeyboardBuilder()
    for player_id, player in players.items():
        builder.row(InlineKeyboardButton(text=f"{player.name}",
                                         callback_data=f"{BUTTON_CALLBACK_TAG_PLAYER_MESSAGES}{str(player_id)}"))
    return builder.as_markup()

def keyboard_players_in_chat(player_ids: dict[int, Player]):
    builder = InlineKeyboardBuilder()
    for player_id, player in player_ids:
        builder.row(InlineKeyboardButton(text=f"{player.name}", callback_data=f"{BUTTON_CALLBACK_TAG_PLAYER_MESSAGES}{str(player_id)}"))
    return builder.as_markup()