from typing import List

import discord

from settings import rulebook_url, tourney_name, footer_icon, footer_note
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

        # GENERATE EMBED
        title = f"Smash Ultimate Best-of-{num_of_games} Veto"
        self.embed = discord.Embed(title=title,
                                   description=self.description,
                                   color=discord.Colour.gold())
        # loop through max games times and generate embed fields
        for x in range(1, num_of_games + 1):
            self.embed.add_field(name=self.games[x - 1].name,
                                 value="**Winner:** TBD", inline=False)
            # x - 1 because its using index num
            self.embed.add_field(name="Starter Stages",
                                 value=self.games[x - 1].starters_embed(),
                                 inline=True)
            self.embed.add_field(name="Counterpick Stages",
                                 value=self.games[x - 1].counters_embed(),
                                 inline=True)
        # set footer
        self.embed.set_footer(icon_url=footer_icon,
                              text=f"{tourney_name} | {footer_note}")
