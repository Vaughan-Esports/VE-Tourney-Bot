from string import capwords
from typing import List

from smash.stage import Stage


class StageList:
    """
    Represents a list of smash stages
    """

    def __init__(self, stages: List[dict]):
        self.starters: List[Stage] = []
        self.counters: List[Stage] = []

        for x in range(len(stages)):
            if stages[x]['starter']:
                self.starters.append(Stage(stages[x]['name'],
                                           stages[x]['starter',
                                                     stages[x]['aliases']]))
            else:
                self.counters.append(Stage(stages[x]['name'],
                                           stages[x]['starter',
                                                     stages[x]['aliases']]))

    def starters_embed(self) -> str:
        """
        Generate embed string for stagelist starters
        :return:
        """
        message = ""
        for x in range(len(self.starters)):
            message = f'{message}{self.starters[x]}\n'
        return message

    def counters_embed(self) -> str:
        """
        Generate embed string for stagelist counters
        :return:
        """
        message = ""
        for x in range(len(self.counters)):
            message = f'{message}{self.counters[x]}\n'
        return message

    def veto(self, stage: str) -> bool:
        """
        Tries to veto a stage
        :param stage: stage to veto
        :return: boolean value if stage was veto'd
        """
        # search for stage in starters
        for x in range(len(self.starters)):
            # check for name or alias match
            if capwords(stage) == self.starters[x].name \
                    or stage.lower in self.starters[x].aliases:
                # if matching, change the state of the stage
                self.starters[x].veto = True
                return True

        # search through counters
        for x in range(len(self.counters)):
            # check for name or alias match
            if capwords(stage) == self.counters[x].name \
                    or stage.lower in self.starters[x].aliases:
                # if matching, change the state of the stage
                self.counters[x].veto = True
                return True

        # returns false if it wasn't successful
        return False
