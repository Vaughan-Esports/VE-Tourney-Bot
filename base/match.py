from abc import ABC
from typing import List

from discord import Member

from base.game import Game


class Match(ABC):
    """
    Base class representing a match
    """

    def __init__(self, players: List[Member], num_of_games: int):
        self.players = players
        self.games: List[Game]
