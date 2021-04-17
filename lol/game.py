from lol.champ_pool import ChampPool


class Game:
    """
    Represents a League of Legends ARAM Game
    """

    def __init__(self, game_num: int):
        self.name = f"`                    " \
                    f"Game {game_num + 1}" \
                    f"                     `"

        self.selected_stage = None
        self.winner = None

        self.team1_champ_pool = ChampPool()
        self.team2_champ_pool = ChampPool()

    @property
    def winner_embed(self) -> str:
        """
        Generate embed string for winner line
        :return:
        """
        message = "**Winner:**"
        if self.winner is None:
            return f"{message} TBD"
        else:
            return f"{message} {self.winner.mention}"

    @property
    def team1_embed(self) -> str:
        """
        Embed string for team1 Champs
        :return:
        """
        message = ""
        # loop through champ names
        for champ in self.team1_champ_pool.champions:
            # append each name to a new line in the message
            message = f'{message}{champ}\n'
        # return message string
        return message

    @property
    def team2_embed(self) -> str:
        """
        Embed string for team2 Champs
        :return:
        """
        message = ""
        # loop through champ names
        for champ in self.team2_champ_pool.champions:
            # append each name to a new line in the message
            message = f'{message}{champ}\n'
        # return message string
        return message

    def reroll_team1_champs(self):
        """
        Recreates new team1 champ pool
        :return:
        """
        self.team1_champ_pool = ChampPool()

    def reroll_team2_champs(self):
        """
        Recreates new team2 champ pool
        :return:
        """
        self.team2_champ_pool = ChampPool()
