from typing import Dict, List
from collections import defaultdict


class ScoreCard:
    def __init__(self, number_of_rounds: int, player_names: List[str]) -> None:
        scorecard = Dict[str, Dict[int, ScoreCardEntry]]
        self._scorecard: scorecard = defaultdict(dict)
        self.number_of_rounds = number_of_rounds
        for player_name in player_names:
            for number_of_cards in range(number_of_rounds, 0, -1):
                self._scorecard[player_name][number_of_cards] = ScoreCardEntry()

    def get_bid(self, player_name: str, number_of_cards: int) -> int:
        return self._scorecard[player_name][number_of_cards].get_bid()

    def get_tricks_taken(self, player_name: str, number_of_cards: int) -> int:
        return self._scorecard[player_name][number_of_cards].get_tricks_taken()

    def get_round_score(self, player_name: str, number_of_cards: int) -> int:
        return self._scorecard[player_name][number_of_cards].get_points()

    def get_total_scores(self) -> Dict[str, int]:
        scores: Dict[str, int] = {}
        for player in self._scorecard:
            total_score = sum(
                self._scorecard[player][i].get_points()
                for i in range(self.number_of_rounds, 0, -1)
            )
            scores[player] = total_score
        return scores

    def set_bid(self, player_name: str, number_of_cards: int, bid: int) -> None:
        self._scorecard[player_name][number_of_cards].set_bid(bid)

    def add_trick(self, player_name: str, number_of_cards: int) -> None:
        self._scorecard[player_name][number_of_cards].add_trick()

    def update_scores(self, number_of_cards: int) -> None:
        for player_name in self._scorecard:
            self._scorecard[player_name][number_of_cards].update_score()


class ScoreCardEntry:
    def __init__(self) -> None:
        self.bid = 0
        self.taken = 0
        self.points = 0

    def get_bid(self) -> int:
        return self.bid

    def set_bid(self, bid) -> None:
        self.bid = bid

    def get_tricks_taken(self) -> int:
        return self.taken

    def add_trick(self) -> None:
        self.taken += 1

    def get_points(self) -> int:
        return self.points

    def update_score(self) -> None:
        self.points += self.taken
        if self.bid == self.taken:
            self.points += 10
