import json
from typing import Dict

from dotenv import load_dotenv
import os

from data.data_registered_chat import Chat
from data.data_registred_player import Player

load_dotenv()

ENV_TOKEN_TG_BOT = "TOKEN_TG_BOT"

ENV_CLIENT_SESSION = "CLIENT_SESSION"
ENV_CLIENT_TG_API_ID = "CLIENT_API_ID"
ENV_CLIENT_TG_API_HASH = "CLIENT_API_HASH"

ENV_RPG_CHATS = "RPG_CHATS"
ENV_PLAYERS = "PLAYERS"
ENV_MODERATOR_ID = "MODERATOR_ID"

def get_bot_token() -> str:
    return os.getenv(ENV_TOKEN_TG_BOT)

def get_client_api_credentials() -> (str, int, str):
    return os.getenv(ENV_CLIENT_SESSION), os.getenv(ENV_CLIENT_TG_API_ID), os.getenv(ENV_CLIENT_TG_API_HASH)

def get_moderator_id() -> int:
    return int(os.getenv(ENV_MODERATOR_ID))

def get_chats() -> Dict[int, Chat]:
    raw_chats = os.getenv(ENV_RPG_CHATS)
    if not raw_chats:
        raise ValueError(f"Переменная среды {ENV_RPG_CHATS} не найдена!")

    try:
        parsed_chats = json.loads(raw_chats)
    except json.JSONDecodeError as e:
        raise ValueError(f"Переменную среды {ENV_RPG_CHATS} невозможно распарсить в JSON!") from e

    return {
        int(key): Chat(
            id=data["id"],
            topic_id=data["topic_id"],
            name=data["name"]
        )
        for key, data in parsed_chats.items()
    }

def get_players() -> Dict[int, Player]:
    raw_players = os.getenv(ENV_PLAYERS)

    if not raw_players:
        raise ValueError(f"Переменная среды {ENV_PLAYERS} не найдена!")

    try:
        parsed_chats = json.loads(raw_players)
    except json.JSONDecodeError as e:
        raise ValueError(f"Переменную среды {ENV_PLAYERS} невозможно распарсить в JSON!") from e

    return {
        int(key): Player(
            name=data["name"],
            chats=data["chats"]
        )
        for key, data in parsed_chats.items()
    }