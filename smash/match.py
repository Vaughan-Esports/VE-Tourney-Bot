from typing import List

from smash.game import Game
from smash.player import Player


class Match:
    """
    Represents a Smash match
    """

    def __init__(self, player1: Player, player2: Player, num_of_games: int):
        # players
        self.player1 = player1
        self.player2 = player2

        # match data
        self.games: List[Game]
        self.name: str
        self.description: str

        # match state
        self.num_of_games: int = num_of_games
        self.current_game: int = 0

        # generate blank games
        for x in range(num_of_games):
            self.games.append(Game(x))
