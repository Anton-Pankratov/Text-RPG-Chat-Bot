from dataclasses import dataclass
from typing import Dict


@dataclass
class Chat:
    id: int
    topic_id: int
    name: str


@dataclass
class RegisteredChatData:
    chats: Dict[int, Chat]
