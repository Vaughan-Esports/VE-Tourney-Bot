from string import capwords

from base.game import Game
from settings import stages
from smash.stagelist import StageList


class Game(Game):
    """
    Represents a Smash game
    """

    def __init__(self, game_num: int):
        super().__init__(game_num)
        self.stagelist: StageList = StageList(stages)

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

    def veto(self, stage: str) -> bool:
        """
        Tries to veto a stage
        :param stage: stage to veto
        :return: boolean value if stage was veto'd
        """
        # search for stage in starters
        for x in range(len(self.stagelist.starters)):
            # check for name or alias match
            if capwords(stage) == self.stagelist.starters[x].name \
                    or stage.lower in self.stagelist.starters[x].aliases:
                # if matching, change the state of the stage
                self.stagelist.starters[x].veto = True
                return True

        # search through counters
        for x in range(len(self.stagelist.counters)):
            # check for name or alias match
            if capwords(stage) == self.stagelist.counters[x].name \
                    or stage.lower in self.stagelist.starters[x].aliases:
                # if matching, change the state of the stage
                self.stagelist.counters[x].veto = True
                return True

        # returns false if it wasn't successful
        return False
