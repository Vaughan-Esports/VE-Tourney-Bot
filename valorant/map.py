from string import capwords

from settings import hide_map_on_veto, cross_map_on_veto


class Map:
    """
    Represents a VALORANT Map
    """

    def __init__(self, name: str):
        """
        Constructor method
        :param name: name of the map
        """
        self.name = name
        self.veto = False
        self.chosen = False

    def __str__(self) -> str:
        """
        String representation of the map
        :return: string of map
        """
        if self.veto:
            name = self.name
            # surround in cross out if crossing
            if cross_map_on_veto:
                name = f'~~{name}~~'
            # surround in spoiler tags if hiding
            if hide_map_on_veto:
                name = f'||{name}||'
            # return the name of the stage
            return name
        elif self.chosen:
            return f'⮕**{self.name}**'
        else:
            return self.name

    def __eq__(self, other):
        """
        Compares a string of the map name to its name
        :param other: string name of other map
        :return: boolean if matching
        """
        return capwords(other) == self.name
