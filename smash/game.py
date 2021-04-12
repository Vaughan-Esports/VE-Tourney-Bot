from smash.stagelist import StageList


class Game:
    """
    Represents a Smash game
    """

    def __init__(self, game_num: int):
        self.name = f"`                    " \
                    f"Game {game_num + 1}" \
                    f"                     `"

        self.selected_stage = None
        self.winner = None

        self.stagelist: StageList = StageList()

        # auto veto counters if first game
        if game_num == 0:
            for x in range(len(self.stagelist.counters)):
                self.stagelist.counters[x].veto = True

    def starters_embed(self) -> str:
        """
        Generate embed string for stagelist starters
        :return:
        """
        message = ""
        # loop through start stage names
        for x in range(len(self.stagelist.starters)):
            # append each name to a new line in the message
            message = f'{message}{self.stagelist.starters[x]}\n'
        # return message string
        return message

    def counters_embed(self) -> str:
        """
        Generate embed string for stagelist counters
        :return:
        """
        message = ""
        # loop through counter stage names
        for x in range(len(self.stagelist.counters)):
            # append each name to a new line in the message
            message = f'{message}{self.stagelist.counters[x]}\n'
        # return message string
        return message

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

    def choose_stage(self, stage: str):
        """
        Tries to choose a stage
        :param stage: name/alias of stage to chose
        """
        self.selected_stage = self.stagelist.choose(stage)

    def veto_stage(self, stage: str):
        """
        Tries to veto a stage
        :param stage: name/alias of stage to veto
        """
        self.stagelist.veto(stage)
