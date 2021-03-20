from typing import List

from settings import rulebook_url, tourney_name
from smash.game import Game
from smash.player import Player


class Match:
    """
    Represents a Smash match
    """

    def __init__(self, player1: Player, player2: Player, num_of_games: int):
        # players
        self.player1 = player1
        self.player2 = player2

        # match data
        self.games: List[Game] = []
        self.name: str = f"{tourney_name}: {player1.name} vs {player2.name}"
        self.description: str = f"{self.player1.mention} vs " \
                                f"{self.player2.mention} " \
                                f"\nThe rulebook can be found " \
                                f"[here]({rulebook_url})"

        # match state
        self.num_of_games: int = num_of_games
        self.current_game: int = 0

        # generate blank games
        for x in range(num_of_games):
            self.games.append(Game(x))
