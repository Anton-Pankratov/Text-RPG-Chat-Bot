import json
from dataclasses import asdict

from data.data_message_user import MessageUserData


def pack_user_message_data(message: MessageUserData) -> str:
    return json.dumps(asdict(message))

def unpack_user_message_data(packed_message: str) -> MessageUserData:
    data = json.loads(packed_message)
    return MessageUserData(**data)