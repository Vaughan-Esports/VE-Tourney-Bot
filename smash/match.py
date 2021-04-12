import asyncio
from typing import List

import discord
from discord.ext import commands

from settings import rulebook_url, tourney_name, footer_icon, footer_note, \
    veto_timeout, newline
from smash.game import Game
from smash.player import Player
from utils.checks import playerCheck, stageCheck


class Match:
    """
    Represents a Smash match
    """

    def __init__(self, player1: Player, player2: Player, num_of_games: int):
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

        # generate first game
        self.games.append(Game(0))

    @property
    def embed(self):
        title = f"Smash Ultimate Best-of-{self.num_of_games} Veto"
        embed = discord.Embed(title=title,
                              description=self.description,
                              color=discord.Colour.gold())
        # loop through max games times and generate embed fields
        for x in range(len(self.games)):
            embed.add_field(name=self.games[x].name,
                            value=self.games[x].winner_embed(),
                            inline=False)
            # x - 1 because its using index num
            embed.add_field(name="__Starter Stages__",
                            value=self.games[x].starters_embed(),
                            inline=True)
            embed.add_field(name="__Counterpick Stages__",
                            value=self.games[x].counters_embed(),
                            inline=True)
        # set footer
        embed.set_footer(icon_url=footer_icon,
                         text=f"{tourney_name} | {footer_note}")

        return embed

    async def veto(self, ctx: discord.ext.commands.Context,
                   bot: discord.ext.commands.Bot):
        # FIGURING OUT GAME EMBED INDEXES (ONLY IF U WANT TO REWRITE):
        # GAME NUM * 3 = embed title index, just + 1 and + 2 for stage lists
        # IF FINISH EARLY LOOP FROM CURRENT_GAME TO NUM_OF_GAMES - 1
        # AND CROSS OUT LINE

        # add DSR stages to the game if on game 3 or higher
        if self.current_game >= 2:
            for x in range(len(self.player2.dsr)):
                self.games[self.current_game].veto_stage(
                    self.player2.dsr[x].name)

        # send first embed
        await ctx.send(embed=self.embed)

        # initial veto
        if self.current_game == 0:
            # loop through 4 stage veto's/selection
            for x in range(4):
                # check which message to send
                if x == 0:
                    await ctx.send(f"{self.player1.mention}, veto a starter.")
                if x == 1:
                    await ctx.send(f"{self.player2.mention}, veto a starter.")
                if x == 2:
                    await ctx.send(
                        f"{self.player2.mention}, veto another starter.")
                if x == 3:
                    await ctx.send(
                        f"{self.player1.mention}, select the stage from "
                        f"the remaining starters.")

                # wait for players stage choice
                msg = await bot.wait_for('message',
                                         check=stageCheck(ctx, self),
                                         timeout=veto_timeout)

                # if on stage selection
                if x == 3:
                    # choose the stage
                    self.games[self.current_game].choose_stage(msg.content)
                # if on veto still
                else:
                    # veto the stage
                    self.games[self.current_game].veto_stage(msg.content)

                # regenerate and send embed
                await ctx.send(embed=self.embed)

        # subsequent veto
        else:
            # loop through 3 stage veto's/selection process
            for x in range(3):
                if x == 0:
                    await ctx.send(f"{self.player1.mention}, veto a stage.")
                elif x == 1:
                    await ctx.send(
                        f"{self.player1.mention}, veto another stage.")
                elif x == 2:
                    await ctx.send(
                        f"{self.player2.mention}, select the stage.")
                # wait for players stage choice
                msg = await bot.wait_for('message',
                                         check=stageCheck(ctx, self),
                                         timeout=veto_timeout)

                # if on stage selection
                if x == 2:
                    # choose the stage
                    self.games[self.current_game].choose_stage(msg.content)
                # if on veto still
                else:
                    # veto the stage
                    self.games[self.current_game].veto_stage(msg.content)

                # regenerate and send embed
                await ctx.send(embed=self.embed)

        # get winner
        await ctx.send(f"{newline}GLHF! Once finished, "
                       f"the winner should say `me`.")
        msg = await bot.wait_for('message',
                                 check=playerCheck(ctx),
                                 timeout=veto_timeout)

        # swap player 1 if player 2 was winner
        if msg.author.id == self.player2.id:
            self.swap_players()

        # add stage to winner dsr list
        self.player1.dsr.append(
            self.games[self.current_game].selected_stage)

        # set the game winner
        self.games[self.current_game].winner = self.player1
        self.player1.wins += 1

        # check if the match has a winner
        if self.player1.wins >= (self.num_of_games // 2) + 1:
            self.winner = self.player1
            await ctx.send(embed=self.embed)
            await ctx.send('GG!')
        # else prep for the next game veto
        else:
            # move to next game
            self.current_game += 1

            # add games
            self.games.append(Game(self.current_game))

            # setup next game
            await ctx.send(embed=self.embed)
            await ctx.send('Starting next game veto...')
            await asyncio.sleep(3)

    def swap_players(self):
        """
        Swap player1 and player2
        """
        # swap player objects
        p1 = self.player2
        p2 = self.player1

        # set new players
        self.player1 = p1
        self.player2 = p2
