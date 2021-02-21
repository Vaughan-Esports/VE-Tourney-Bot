from abc import ABC
from typing import List

import discord

from base.map import Map


class Game(ABC):
    """
    Base game class, represents a game object
    """

    def __init__(self, game_num: int, map_pool: List[Map]):
        """
        Constructor method for a game
        :param game_num: game number (starts at 0)
        :param map_pool: List of maps for the game
        """

        self.match_num = game_num
        self.map_pool = map_pool

        self.name = f'Game {game_num + 1}'

        self.selected_map: Map
        self.winner: discord.Member
