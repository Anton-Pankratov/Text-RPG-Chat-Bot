
def handle_chat_id_text(chat_id: int) -> int:
    str_chat_id = str(chat_id)
    if str_chat_id.startswith("-100"):
        return int(str_chat_id.removeprefix("-100"))
    elif str_chat_id.startswith("-"):
        return int(str_chat_id.removeprefix("-"))
    else: return int(chat_id)