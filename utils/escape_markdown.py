import re


def escape_markdown_link(text: str) -> str:
    # Заменяем URL в тексте на "[ссылка](URL)" без экранирования URL
    text = re.sub(r'(https?://\S+)', r'[ссылка](\1)', text)
    return text.replace('#', "_")


def escape_markdown_text(text: str) -> str:
    """
    Экранирует текст для использования в формате MarkdownV2.
    """
    # Список символов, которые нужно экранировать в MarkdownV2
    special_chars = r'_*[\]()~`>#+\-=|{}.!\\'

    # Экранируем все символы из списка
    text = re.sub(f'([{re.escape(special_chars)}])', r'\\\1', text)

    # Возвращаем экранированный текст
    return text.replace("#", "*")