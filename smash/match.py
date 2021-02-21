from typing import List

import discord.ext.commands

from base.match import Match
from smash.player import Player


class Match(Match):
    """
    Represents a Smash match
    """

    def __init__(self, players: List[Player], num_of_games: int,
                 ctx: discord.ext.commands.Context,
                 bot: discord.ext.commands.Bot,
                 main_message: discord.Message,
                 embed: discord.Embed):
        super().__init__(players, num_of_games, ctx, bot, main_message, embed)

        # generate blank games
