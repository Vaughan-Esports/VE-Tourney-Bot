from typing import List

from base.match import Match
from smash.game import Game
from smash.player import Player


class Match(Match):
    """
    Represents a Smash match
    """

    def __init__(self, players: List[Player], num_of_games: int, ):
        super().__init__(players, num_of_games)

        # generate blank games
        self.games: List[Game] = []
        self.game_num = 0
        for x in range(num_of_games):
            self.games.append(Game(x))
