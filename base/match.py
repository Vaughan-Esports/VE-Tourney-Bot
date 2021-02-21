from abc import ABC
from typing import List

import discord.ext.commands

from base.game import Game


class Match(ABC):
    """
    Base class representing a match
    """

    def __init__(self, players, num_of_games: int,
                 ctx: discord.ext.commands.Context,
                 bot: discord.ext.commands.Bot,
                 main_message: discord.Message,
                 embed: discord.Embed):
        """
        Constructs a match object
        :param players: list of players
        :param num_of_games: max number of games
        :param ctx: message context
        :param bot: bot object to use
        :param main_message: main message to use
        :param embed: embed to use
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

        # objects for veto
        self.ctx = ctx
        self.bot = bot
        self.main_message = main_message
        self.embed = embed
