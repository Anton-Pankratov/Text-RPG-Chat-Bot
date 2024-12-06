from src.properties import MESSAGE_SHORT_TEXT_ROW_LENGTH


def shorten_text(text: str, max_length = MESSAGE_SHORT_TEXT_ROW_LENGTH) -> str:
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text