from string import capwords
from typing import List

from settings import hide_map_on_veto, cross_map_on_veto


class Stage:
    """
    Represents a Smash stage
    """

    def __init__(self, name: str, starter: bool, aliases: List[str] = None):
        """
        Constructor Method
        :param name: name of the stage
        :param starter: if stage is a starter
        :param aliases: alias names for the stage
        """
        self.name = name
        self.veto = False
        self.chosen = False
        self.starter = starter
        self.aliases = aliases

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

    def __eq__(self, stage: str) -> bool:
        """
        Compares a string of the stage name to its name and aliases
        :param stage: string name of the stage
        :return: boolean if matching
        """
        return capwords(stage) == self.name or stage.lower() in self.aliases
