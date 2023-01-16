from random import shuffle
from typing import List

from card_value import Card_Value
from suit import Suit
from card import Card


class Deck:
    def __init__(self) -> None:
        self.deck: List[Card] = []
        for suit in Suit:
            if suit == Suit.NOTRUMPS:
                continue
            for value in Card_Value:
                self.deck.append(Card(suit, value))
        shuffle(self.deck)

    def deal_card(self) -> Card:
        return self.deck.pop()

    @staticmethod
    def compare_cards(lead: Suit, cards: List[Card], trumps: Suit) -> Card:
        for card in cards:
            if card.suit == lead:
                card.priority = 2
            elif card.suit == trumps:
                card.priority = 3
        winning_card = sorted(
            cards,
            key=lambda x: (x.priority, x.card_value.value),
            reverse=True,
        )[0]
        return winning_card
