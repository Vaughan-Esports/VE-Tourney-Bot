from typing import List

from settings import val_maps
from valorant.map import Map


class MapPool:
    """
    Represents a VALORANT Map Pool
    """

    def __init__(self):
        # map list
        self.maps: List[Map] = []

        # loops through the map from settings
        for val_map in val_maps:
            self.maps.append(Map(val_map))

    def __contains__(self, item):
        """
        Check if a string is the name of a stage
        :param item: string of map name
        :return:
        """
        # search through map for match
        for val_map in self.maps:
            if val_map == item and \
                    not val_map.veto and \
                    not val_map.chosen:
                return True

        # else return false if it wasn't found
        return False
