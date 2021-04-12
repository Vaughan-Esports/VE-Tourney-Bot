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
                                           stages[x]['starter'],
                                           stages[x]['aliases']))
            # if starter bool = false
            else:
                # create new stage from info and add to counters
                self.counters.append(Stage(stages[x]['name'],
                                           stages[x]['starter'],
                                           stages[x]['aliases']))

    def veto(self, stage: str) -> Stage:
        """
        Tries to veto a stage
        :param stage: name/alias of stage to veto
        :return: the stage object that was veto'd
        """
        # search for stage in starters
        for x in range(len(self.starters)):
            if self.starters[x] == stage:
                # if matching, change the state of the stage
                self.starters[x].veto = True
                return self.starters[x]

        # search through counters
        for x in range(len(self.counters)):
            if self.counters[x] == stage:
                # if matching, change the state of the stage
                self.counters[x].veto = True
                return self.counters[x]

    def choose(self, stage: str) -> Stage:
        """
        Chooses a stage
        :param stage: name/alias of stage to veto
        :return: the stage object that was chosen
        """
        # search for stage in starters
        for x in range(len(self.starters)):
            if self.starters[x] == stage:
                # if matching, change the state of the stage
                self.starters[x].chosen = True
                return self.starters[x]

        # search through counters
        for x in range(len(self.counters)):
            if self.counters[x] == stage:
                # if matching, change the state of the stage
                self.counters[x].chosen = True
                return self.counters[x]

    def __contains__(self, stage: str):
        """
        Check's if a string is the name of a stage
        :param stage:
        :return:
        """
        # search for stage in starters
        for x in range(len(self.starters)):
            if self.starters[x] == stage and \
                    not self.starters[x].veto and \
                    not self.starters[x].chosen:
                return True

        # search through counters
        for x in range(len(self.counters)):
            if self.counters[x] == stage and \
                    not self.counters[x].veto and \
                    not self.counters[x].chosen:
                return True

        # returns false if it wasn't successful
        return False
