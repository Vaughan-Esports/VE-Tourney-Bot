from abc import ABC
from typing import List

import discord

from map import Map


class Game(ABC):
    """
    Base game class, represents a game object
    """

    def __init__(self, match_num: str, map_pool: List[Map]):
        self.match_num = match_num
        self.map_pool = map_pool

        self.selected_map: Map
        self.winner: discord.Member
