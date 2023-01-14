import random
from abc import ABC, abstractmethod
from typing import List, Dict

from suit import Suit
from card import Card
from validation import BidValidation, TurnValidation

Scorecard = Dict[str, Dict[int, Dict[str, int]]]


class Player(ABC):
    """Base Class from which human and bot players inherit from."""

    def __init__(self, player_name: str) -> None:
        self.hand: List[Card] = []
        self.player_name = player_name
        super().__init__()

    def __repr__(self) -> str:
        return self.player_name

    def pre_game_init(
        self, number_of_rounds: int, number_of_players: int, scorecard: Scorecard
    ) -> None:
        self.scorecard: Scorecard = scorecard
        self.number_of_rounds = number_of_rounds
        self.number_of_players = number_of_players

    def add_card(self, card: Card) -> None:
        self.hand.append(card)

    def remove_card(self, card: Card) -> None:
        self.hand.pop(self.hand.index(card))

    def reset(self) -> None:
        self.hand = []

    def update_scores(self, scorecard: Scorecard) -> None:
        self.scorecard = scorecard

    def get_scores(self) -> Dict[str, int]:
        scores: Dict[str, int] = {}
        for player in self.scorecard:
            total_score = sum(
                self.scorecard[player][i]["Points"]
                for i in range(self.number_of_rounds, 0, -1)
            )
            scores[player] = total_score
        return scores

    def sort_hand(self) -> None:
        self.hand.sort(key=lambda x: (x.suit.value, x.card_value.value))

    def validate_bid(self, bid: str, current_bids: List[int]) -> BidValidation | None:
        if not bid.isnumeric():
            return BidValidation.NotNumeric

        int_bid = int(bid)
        if not 0 <= int_bid <= len(self.hand):
            return BidValidation.OutOfRange

        if (
            int_bid + sum(current_bids) == len(self.hand)
            and len(current_bids) == self.number_of_players - 1
        ):
            return BidValidation.RestrictedBid

    def validate_turn(
        self, card_idx: int, cards_played: List[Card]
    ) -> TurnValidation | None:
        if not card_idx.isnumeric():
            return TurnValidation.NotNumeric

        int_card_idx = int(card_idx)
        if not 0 <= int_card_idx <= len(self.hand) - 1:
            return TurnValidation.OutOfRange

        card = self.hand[int_card_idx]
        if (
            cards_played
            and cards_played[0].suit != card.suit
            and any(card for card in self.hand if card.suit == cards_played[0].suit)
        ):
            return TurnValidation.RestrictedSuit

    @abstractmethod
    def bid(self, trumps: Suit, current_bids: List[int]) -> int:
        """Choose a number of tricks to bid"""

    @abstractmethod
    def play_turn(self, trumps: Suit, cards_played: List[Card]) -> Card:
        """Return a card from self.hand to play"""

    @abstractmethod
    def post_round(self, scorecard: Scorecard) -> None:
        """Handles post round events"""


class RandomBot(Player):
    def bid(self, trumps: Suit, current_bids: List[int]) -> int:
        possible_bids = list(range(0, len(self.hand) + 1))
        if len(current_bids) == self.number_of_players - 1:
            restricted_bid = len(self.hand) - sum(current_bids)
            if restricted_bid in possible_bids:
                possible_bids.pop(possible_bids.index(restricted_bid))
        return random.choice(possible_bids)

    def play_turn(self, trumps: Suit, cards_played: List[Card]) -> Card:
        if not cards_played:
            return random.choice(self.hand)

        lead_suit_cards = [
            card for card in self.hand if card.suit == cards_played[0].suit
        ]
        if lead_suit_cards:
            return random.choice(lead_suit_cards)

        return random.choice(self.hand)

    def post_round(self, scorecard: Scorecard) -> None:
        self.update_scores(scorecard)


class HumanInputPlayer(Player):
    def bid(self, trumps: Suit, current_bids: List[int]) -> int:
        status = f"There are {self.number_of_players} players. "
        status += f"{trumps.name} are trumps.\n"
        if current_bids:
            status += f"The current bids are: {', '.join(map(str, current_bids))}\n"
        else:
            status += "You are leading.\n"
        status += f"Your hand is {self.hand}\n"
        print(status)
        while True:
            number_bid = input("How many would you like to bid? ").strip()
            print()
            validation = self.validate_bid(number_bid, current_bids)
            match validation:
                case BidValidation.NotNumeric:
                    print("Your bid must be a number!\n")
                    continue
                case BidValidation.OutOfRange:
                    print(f"Your bid must be be between 0 and {len(self.hand)}\n")
                    continue
                case BidValidation.RestrictedBid:
                    print(f"That bid is not allowed!\n")
                    continue

            return int(number_bid)

    def play_turn(self, trumps: Suit, cards_played: List[Card]) -> Card:
        status = f"There are {self.number_of_players} players. "
        status += f"{trumps.name} are trumps.\n"
        if cards_played:
            status += (
                f"The current cards played are: {', '.join(map(str, cards_played))}\n"
            )
        else:
            status += "You are leading.\n"
        status += f"Your hand is {self.hand}\n"
        print(status)
        while True:
            card_idx = input(
                "Select the index of the card that you would like to play: "
            ).strip()
            print()
            validation = self.validate_turn(card_idx, cards_played)
            match validation:
                case TurnValidation.NotNumeric:
                    print("Enter a number!\n")
                    continue
                case TurnValidation.OutOfRange:
                    print("That index is outside of the range of your hand!\n")
                    continue
                case TurnValidation.RestrictedSuit:
                    print("You have to follow suit!\n")
                    continue

            return self.hand[int(card_idx)]

    def post_round(self, scorecard: Scorecard) -> None:
        self.update_scores(scorecard)
        self.print_scores()
        self.sort_hand()

    def print_scores(self) -> None:
        print("Scores: ")
        scores = self.get_scores()
        for player in scores:
            print(f"{player}: {scores[player]}")
        print()
