from data.data_bid_status import BidStatusData
from db import db
from utils.enums.extract_enum_code import extract_enum_code
from utils.enums.status import BidStatus


async def save_bid_status(user_id: int, actual_message_row_id: int, status_code: int):
    await db.manager_bid_handler.save_bid_status(
        BidStatusData(
            user_id=user_id,
            actual_message_row_id=actual_message_row_id,
            bid_status_code=status_code
        )
    )


async def update_bid_status(actual_message_row_id: int, status: BidStatus):
    await db.manager_bid_handler.update_bid_status(status=status, message_row_id=actual_message_row_id)


async def get_all_messages_by_bid_status(status: BidStatus):
    return await db.manager_bid_handler.get_all_messages_by_bid_status(status=extract_enum_code(status))


async def get_user_messages_by_bid_status(user_id: int, status: BidStatus):
    return await db.manager_bid_handler.get_user_messages_by_bid_status(user_id=user_id,
                                                                        status=extract_enum_code(status))
