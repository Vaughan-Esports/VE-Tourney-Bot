from typing import List

import discord

from smash.stage import Stage


class Player:
    """
    Represents a player in a Smash match
    """

    def __init__(self, user: discord.Member):
        """
        Constructor method for a Smash Player
        :param user: Discord user to grab info from
        """
        self.name = user.display_name
        self.mention = user.mention

        # list of DSR stages
        self.dsr: List[Stage] = []

    def __eq__(self, other: discord.Member) -> bool:
        """
        Compares self to discord member
        :param other: Discord member to check
        :return: boolean for whether they are the same
        """
        return self.mention == other.mention
