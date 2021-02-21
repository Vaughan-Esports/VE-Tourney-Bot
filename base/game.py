from abc import ABC
from typing import List

import discord

from map import Map


class Game(ABC):
    """
    Base game class, represents a game object
    """

    def __init__(self, match_num: int, map_pool: List[Map]):
        self.match_num = match_num
        self.map_pool = map_pool

        self.name = f'Game {match_num}'

        self.selected_map: Map
        self.winner: discord.Member
