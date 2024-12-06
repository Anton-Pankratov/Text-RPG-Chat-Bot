from enum import Enum

from src.strings import TEXT_STATUS_CREATED, TEXT_STATUS_PROCESSING, TEXT_STATUS_CLARIFICATION, TEXT_STATUS_FINISHED


class BidStatus(Enum):
    CREATED = (1, TEXT_STATUS_CREATED)
    PROCESSING = (2, TEXT_STATUS_PROCESSING)
    CLARIFICATION = (3, TEXT_STATUS_CLARIFICATION)
    FINISHED = (4, TEXT_STATUS_FINISHED)

    def __init__(self, code, description):
        self.code = code
        self.description = description