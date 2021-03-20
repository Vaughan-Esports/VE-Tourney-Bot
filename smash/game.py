from base.game import Game
from smash.stagelist import StageList


class Game(Game):
    """
    Represents a Smash game
    """

    def __init__(self, game_num: int):
        super().__init__(game_num)
        self.stagelist: StageList = StageList()
        # stage veto / selection process state
        self.state = 0

    def starters_embed(self) -> str:
        """
        Generate embed string for stagelist starters
        :return:
        """
        message = ""
        for x in range(len(self.stagelist.starters)):
            message = f'{message}{self.stagelist.starters[x]}\n'
        return message

    def counters_embed(self) -> str:
        """
        Generate embed string for stagelist counters
        :return:
        """
        message = ""
        for x in range(len(self.stagelist.counters)):
            message = f'{message}{self.stagelist.counters[x]}\n'
        return message
