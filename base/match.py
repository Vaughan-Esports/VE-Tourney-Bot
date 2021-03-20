from abc import ABC
from typing import List

from base.game import Game
from smash.player import Player


class Match(ABC):
    """
    Base class representing a match
    """

    def __init__(self, players: List[Player], num_of_games: int, ):
        """
        Constructs a match object
        :param players: list of players
        :param num_of_games: max number of games
        """
        # players
        self.players = players

        # match data
        self.games: List[Game]
        self.name: str
        self.description: str

        # match state
        self.num_of_games: int = num_of_games
        self.current_game: int = 0
