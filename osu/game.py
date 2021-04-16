from osu.map_pool import MapPool


class Game:
    """
    Represents an osu! game
    """

    def __init__(self, game_num: int):
        self.name = f"`                    " \
                    f"Game {game_num + 1}" \
                    f"                     `"

        self.selected_map = None
        self.winner = None

        self.map_pool: MapPool = MapPool()

    @property
    def no_mod_embed(self) -> str:
        message = ""
        # loop through no mods list
        for beatmap in self.map_pool.noMod:
            # append map name to a newline in the message
            message = f'{message}{beatmap}\n'
        # return message string
        return message

    @property
    def hidden_embed(self) -> str:
        message = ""
        # loop through no mods list
        for beatmap in self.map_pool.hidden:
            # append map name to a newline in the message
            message = f'{message}{beatmap}\n'
        # return message string
        return message

    @property
    def hard_rock_embed(self) -> str:
        message = ""
        # loop through no mods list
        for beatmap in self.map_pool.hardRock:
            # append map name to a newline in the message
            message = f'{message}{beatmap}\n'
        # return message string
        return message

    @property
    def double_time_embed(self) -> str:
        message = ""
        # loop through no mods list
        for beatmap in self.map_pool.doubleTime:
            # append map name to a newline in the message
            message = f'{message}{beatmap}\n'
        # return message string
        return message

    @property
    def free_mod_embed(self) -> str:
        message = ""
        # loop through no mods list
        for beatmap in self.map_pool.noMod:
            # append map name to a newline in the message
            message = f'{message}{beatmap}\n'
        # return message string
        return message

    @property
    def tiebreaker_embed(self) -> str:
        return self.map_pool.tieBreaker
