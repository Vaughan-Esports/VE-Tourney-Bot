import discord

from smash.stage import Stage


class Player:
    """
    Represents a player in a Smash match
    """

    def __init__(self, user: discord.Member):
        self.name = user.display_name
        self.mention = user.mention

        self.dsr: Stage
