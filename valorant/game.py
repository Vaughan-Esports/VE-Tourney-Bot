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

        self.att_start = None
        self.def_start = None

    def winner_embed(self) -> str:
        """
        Generate embed string for winner line
        :return:
        """
        message = "**Winner:**"
        if self.winner is None:
            return f"{message} TBD"
        else:
            return f"{message} {self.winner.mention}"

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

    def sides_embed(self) -> str:
        """
        Generate embed string for discord embeds
        :return: string
        """
        if self.att_start is not None and self.def_start is not None:
            return f"**Attack:** {self.att_start.mention} \n" \
                   f"**Defense:** {self.def_start.mention}"
        else:
            return f"**Attack:** TBD \n" \
                   f"**Defense:** TBD"

    def veto_map(self, name: str):
        """
        Tries to veto a map
        :param name:
        :return: map that was veto'd
        """
        for x in range(len(self.map_pool.maps)):
            if self.map_pool.maps[x] == name:
                # if matching change th state of the map and return it
                self.map_pool.maps[x].veto = True
                return self.map_pool.maps[x]

    def choose(self, name: str):
        """
        Tries to choose a map
        :param name:
        :return: map that was chosen
        """
        for x in range(len(self.map_pool.maps)):
            if self.map_pool.maps[x] == name:
                # if matching change th state of the map and return it
                self.map_pool.maps[x].chosen = True
                return self.map_pool.maps[x]
