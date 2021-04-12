from typing import List

import discord
from discord.ext import commands

from settings import tourney_name, rulebook_url, footer_icon, footer_note, \
    veto_timeout
from utils.checks import mapCheck
from valorant.game import Game


class Match:
    """
    Represents a VALORANT Match
    """

    def __init__(self,
                 captain1: discord.Member,
                 captain2: discord.Member,
                 num_of_games: int):
        # captains
        self.captain1 = captain1
        self.captain2 = captain2
        self.winner = None
        # match data
        self.games: List[Game] = []
        self.name: str = f"{tourney_name}: {captain1.name} vs {captain2.name}"
        self.description: str = f"{self.captain1.mention} vs " \
                                f"{self.captain2.mention} " \
                                f"\nThe rulebook can be found " \
                                f"[here]({rulebook_url})"

        # match state
        self.num_of_games: int = num_of_games
        self.current_game: int = 0

        # generate first game
        self.games.append(Game(0))

    @property
    def embed(self):
        title = f"VALORANT Best-of-{self.num_of_games} Veto"
        embed = discord.Embed(title=title,
                              description=self.description,
                              color=discord.Colour.gold())
        # loop through max games times and generate embed fields
        for x in range(len(self.games)):
            embed.add_field(name=self.games[x].name,
                            value=self.games[x].winner_embed(),
                            inline=False)
            # x - 1 because its using index num
            embed.add_field(name="__Maps__",
                            value=self.games[x].map_embed(),
                            inline=True)
            embed.add_field(name="__Sides__",
                            value=self.games[x].sides_embed(),
                            inline=True)
        # set footer
        embed.set_footer(icon_url=footer_icon,
                         text=f"{tourney_name} | {footer_note}")

        return embed

    async def veto(self, ctx: discord.ext.commands.Context,
                   bot: discord.ext.commands.Bot):
        # send first embed
        await ctx.send(embed=self.embed)

        # Bo1 VETO
        if self.num_of_games == 1:
            for x in range(4):
                if x == 0:
                    await ctx.send(
                        f"{self.captain1.mention} please veto a map.")
                elif x == 1:
                    await ctx.send(
                        f"{self.captain2.mention} please veto a map.")
                elif x == 2:
                    await ctx.send(
                        f"{self.captain1.mention} please veto another map.")
                elif x == 3:
                    await ctx.send(
                        f"{self.captain2.mention} please veto another map.")
                elif x == 4:
                    await ctx.send(
                        f"{self.captain1.mention} what is your "
                        f"preferred starting side?")

                msg = await bot.wait_for('message',
                                         check=mapCheck(ctx, self),
                                         timeout=veto_timeout)

                # if veto'ing
                if x != 3
