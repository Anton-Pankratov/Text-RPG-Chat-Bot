from data.data_message_user import MessageUserData
from db.tables.message_user import DATABASE_REQUEST_SAVE_MESSAGE_USER, \
    DATABASE_REQUEST_GET_USER_MESSAGE_ROW_ID, DATABASE_REQUEST_DELETE_USER_MESSAGE, DATABASE_REQUEST_GET_USER_IDS_COUNT, \
    DATABASE_REQUEST_GET_USER_IDS, DATABASE_REQUEST_GET_MESSAGES_BY_ENCRYPTED_USER_IDS
from security.cipher import encrypt_text, decrypt_text


class DbManagerUserMessages:

    def __init__(self, db_chat_bot):
        self.db_chat_bot = db_chat_bot

    async def save_user_message(self, message: MessageUserData) -> int:
        encrypted_chat_id = encrypt_text(str(message.chat_id))
        encrypted_topic_id = encrypt_text(str(message.topic_id))
        encrypted_user_id = encrypt_text(str(message.user_id))
        encrypted_message_id = encrypt_text(str(message.message_id))
        encrypted_user_text = encrypt_text(message.message_text)

        cursor = await self.db_chat_bot.database.execute(
            DATABASE_REQUEST_SAVE_MESSAGE_USER,
            (encrypted_chat_id, encrypted_topic_id, encrypted_user_id,
             encrypted_message_id, encrypted_user_text)
        )

        await self.db_chat_bot.database.commit()

        return cursor.lastrowid

    async def get_all_user_ids(self):
        all_user_ids = {}
        limit = 1000
        offset = 0

        async with self.db_chat_bot.database.execute(DATABASE_REQUEST_GET_USER_IDS_COUNT) as cursor:
            total_rows = await cursor.fetchone()
            total_records = total_rows[0] if total_rows else 0

        while offset < total_records:
            async with self.db_chat_bot.database.execute(DATABASE_REQUEST_GET_USER_IDS, (limit, offset)) as cursor:
                rows = await cursor.fetchall()

                for row in rows:
                    all_user_ids[row[0]] = int(decrypt_text(row[0]))

            offset += limit

        return all_user_ids

    async def get_all_user_messages(self, user_id: int):
        db_all_user_ids = await self.get_all_user_ids()
        db_encrypted_ids = []

        for encrypted_id, db_user_id in db_all_user_ids.items():
            if db_user_id == user_id:
                db_encrypted_ids.append(encrypted_id)

        user_ids_placeholder = ', '.join(['?'] * len(db_encrypted_ids))
        async with self.db_chat_bot.database.execute(
                DATABASE_REQUEST_GET_MESSAGES_BY_ENCRYPTED_USER_IDS(user_ids_placeholder), db_encrypted_ids) as cursor:
            rows = await cursor.fetchall()

            decrypted_rows = []

            for row in rows:
                db_row_id = row[0]
                chat_id = decrypt_text(row[1])
                topic_id = decrypt_text(row[2])
                user_id = decrypt_text(row[3])
                message_id = decrypt_text(row[4])
                message_text = decrypt_text(row[5])

                decrypted_row = MessageUserData(
                    db_row_id=db_row_id,
                    chat_id=int(chat_id) if chat_id else None,
                    topic_id=int(topic_id) if topic_id else None,
                    user_id=int(user_id) if user_id else None,
                    message_id=int(message_id) if message_id else None,
                    message_text=message_text
                )

                decrypted_rows.append(decrypted_row)

        return decrypted_rows

    async def get_user_message_row_id(self, chat_id: int, topic_id: int, message_id: int, user_id: int):
        async with self.db_chat_bot.database.execute(DATABASE_REQUEST_GET_USER_MESSAGE_ROW_ID,
                                                     (chat_id, topic_id, message_id, user_id)) as cursor:
            row = await cursor.fetchone()

            await self.db_chat_bot.database.commit()

            if row:
                return row[0]
            return None

    async def delete_user_message(self, row_id: int):
        await self.db_chat_bot.database.execute(DATABASE_REQUEST_DELETE_USER_MESSAGE, (row_id,))
        await self.db_chat_bot.database.commit()
