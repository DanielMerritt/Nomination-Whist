from enum import Enum, auto


class BidValidation(Enum):
    NotNumeric = auto()
    OutOfRange = auto()
    RestrictedBid = auto()


class TurnValidation(Enum):
    NotNumeric = auto()
    OutOfRange = auto()
    RestrictedSuit = auto()
