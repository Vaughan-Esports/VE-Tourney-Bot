from base.game import Game
from smash.stage import Stage
from smash.stagelist import StageList


class Game(Game):
    """
    Represents a Smash game
    """

    def __init__(self, game_num: int):
        self.name = f"`                         " \
                    f"Game {game_num + 1}" \
                    f"                            `"

        self.selected_map: Stage
        self.winner = None

        self.stagelist: StageList = StageList()
        # stage veto / selection process state
        self.state = 0

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
