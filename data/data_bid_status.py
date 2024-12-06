from dataclasses import dataclass

@dataclass
class BidStatusData:
    user_id: int
    actual_message_row_id: int
    bid_status_code: int