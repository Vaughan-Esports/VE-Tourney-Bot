import random
from typing import List

from lol.champion import Champion
from settings import lol_champs, aram_champ_pool_size


class ChampPool:
    """
    Represents an ARAM Champ Pool of 20 Random Champions
    """

    def __init__(self):
        self.champions: List[Champion] = []

        while len(self.champions) < aram_champ_pool_size:
            champ = lol_champs[random.randint(0, len(lol_champs) - 1)]
            if champ not in self.champions:
                self.champions.append(Champion(champ))

    def __contains__(self, item):
        """
        Checks if a champion is in the pool
        :param item:
        :return:
        """
        # loop through all champions
        for champ in self.champions:
            # return true if found
            if champ == item:
                return True

        # return false otherwise
        return False
