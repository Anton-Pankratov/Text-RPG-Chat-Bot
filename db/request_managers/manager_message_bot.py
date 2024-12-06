from data.data_message_bot import MessageBotData
from db.tables.message_bot import DATABASE_REQUEST_SAVE_MESSAGE_BOT, DATABASE_REQUEST_GET_BOT_MESSAGE, \
    DATABASE_REQUEST_DELETE_BOT_MESSAGE
from utils.enums.tag import Tags


class DbManagerBotMessage:

    def __init__(self, db_chat_bot):
        self.db_chat_bot = db_chat_bot

    async def save_bot_message(self, message: MessageBotData):
        await self.db_chat_bot.transaction(
            DATABASE_REQUEST_SAVE_MESSAGE_BOT,
            (message.chat_id, message.topic_id, message.user_id, message.message_tag, message.message_id)
        )

    async def get_bot_messages(self, chat_id: int, topic_id: int):
        async with self.db_chat_bot.transaction_result(DATABASE_REQUEST_GET_BOT_MESSAGE,
                                                       (chat_id, topic_id)) as cursor:
            rows = await cursor.fetchall()

            data = [
                MessageBotData(
                    chat_id=row[1], topic_id=row[2], user_id=row[3], message_tag=row[4], message_id=row[5]
                ) for row in rows
            ]

            if rows:
                await self.db_chat_bot.transaction(DATABASE_REQUEST_DELETE_BOT_MESSAGE, (chat_id, topic_id))

            return data
