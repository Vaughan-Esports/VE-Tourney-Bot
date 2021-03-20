from string import capwords
from typing import List

from settings import stages
from smash.stage import Stage


class StageList:
    """
    Represents a list of smash stages
    """

    def __init__(self):
        # stage lists
        self.starters: List[Stage] = []
        self.counters: List[Stage] = []

        # loops through the stages from settings
        for x in range(len(stages)):
            # if starter bool = true
            if stages[x]['starter']:
                # create new stage from info and add to starters
                self.starters.append(Stage(stages[x]['name'],
                                           stages[x]['starter',
                                                     stages[x]['aliases']]))
            # if starter bool = false
            else:
                # create new stage from info and add to counters
                self.counters.append(Stage(stages[x]['name'],
                                           stages[x]['starter',
                                                     stages[x]['aliases']]))

    def veto(self, stage: str) -> bool:
        """
        Tries to veto a stage
        :param stage: name/alias of stage to veto
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
