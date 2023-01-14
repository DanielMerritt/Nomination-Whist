from enum import Enum


class Suit(Enum):
    HEARTS: int = 0
    CLUBS: int = 1
    DIAMONDS: int = 2
    SPADES: int = 3
    NOTRUMPS: int = 4

    def next(self):
        new_idx = (self.value + 1) % 5
        return Suit(new_idx)
