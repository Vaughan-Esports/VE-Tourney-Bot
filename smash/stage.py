from typing import List

from base.map import Map


class Stage(Map):
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
        super().__init__(name)
        self.starter = starter
        self.aliases = aliases
