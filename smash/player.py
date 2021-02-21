import discord


class Player:
    """
    Represents a player in a Smash match
    """

    def __init__(self, user: discord.Member):
        self.name = user.display_name
        self.mention = user.mention

        self.dsr = None

    def __eq__(self, other: discord.Member) -> bool:
        """
        Compares self to discord member
        :param other: Discord member to check
        :return: boolean for whether they are the same
        """
        return self.mention == other.mention
