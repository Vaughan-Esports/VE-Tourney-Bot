from typing import List


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
            return f'~~{self.name}~~'
        elif self.chosen:
            return f'⮕**{self.name}~~'
        else:
            return self.name
