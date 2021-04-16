from typing import List

import discord
import discord.ext

from osu.game import Game
from settings import tourney_name, rulebook_url, footer_icon, footer_note


class Match:
    """
    Represents an osu! match
    """

    def __init__(self,
                 player1: discord.User,
                 player2: discord.User,
                 num_of_games: int):
        # players
        self.player1 = player1
        self.player2 = player2
        self.winner = None

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

        for x in range(num_of_games):
            self.games.append(Game(x))

    @property
    def embed(self):
        title = f"osu! Best-of-{self.num_of_games} Veto"
        embed = discord.Embed(title=title,
                              description=self.description,
                              color=discord.Colour.gold())
        # loop through max games times and generate embed fields
        embed.add_field(name=self.games[self.current_game].name,
                        value=self.games[self.current_game].winner_embed,
                        inline=False)
        embed.add_field(name="__No Mod (NM)__",
                        value=self.games[self.current_game].no_mod_embed,
                        inline=False)
        embed.add_field(name="__Hidden (HD)__",
                        value=self.games[self.current_game].hidden_embed,
                        inline=False)
        embed.add_field(name="__Hard Rock (HR)__",
                        value=self.games[self.current_game].hard_rock_embed,
                        inline=False)
        embed.add_field(name="__Double Time (DT)__",
                        value=self.games[self.current_game].double_time_embed,
                        inline=False)
        embed.add_field(name="__Free Mod (FM)__",
                        value=self.games[self.current_game].free_mod_embed,
                        inline=False)
        embed.add_field(name="__Tie Breaker (TB)__",
                        value=self.games[self.current_game].tiebreaker_embed,
                        inline=False)

        # set footer
        embed.set_footer(icon_url=footer_icon,
                         text=f"{tourney_name} | {footer_note}")

        return embed

    def veto(self, ctx: discord.ext.commands.Context,
             bot: discord.ext.commands.Bot):
        # send first embed
        await ctx.send(embed=self.embed)

        # initial veto
        if self.current_game == 0:
            # loop through the two stage process
            for x in range(2):
                if x == 0:
                    await ctx.send(f'{self.player1.mention}, veto a map.')
                elif x == 1:
                    await ctx.send(f'{self.player2.mention}, veto a map.')
