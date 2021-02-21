from abc import ABC


class Map(ABC):
    def __init__(self, name: str):
        self.name = name
