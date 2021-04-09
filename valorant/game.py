from map_pool import MapPool


class Game:
    """
    Represents a VALORANT game
    """

    def __init__(self, game_num: int):
        self.name = f"`                    " \
                    f"Game {game_num + 1}" \
                    f"                     `"

        self.selected_stage = None
        self.winner = None
        self.map_pool = MapPool()

    def map_embed(self) -> str:
        """
        Generate embed string for discord embeds
        :return: string
        """
        message = ""
        # loop through map names
        for val_map in self.map_pool.maps:
            # append each map name to a newline
            message = f'{message}{val_map}\n'
        # return message string
        return message
