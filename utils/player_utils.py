import random

import discord
from discord.ext import commands

from settings import newline
from smash.player import Player
from utils import embeds
from utils.checks import playerCheck


async def get_players(ctx: discord.ext.commands.Context):
    """
    Returns player objects from context
    :param ctx: message context
    :return: player 1 and 2 objects
    """
    # placeholder vars
    player1 = None
    player2 = None

    # if just one mention then its their opponent
    if len(ctx.message.mentions) == 1:
        player1 = ctx.author
        player2 = ctx.message.mentions[0]

    # if two mentions then its two players
    elif len(ctx.message.mentions) == 2:
        player1 = ctx.message.mentions[0]
        player2 = ctx.message.mentions[1]

    # return players
    return player1, player2


async def coinflip(ctx: discord.ext.commands.Context, p1: discord.User,
                   p2: discord.User):
    """
    Flips a coin and chooses higher seed
    :param ctx: message context
    :param p1: first player
    :param p2: second player
    :return: new player order with player 1 as coinflip winner
    """
    player1 = None
    player2 = None

    # pick random
    num = random.randrange(0, 101)
    if num % 2 == 0:
        player1 = p1
        player2 = p2
    elif num % 2 == 1:
        player1 = p2
        player2 = p1
    await ctx.send(embed=await embeds.coinflip_winner(player1))

    return player1, player2


async def seed_selection(ctx: discord.ext.commands.Context,
                         bot: discord.ext.commands.Bot,
                         match):
    # HIGHER SEED SELECTION
    await ctx.send(f"{newline}Player 1 (the higher seed) say `me`")

    msg = await bot.wait_for('message', check=playerCheck(ctx), timeout=300)

    # placeholders
    p1 = match.player1
    p2 = match.player2

    # changes player order if player 2 said they were first seed
    if Player(msg.author) == match.player2:
        match.player1 = p2
        match.player2 = p1

    # notifies of veto starts
    await ctx.send(f"Starting veto with {match.player1.mention} as "
                   f"**Player 1** and {match.player2.mention} "
                   f"as **Player 2** in 5 seconds...")
