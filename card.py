from suit import Suit
from card_value import CardValue


class Card:
    def __init__(self, suit: Suit, value: CardValue) -> None:
        self.suit = suit
        self.card_value = value
        # Priority is increased when leading or trumping
        self.priority = 1

    def __repr__(self) -> str:
        return f"{self.card_value.name} of {self.suit.name}"
