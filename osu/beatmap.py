from settings import cross_map_on_veto, hide_map_on_veto


class Beatmap:
    """
    Represents an osu beatmap
    """

    def __init__(self, name: str, map_id: int, category: int, alias: str):
        """
        Constructor Method
        :param name: name of the map
        :param map_id: beatmap id
        :param category: beatmap category (0-5 | NM-HD-HR-DT-FM-TB)
        :param alias: alias of the map (e.g. NM1)
        """
        self.name = name
        self.map_id = map_id
        self.category = category
        self.alias = alias

        self.veto = False
        self.chosen = False

    def __str__(self) -> str:
        """
        String representation of a map
        :return:
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

    def __eq__(self, other) -> bool:
        """
        Compares a string of a map name to self
        :param other: string name of map
        :return: boolean if matching
        """
        return other.lower() == self.name.lower() or \
               other.upper() == self.alias.upper()
