from dataclasses import dataclass
from typing import Dict


@dataclass
class Player:
    name: str
    chats: list[int]


@dataclass
class RegisteredPlayerData:
    players: Dict[int, Player]