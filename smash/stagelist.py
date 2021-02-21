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
