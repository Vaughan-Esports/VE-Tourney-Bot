from typing import List

import discord
from discord.ext import commands

from settings import tourney_name, rulebook_url, footer_icon, footer_note, \
    veto_timeout
from utils.checks import mapCheck, sideCheck
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

        # generate games
        for x in range(num_of_games):
            self.games.append(Game(x))

    @property
    def embed(self):
        title = f"VALORANT Best-of-{self.num_of_games} Veto"
        embed = discord.Embed(title=title,
                              description=self.description,
                              color=discord.Colour.gold())
        # loop through max games times and generate embed fields
        for x in range(len(self.games)):
            embed.add_field(name=self.games[x].name,
                            value='_ _',
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
            for x in range(5):
                if x == 0:
                    await ctx.send(
                        f"{self.captain1.mention} veto a map.")
                elif x == 1:
                    await ctx.send(
                        f"{self.captain2.mention} veto a map.")
                elif x == 2:
                    await ctx.send(
                        f"{self.captain1.mention} veto another map.")
                elif x == 3:
                    await ctx.send(
                        f"{self.captain2.mention} veto another map.")
                elif x == 4:
                    # select last map
                    self.games[self.current_game].choose_last()

                    # resend embed
                    await ctx.send(embed=self.embed)

                    await ctx.send(
                        f"{self.captain1.mention} what is your "
                        f"preferred starting side?")

                # if veto'ing
                if x <= 3:
                    msg = await bot.wait_for('message',
                                             check=mapCheck(ctx, self),
                                             timeout=veto_timeout)
                    # veto the map
                    self.games[self.current_game].veto_map(msg.content)

                # otherwise select side
                else:
                    # run side selection
                    await self.sideSelection(ctx, bot, 1)

                # resend embed
                await ctx.send(embed=self.embed)

        # Bo3 VETO
        elif self.num_of_games == 3:
            for x in range(6):
                if x == 0:
                    await ctx.send(
                        f"{self.captain1.mention} select a map for game 1.")
                elif x == 1:
                    await ctx.send(
                        f"{self.captain2.mention} what is your "
                        f"preferred starting side for game 1?")
                    await self.sideSelection(ctx, bot, 2)
                    # update current game
                    self.current_game += 1
                    # refresh embed
                    await ctx.send(embed=self.embed)
                    # skip to next step
                    continue

                elif x == 2:
                    await ctx.send(
                        f"{self.captain2.mention} select a map for game 2.")
                elif x == 3:
                    await ctx.send(
                        f"{self.captain1.mention} what is your "
                        f"preferred starting side for game 2?")
                    await self.sideSelection(ctx, bot, 1)
                    # update current game
                    self.current_game += 1
                    # refresh embed
                    await ctx.send(embed=self.embed)
                    # skip to next step
                    continue

                elif x == 4:
                    await ctx.send(
                        f"{self.captain1.mention} please veto a map.")
                elif x == 5:
                    await ctx.send(
                        f"{self.captain2.mention} please veto a map.")

                msg = await bot.wait_for('message',
                                         check=mapCheck(ctx, self),
                                         timeout=veto_timeout)

                if x == 0 or x == 2:
                    # choose map for these games
                    self.games[self.current_game].choose(msg.content)
                    # loop through and veto from rest (chosen takes over veto)
                    for game in self.games:
                        game.veto_map(msg.content)

                # FIXME: idk some way to do this better but it s 4am now xd
                elif x == 4 or x == 5:
                    # veto the map from all games
                    for game in self.games:
                        game.veto_map(msg.content)

                    if x == 5:
                        # choose last map
                        self.games[self.current_game].choose_last()

                        # refresh embed
                        await ctx.send(embed=self.embed)

                        # side selection for last game
                        await ctx.send(
                            f"{self.captain1.mention} what is your "
                            f"preferred starting side for game 3?")
                        await self.sideSelection(ctx, bot, 1)

                # refresh embed
                await ctx.send(embed=self.embed)

        # BO5 VETO
        # FIXME: most definitely can be better, but its 4am xd
        elif self.num_of_games == 5:
            for x in range(9):
                # GAME 1
                if x == 0:
                    await ctx.send(
                        f"{self.captain1.mention} select a map for game 1.")
                elif x == 1:
                    await ctx.send(
                        f"{self.captain2.mention} what is your "
                        f"preferred starting side for game 1?")
                    await self.sideSelection(ctx, bot, 2)
                    # update current game
                    self.current_game += 1
                    # refresh embed
                    await ctx.send(embed=self.embed)
                    # skip to next step
                    continue

                # GAME 2
                elif x == 2:
                    await ctx.send(
                        f"{self.captain2.mention} select a map for game 2.")
                elif x == 3:
                    await ctx.send(
                        f"{self.captain1.mention} what is your "
                        f"preferred starting side for game 2?")
                    await self.sideSelection(ctx, bot, 1)
                    # update current game
                    self.current_game += 1
                    # refresh embed
                    await ctx.send(embed=self.embed)
                    # skip to next step
                    continue

                # GAME 3
                elif x == 4:
                    await ctx.send(
                        f"{self.captain1.mention} select a map for game 3.")
                elif x == 5:
                    await ctx.send(
                        f"{self.captain2.mention} what is your "
                        f"preferred starting side for game 3?")
                    await self.sideSelection(ctx, bot, 2)
                    # update current game
                    self.current_game += 1
                    # refresh embed
                    await ctx.send(embed=self.embed)
                    # skip to next step
                    continue

                # GAME 4
                elif x == 6:
                    await ctx.send(
                        f"{self.captain2.mention} select a map for game 4.")
                elif x == 7:
                    await ctx.send(
                        f"{self.captain1.mention} what is your "
                        f"preferred starting side for game 4?")
                    await self.sideSelection(ctx, bot, 1)
                    # update current game
                    self.current_game += 1
                    # refresh embed
                    await ctx.send(embed=self.embed)
                    # skip to next step
                    continue

                if x % 2 == 0 and x != 8:
                    msg = await bot.wait_for('message',
                                             check=mapCheck(ctx, self),
                                             timeout=veto_timeout)
                    # choose map for these games
                    self.games[self.current_game].choose(msg.content)
                    # loop through and veto from rest (chosen takes over veto)
                    for game in self.games:
                        game.veto_map(msg.content)

                # FIXME: idk some way to do this better but it s 4am now xd
                elif x == 8:
                    # choose last map
                    self.games[self.current_game].choose_last()

                    # refresh embed
                    await ctx.send(embed=self.embed)

                    # side selection for last game
                    await ctx.send(
                        f"{self.captain1.mention} what is your "
                        f"preferred starting side for game 5?")
                    await self.sideSelection(ctx, bot, 1)

                # refresh embed
                await ctx.send(embed=self.embed)

        await ctx.send("GLHF! Don't forget to report your scores afterwards.")

    async def sideSelection(self, ctx, bot, chooser):
        # get side message
        msg = await bot.wait_for('message',
                                 check=sideCheck(ctx),
                                 timeout=veto_timeout)

        # set proper captain pings
        if 'att' in msg.content.lower():
            if chooser == 1:
                self.games[self.current_game].att_start = self.captain1
                self.games[self.current_game].def_start = self.captain2
            else:
                self.games[self.current_game].att_start = self.captain2
                self.games[self.current_game].def_start = self.captain1
        elif 'def' in msg.content.lower():
            if chooser == 2:
                self.games[self.current_game].att_start = self.captain1
                self.games[self.current_game].def_start = self.captain2
            else:
                self.games[self.current_game].att_start = self.captain2
                self.games[self.current_game].def_start = self.captain1
