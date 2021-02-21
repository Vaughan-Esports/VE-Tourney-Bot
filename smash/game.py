from typing import List

import stage
from base.game import Game


class Game(Game):
    """
    Represents a Smash game
    """

    def __init__(self, game_num: int, map_pool: List[stage]):
        super().__init__(game_num, map_pool)
