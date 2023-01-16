from typing import Dict, List

from suit import Suit
from card import Card
from deck import Deck
from player import Player
from scorecard import ScoreCard


class Game:
    def __init__(self, number_of_rounds: int, players: List[Player]) -> None:
        assert number_of_rounds * len(players) <= 52
        self.number_of_rounds = number_of_rounds
        self.current_number_of_cards = number_of_rounds
        self.players = players
        self.number_of_players = len(players)
        self.trumps = Suit.CLUBS if number_of_rounds % 10 == 0 else Suit.HEARTS
        self.round_leader = players[0]
        player_names = [player.player_name for player in self.players]
        self.scorecard = ScoreCard(self.number_of_rounds, player_names)
        self.player_pre_game_init()

    def start_game(self) -> None:
        while self.current_number_of_cards > 0:
            self.prepare_round()
            self.bidding()
            self.play_round()
            self.cleanup()
            self.current_number_of_cards -= 1

    def prepare_round(self) -> None:
        self.deck = Deck()
        self.deal_cards()

    def deal_cards(self) -> None:
        for player in self.players:
            for _ in range(self.current_number_of_cards):
                player.add_card(self.deck.deal_card())
            player.sort_hand()

    def rotate_players(self) -> None:
        self.players = self.players[1:] + self.players[:1]

    def bidding(self) -> None:
        current_bids: List[int] = []
        for player in self.players:
            number_bid = player.bid(self.trumps, current_bids)
            self.scorecard.set_bid(
                player.player_name, self.current_number_of_cards, number_bid
            )
            current_bids.append(number_bid)

    def play_round(self) -> None:
        for _ in range(self.current_number_of_cards):
            trick_winner = self.play_trick()
            self.scorecard.add_trick(
                trick_winner.player_name, self.current_number_of_cards
            )
            # Rotate players until trick winner is leading
            while self.players[0] != trick_winner:
                self.rotate_players()

    def play_trick(self) -> Player:
        self.current_trick: Dict[Card, Player] = {}
        cards_played: List[Card] = []
        for player in self.players:
            card_played = player.play_turn(self.trumps, cards_played)
            if player == self.players[0]:
                self.lead = card_played.suit
            player.remove_card(card_played)
            self.current_trick[card_played] = player
            cards_played.append(card_played)
        winning_player = self.evaluate_trick()
        return winning_player

    def evaluate_trick(self) -> Player:
        cards = [card for card in self.current_trick]
        winning_card = self.deck.compare_cards(
            lead=self.lead, cards=cards, trumps=self.trumps
        )
        return self.current_trick[winning_card]

    def cleanup(self) -> None:
        self.scorecard.update_scores(self.current_number_of_cards)
        self.post_round_event()
        if self.current_number_of_cards == 1:
            return

        for player in self.players:
            player.reset()

        # Leader of previous round now plays last
        while self.players[-1] != self.round_leader:
            self.rotate_players()
        self.round_leader = self.players[0]
        self.trumps = self.trumps.next()

    def player_pre_game_init(self) -> None:
        for player in self.players:
            player.pre_game_init(
                self.number_of_rounds, self.number_of_players, self.scorecard
            )

    def post_round_event(self) -> None:
        for player in self.players:
            player.post_round(self.scorecard)
