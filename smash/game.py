from base.game import Game
from settings import stages
from smash.stagelist import StageList


class Game(Game):
    """
    Represents a Smash game
    """

    def __init__(self, game_num: int, map_pool: StageList):
        super().__init__(game_num)
        self.stagelist = StageList(stages)
