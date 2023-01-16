from typing import Dict, List
from collections import defaultdict


class ScoreCard:
    def __init__(self, number_of_rounds: int, player_names: List[str]) -> None:
        scorecard = Dict[str, Dict[int, Dict[str, int]]]
        self._scorecard: scorecard = defaultdict(lambda: defaultdict(dict))
        self.number_of_rounds = number_of_rounds
        for player_name in player_names:
            for number_of_cards in range(number_of_rounds, 0, -1):
                for value in ["Bid", "Taken", "Points"]:
                    self._scorecard[player_name][number_of_cards][value] = 0

    def get_bid(self, player_name: str, number_of_cards: int) -> int:
        return self._scorecard[player_name][number_of_cards]["Bid"]

    def get_tricks_taken(self, player_name: str, number_of_cards: int) -> int:
        return self._scorecard[player_name][number_of_cards]["Taken"]

    def get_round_score(self, player_name: str, number_of_cards: int) -> int:
        return self._scorecard[player_name][number_of_cards]["Points"]

    def get_total_scores(self) -> Dict[str, int]:
        scores: Dict[str, int] = {}
        for player in self._scorecard:
            total_score = sum(
                self._scorecard[player][i]["Points"]
                for i in range(self.number_of_rounds, 0, -1)
            )
            scores[player] = total_score
        return scores

    def set_bid(self, player_name: str, number_of_cards: int, bid: int) -> None:
        self._scorecard[player_name][number_of_cards]["Bid"] = bid

    def add_trick(self, player_name: str, number_of_cards: int) -> None:
        self._scorecard[player_name][number_of_cards]["Taken"] += 1

    def update_scores(self, number_of_cards: int) -> None:
        for player_name in self._scorecard:
            scorecard_row = self._scorecard[player_name][number_of_cards]
            scorecard_row["Points"] += scorecard_row["Taken"]

            if scorecard_row["Bid"] == scorecard_row["Taken"]:
                scorecard_row["Points"] += 10
