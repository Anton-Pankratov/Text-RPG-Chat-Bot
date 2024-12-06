from contextlib import asynccontextmanager

import aiosqlite

from db.db_properties import DATABASE_FILE_NAME
from db.request_managers.manager_bid_handler import DbManagerBidHandler
from db.request_managers.manager_message_bot import DbManagerBotMessage
from db.request_managers.manager_message_user import DbManagerUserMessages
from db.tables.bid_status import DATABASE_REQUEST_CREATE_BID_STATUS
from db.tables.message_bot import DATABASE_REQUEST_CREATE_MESSAGE_BOT
from db.tables.message_user import DATABASE_REQUEST_CREATE_TABLE_MESSAGE_USER, DATABASE_REQUEST_CREATE_USER_ID_INDEX


class DatabaseChatBot:

    def __init__(self):
        self.database = None
        self.manager_msg_user = DbManagerUserMessages(self)
        self.manager_msg_bot = DbManagerBotMessage(self)
        self.manager_bid_handler = DbManagerBidHandler(self)

    async def init_db(self):
        if self.database is None:
            self.database = await aiosqlite.connect(DATABASE_FILE_NAME)
            await self.database.execute(DATABASE_REQUEST_CREATE_TABLE_MESSAGE_USER)
            await self.database.execute(DATABASE_REQUEST_CREATE_USER_ID_INDEX)
            await self.database.execute(DATABASE_REQUEST_CREATE_MESSAGE_BOT)
            await self.database.execute(DATABASE_REQUEST_CREATE_BID_STATUS)
            await self.database.commit()

    async def transaction(self, query: str, params: tuple):
        await self.database.execute(query, params)
        await self.database.commit()

    @asynccontextmanager
    async def transaction_result(self, query: str, params: tuple):
        cursor = await self.database.execute(query, params)
        try:
            yield cursor
        finally:
            await cursor.close()

    async def close_db(self):
        if self.database is not None:
            await self.database.close()
            self.database = None