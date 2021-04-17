import asyncio
from typing import List

import discord

from lol.game import Game
from settings import tourney_name, rulebook_url, footer_icon, footer_note, \
    lol_champselect_timeout, newline, lol_game_timeout
from utils import embeds
from utils.checks import yesOrNoCheck, playerCheck


class Match:
    """
    Represents a League ARAM Match
    """

    def __init__(self,
                 captain1: discord.Member,
                 captain2: discord.Member,
                 num_of_games: int):
        # captains
        self.captain1 = captain1
        self.captain1_wins: int = 0
        self.captain2 = captain2
        self.captain2_wins: int = 0
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
        title = f"LoL ARAM Best-of-{self.num_of_games} Veto"
        embed = discord.Embed(title=title,
                              description=self.description,
                              color=discord.Colour.gold())
        embed.add_field(name="Team 1",
                        value=self.captain1.mention,
                        inline=True)
        embed.add_field(name="Team 2",
                        value=self.captain2.mention,
                        inline=True)
        # add current game fields
        game = self.games[self.current_game]
        embed.add_field(name=game.name,
                        value=game.winner_embed,
                        inline=False)
        embed.add_field(name="_ _",
                        value="_ _",
                        inline=False)
        embed.add_field(name="__Team 1 Champions__",
                        value=game.team1_embed,
                        inline=True)
        embed.add_field(name="__Team 2 Champions__",
                        value=game.team2_embed,
                        inline=True)
        # set footer
        embed.set_footer(icon_url=footer_icon,
                         text=f"{tourney_name} | {footer_note}")

        return embed

    @property
    def winner_embed(self):
        title = f"LoL ARAM Best-of-{self.num_of_games} Veto"
        embed = discord.Embed(title=title,
                              description=self.description,
                              color=discord.Colour.green())
        # loop through max games times and generate embed fields
        for game in self.games:
            if game.winner is not None:
                embed.add_field(name=game.name,
                                value=game.winner_embed,
                                inline=False)

        # set footer
        embed.set_footer(icon_url=footer_icon,
                         text=f"{tourney_name} | {footer_note}")
        return embed

    async def veto(self, ctx, bot):
        # send first embed
        await ctx.send(embed=self.embed)

        # team 1 veto chance
        await ctx.send(f'{self.captain1.mention}, would you like to reroll? '
                       f'(Y/N) | You have `{lol_champselect_timeout}s` '
                       f'to decide.')
        try:
            msg = await bot.wait_for('message',
                                     check=yesOrNoCheck(ctx),
                                     timeout=lol_champselect_timeout)
            if 'y' in msg.content.lower():
                self.games[self.current_game].reroll_team1_champs()

        except asyncio.TimeoutError:
            # get error embed and edit original message
            text = 'Timer ran out. Moving on!'
            await ctx.send(embed=await embeds.timeout_error(text))

        # regenerate and send embed
        await ctx.send(embed=self.embed)

        # team 2 veto chance
        await ctx.send(f'{self.captain2.mention}, would you like to reroll? '
                       f'(Y/N) | You have `{lol_champselect_timeout}s` '
                       f'to decide.')

        try:
            msg = await bot.wait_for('message',
                                     check=yesOrNoCheck(ctx),
                                     timeout=lol_champselect_timeout)
            if 'y' in msg.content.lower():
                self.games[self.current_game].reroll_team2_champs()

        except asyncio.TimeoutError:
            # get error embed and edit original message
            text = 'Timer ran out. Moving on!'
            await ctx.send(embed=await embeds.timeout_error(text))

        # regenerate and send embed
        await ctx.send(embed=self.embed)

        # get winner
        await ctx.send(f"{newline}GLHF! Once finished, "
                       f"the winner should say `me`.")
        msg = await bot.wait_for('message',
                                 check=playerCheck(ctx),
                                 timeout=lol_game_timeout)

        # swap player 1 if player 2 was winner
        if msg.author.id == self.captain2.id:
            self.swap_captains()

        # set the game winner
        self.games[self.current_game].winner = self.captain1
        self.captain1_wins += 1

        # check if the match has a winner
        if self.captain1_wins >= (self.num_of_games // 2) + 1:
            self.winner = self.captain1
            await ctx.send(embed=self.winner_embed)
            await ctx.send('GG! Run `ve!close` to archive this channel.')

        # else prep for the next game veto
        else:
            # move to next game
            self.current_game += 1

            # add games
            self.games.append(Game(self.current_game))

            # setup next game
            await ctx.send('Starting next game veto...')
            await asyncio.sleep(3)

    def swap_captains(self):
        """
        Swap player1 and player2
        """
        # swap player objects
        c1 = self.captain2
        c1w = self.captain2_wins
        c2 = self.captain1
        c2w = self.captain1_wins

        # set new players
        self.captain1 = c1
        self.captain1_wins = c1w
        self.captain2 = c2
        self.captain2_wins = c2w
