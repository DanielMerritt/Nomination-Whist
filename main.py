from player import RandomBot, HumanInputPlayer
from game import Game


def main() -> None:
    player1 = HumanInputPlayer("Dan")
    player2 = RandomBot("Bob")
    player3 = RandomBot("Charlie")
    player4 = RandomBot("Dave")

    game = Game(number_of_rounds=3, players=[player1, player2, player3, player4])
    game.start_game()


if __name__ == "__main__":
    main()
