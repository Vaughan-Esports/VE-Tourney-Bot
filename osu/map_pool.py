from typing import List

from osu.beatmap import Beatmap
from settings import beatmaps


class MapPool:
    """
    Represents an osu map pool
    """

    def __init__(self):
        # categories
        self.noMod: List[Beatmap] = []
        self.hidden: List[Beatmap] = []
        self.hardRock: List[Beatmap] = []
        self.doubleTime: List[Beatmap] = []
        self.freeMod: List[Beatmap] = []
        self.tiebreaker: Beatmap

        # loop through maps from settings
        for map in beatmaps:
            if map['category'] == 0:
                self.noMod.append(Beatmap(map['name'],
                                          map['map_id'],
                                          map['category'],
                                          map['alias']))
            elif map['category'] == 1:
                self.hidden.append(Beatmap(map['name'],
                                           map['map_id'],
                                           map['category'],
                                           map['alias']))
            elif map['category'] == 2:
                self.hardRock.append(Beatmap(map['name'],
                                             map['map_id'],
                                             map['category'],
                                             map['alias']))
            elif map['category'] == 3:
                self.doubleTime.append(Beatmap(map['name'],
                                               map['map_id'],
                                               map['category'],
                                               map['alias']))
            elif map['category'] == 4:
                self.freeMod.append(Beatmap(map['name'],
                                            map['map_id'],
                                            map['category'],
                                            map['alias']))
            elif map['category'] == 5:
                self.tieBreaker = (Beatmap(map['name'],
                                           map['map_id'],
                                           map['category'],
                                           map['alias']))

    def veto(self, map: str) -> Beatmap:
        """
        Tries to veto a map
        :param map: name/alias of the map to veto
        :return: the beatmap object that was veto'd
        """
        # searches no mod list
        for beatmap in self.noMod:
            if beatmap == map:
                beatmap.veto = True
                return beatmap
        # searches hidden list
        for beatmap in self.hidden:
            if beatmap == map:
                beatmap.veto = True
                return beatmap
        # searches hardrock list
        for beatmap in self.hardRock:
            if beatmap == map:
                beatmap.veto = True
                return beatmap
        # searches doubletime list
        for beatmap in self.doubleTime:
            if beatmap == map:
                beatmap.veto = True
                return beatmap
        # searches freemod list
        for beatmap in self.freeMod:
            if beatmap == map:
                beatmap.veto = True
                return beatmap

    def choose(self, map: str) -> Beatmap:
        """
        Tries to choose a stage
        :param map: name/alias of the map to choose
        :return: the beatmap object that was chosen
        """
        # searches no mod list
        for beatmap in self.noMod:
            if beatmap == map:
                beatmap.chosen = True
                return beatmap
        # searches hidden list
        for beatmap in self.hidden:
            if beatmap == map:
                beatmap.chosen = True
                return beatmap
        # searches hardrock list
        for beatmap in self.hardRock:
            if beatmap == map:
                beatmap.chosen = True
                return beatmap
        # searches doubletime list
        for beatmap in self.doubleTime:
            if beatmap == map:
                beatmap.chosen = True
                return beatmap
        # searches freemod list
        for beatmap in self.freeMod:
            if beatmap == map:
                beatmap.chosen = True
                return beatmap

    def __contains__(self, map: str) -> bool:
        """
        Checks if a string is in the map pool
        :param map:
        :return:
        """
        # searches no mod list
        for beatmap in self.noMod:
            if beatmap == map and \
                    not beatmap.veto and \
                    not beatmap.chosen:
                return True
        # searches hidden list
        for beatmap in self.hidden:
            if beatmap == map and \
                    not beatmap.veto and \
                    not beatmap.chosen:
                return True
        # searches hardrock list
        for beatmap in self.hardRock:
            if beatmap == map and \
                    not beatmap.veto and \
                    not beatmap.chosen:
                return True
        # searches doubletime list
        for beatmap in self.doubleTime:
            if beatmap == map and \
                    not beatmap.veto and \
                    not beatmap.chosen:
                return True
        # searches freemod list
        for beatmap in self.freeMod:
            if beatmap == map and \
                    not beatmap.veto and \
                    not beatmap.chosen:
                return True

        # returns false if not successful
        return False
