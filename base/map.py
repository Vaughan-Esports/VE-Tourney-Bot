from abc import ABC


class Map(ABC):
    def __init__(self, name: str):
        self.name = name
        self.veto = False
        self.chosen = False

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
