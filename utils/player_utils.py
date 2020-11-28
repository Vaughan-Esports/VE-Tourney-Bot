import asyncio
import random

import discord
from discord.ext import commands

from utils import embeds


async def swap_players(player1: discord.User, player2: discord.User,
                       player1_dsr: list, player2_dsr: list):
    """
    Swap players for smash veto with tracking for DSR'd stages
    :param player1: player 1
    :param player2: player 2
    :param player1_dsr: player 1's DSR stage(s)
    :param player2_dsr: player 2's DSR stage(s)
    :return: new player1 and player2
    """
    # swap player objects
    p1 = player2
    p2 = player1

    # swap player DSR's
    p1_dsr = player2_dsr
    p2_dsr = player1_dsr

    # return new player 1 and player 2
    return p1, p2, p1_dsr, p2_dsr


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

    flip = await embeds.flipping_coin(5)
    coin_msg = await ctx.send(embed=flip)

    # coinflip animation
    for n in range(1, 5):
        await asyncio.sleep(0.7)
        flip = await embeds.flipping_coin(n)
        await coin_msg.edit(embed=flip)

    # pick random
    num = random.randrange(0, 101)
    if num % 2 == 0:
        player1 = p1
        player2 = p2
    elif num % 2 == 1:
        player1 = p2
        player2 = p1
    await coin_msg.edit(embed=await embeds.coinflip_winner(player1))

    return player1, player2
