from data.data_bid_status import BidStatusData
from data.data_message_user import MessageUserData, message_user_data_fields_order
from db.db_properties import DATABASE_FIELD_USER_ID, DATABASE_FIELD_CHAT_ID, DATABASE_FIELD_TOPIC_ID, \
    DATABASE_FIELD_MESSAGE_USER_ID, DATABASE_FIELD_MESSAGE_TEXT
from db.tables.bid_status import DATABASE_REQUEST_SAVE_BID_STATUS, DATABASE_REQUEST_UPDATE_BID_STATUS, \
    DATABASE_REQUEST_GET_ALL_MESSAGES_BY_BID_STATUS, DATABASE_REQUEST_DELETE_BID_STATUS, \
    DATABASE_REQUEST_GET_USER_MESSAGES_BY_BID_STATUS
from security.cipher import decrypt_text
from utils.db_rows_mapper import map_db_rows


class DbManagerBidHandler:

    def __init__(self, db_chat_bot):
        self.db_chat_bot = db_chat_bot

    async def save_bid_status(self, data: BidStatusData):
        await self.db_chat_bot.transaction(DATABASE_REQUEST_SAVE_BID_STATUS,
                                           (data.user_id, data.actual_message_row_id, data.bid_status_code))

    async def update_bid_status(self, message_row_id: int, status: int):
        await self.db_chat_bot.transaction(DATABASE_REQUEST_UPDATE_BID_STATUS, (status, message_row_id))

    async def decrypt_rows(self, rows: list[(int, bytes, bytes, bytes, bytes, bytes)]):
        decrypted_rows = []

        for row in rows:
            db_row_id = row[0]
            chat_id = decrypt_text(row[1])
            topic_id = decrypt_text(row[2])
            user_id = decrypt_text(row[3])
            message_id = decrypt_text(row[4])
            message_text = decrypt_text(row[5])

            decrypted_row = (
                db_row_id,
                int(chat_id) if chat_id else None,
                int(topic_id) if topic_id else None,
                int(user_id) if user_id else None,
                int(message_id) if message_id else None,
                message_text
            )

            decrypted_rows.append(decrypted_row)

        return decrypted_rows

    async def get_all_messages_by_bid_status(self, status: int):
        async with self.db_chat_bot.transaction_result(DATABASE_REQUEST_GET_ALL_MESSAGES_BY_BID_STATUS,
                                                       (status,)) as cursor:
            rows = await cursor.fetchall()
            decrypted_rows = await self.decrypt_rows(rows)
            return await map_db_rows(MessageUserData, decrypted_rows, message_user_data_fields_order)

    async def get_user_messages_by_bid_status(self, user_id: int, status: int):
        async with self.db_chat_bot.transaction_result(DATABASE_REQUEST_GET_USER_MESSAGES_BY_BID_STATUS,
                                                       (user_id, status,)) as cursor:
            rows = await cursor.fetchall()
            decrypted_rows = await self.decrypt_rows(rows)
            return await map_db_rows(MessageUserData, decrypted_rows, message_user_data_fields_order)

    async def delete_bid_status(self, row_id: int):
        await self.db_chat_bot.transaction(DATABASE_REQUEST_DELETE_BID_STATUS, (row_id,))
