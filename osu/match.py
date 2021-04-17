import asyncio
from typing import List

import discord
import discord.ext

from osu.game import Game
from settings import tourney_name, rulebook_url, footer_icon, footer_note, \
    veto_timeout, newline
from utils.checks import beatmapCheck, playerCheck


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
        self.player1_wins: int = 0
        self.player2 = player2
        self.player2_wins: int = 0
        self.winner = None

        # match data
        self.games: List[Game] = []
        self.name: str = f"{tourney_name}: {player1.name} vs {player2.name}"
        self.veto_maps = []

        # match state
        self.num_of_games: int = num_of_games
        self.current_game: int = 0

        # map pick
        self.a_pick = self.player1.mention
        self.b_pick = self.player2.mention

        for x in range(num_of_games):
            if x == num_of_games - 1:
                self.games.append(Game(x, True))
            else:
                self.games.append(Game(x))

    @property
    def description(self):
        return f"{self.player1_wins} - {self.player1.mention} vs " \
               f"{self.player2.mention} - {self.player2_wins} " \
               f"\nThe rulebook can be found " \
               f"[here]({rulebook_url})"

    @property
    def embed(self):
        title = f"osu! Best-of-{self.num_of_games} Veto"
        embed = discord.Embed(title=title,
                              description=self.description,
                              color=discord.Colour.gold())
        # add current game fields
        embed.add_field(name=self.games[self.current_game].name,
                        value='_ _',
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

    @property
    def winner_embed(self):
        title = f"osu! Best-of-{self.num_of_games} Veto"
        embed = discord.Embed(title=title,
                              description=self.description,
                              color=discord.Colour.green())
        # loop through max games times and generate embed fields
        for game in self.games:
            if game.winner is not None:
                embed.add_field(name=game.name,
                                value='_ _',
                                inline=False)
                embed.add_field(name='__Winner__',
                                value=game.winner.mention,
                                inline=False)
                embed.add_field(name='__Map__',
                                value=f'{game.selected_map.alias} - '
                                      f'{game.selected_map.name}',
                                inline=False)

        # set footer
        embed.set_footer(icon_url=footer_icon,
                         text=f"{tourney_name} | {footer_note}")
        return embed

    async def veto(self, ctx: discord.ext.commands.Context,
                   bot: discord.ext.commands.Bot):

        # veto maps that were played already / banned
        for beatmap in self.veto_maps:
            self.games[self.current_game].veto_map(beatmap)

        # send first embed
        await ctx.send(embed=self.embed)

        # if tiebreaker
        if self.current_game == self.num_of_games - 1:
            await ctx.send('TIE BREAKER TIME!')
            await self.send_commands(ctx)

        # initial veto
        elif self.current_game == 0:
            # loop through the two stage process
            for x in range(2):
                if x == 0:
                    await ctx.send(f'{self.player1.mention}, veto a map.')
                elif x == 1:
                    await ctx.send(f'{self.player2.mention}, veto a map.')

                # get map
                msg = await bot.wait_for('message',
                                         check=beatmapCheck(ctx, self),
                                         timeout=veto_timeout)

                # veto map
                self.games[self.current_game].veto_map(msg.content)
                self.veto_maps.append(msg.content)

                # regenerate and send embed
                await ctx.send(embed=self.embed)

        if not self.current_game == self.num_of_games - 1:
            # choose maps
            if self.current_game % 2 == 0:
                # when even its player 2 veto
                await ctx.send(f'{self.b_pick}, pick a map for game'
                               f' {self.current_game + 1}')
            else:
                # when odd its player 1 veto
                await ctx.send(f'{self.a_pick}, pick a map for game'
                               f' {self.current_game + 1}')

            # get map
            msg = await bot.wait_for('message',
                                     check=beatmapCheck(ctx, self),
                                     timeout=veto_timeout)

            # select map
            self.games[self.current_game].choose_map(msg.content)
            # veto map out of future games
            self.veto_maps.append(msg.content)
            # regenerate embed and send
            await ctx.send(embed=self.embed)
            # send commands for the map
            await self.send_commands(ctx)

        # get winner
        await ctx.send(f"{newline}GLHF! Once finished, "
                       f"the winner should say `me`.")
        msg = await bot.wait_for('message',
                                 check=playerCheck(ctx),
                                 timeout=veto_timeout)

        # swap player 1 if player 2 was winner
        if msg.author.id == self.player2.id:
            self.swap_players()

        # add to winner count and set game winner
        self.games[self.current_game].winner = self.player1
        self.player1_wins += 1

        # check if the match has a winner
        if self.player1_wins >= (self.num_of_games // 2) + 1:
            self.winner = self.player1
            await ctx.send(embed=self.winner_embed)
            await ctx.send('GG! Run `ve!close` to archive this channel.'
                           '\n\n'
                           'Don\'t forget to run `!mp close` in osu!')

        # else prep for the next game veto
        else:
            # move to next game
            self.current_game += 1

            # setup next game
            await ctx.send('Starting next game veto...')
            await asyncio.sleep(3)

    async def send_commands(self, ctx: discord.ext.commands.Context):
        await ctx.send(f'**BanchoBot** commands to setup the game: \n'
                       f'{self.games[self.current_game].selected_map.commands}')

    def swap_players(self):
        """
        Swap player1 and player2
        """
        # swap player objects
        p1 = self.player2
        p1w = self.player2_wins
        p2 = self.player1
        p2w = self.player1_wins

        # set new players
        self.player1 = p1
        self.player1_wins = p1w
        self.player2 = p2
        self.player2_wins = p2w
