from abc import ABC

import discord

from base.map import Map


class Game(ABC):
    """
    Base game class, represents a game object
    """

    def __init__(self, game_num: int):
        """
        Constructor method for a game
        :param game_num: game number (starts at 0)
        """
        self.match_num = game_num

        self.name = f'Game {game_num + 1}'

        self.selected_map: Map
        self.winner: discord.Member
