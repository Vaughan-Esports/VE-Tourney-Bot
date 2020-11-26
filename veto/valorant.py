import asyncio
from string import capwords

import discord
from discord.ext import commands

from utils import player_utils
from utils.message_generators import *


async def bo1(ctx: discord.ext.commands.Context, bot: discord.ext.commands.Bot,
              main_message: discord.Message,
              p1: discord.User, p2: discord.User, emb: discord.Embed):
    # setup stuff
    main_msg = main_message
    embed = emb

    # player check function
    def playerCheck(message):
        return message.content.lower() == 'me' and message.channel == ctx.channel

    # stage check function
    def mapCheck(message):
        return capwords(message.content) in maps and message.channel == ctx.channel

    # setup players
    player1, player2 = await player_utils.coinflip(ctx, p1, p2)
    await asyncio.sleep(2)

    # maps
    removed_maps = []

    # notifies of veto starts
    await ctx.send(f"Starting veto with {player1.mention} as **Team A** and {player2.mention} "
                   f"as **Team B** in 5 seconds...")

    # delete all messages and begin veto after 5 seconds
    await asyncio.sleep(5)
    await ctx.channel.purge(after=main_msg)

    for x in range(4):
        if x == 0:
            await ctx.send(f"{player1.mention} please veto a map.")
        elif x == 1:
            await ctx.send(f"{player2.mention} please veto a map.")
        elif x == 2:
            await ctx.send(f"{player1.mention} please veto another map.")
        elif x == 3:
            await ctx.send(f"{player2.mention} please veto another map.")

        # wait for players stage choice
        msg = await bot.wait_for('message', check=mapCheck, timeout=300)

        # remove messages sent after the embed
        await ctx.channel.purge(after=main_msg)

        # if not last map then strike out
        if x != 3:
            # strike out map
            removed_maps.append(capwords(msg.content))
            embed.set_field_at(1, name="Maps",
                               value=valorant_maps_message(removed_maps))
        else:
            removed_maps.append(capwords(msg.content))
            # highlight last map
            selected_map = ""
            for val_map in maps:
                if val_map not in removed_maps:
                    selected_map = val_map
            embed.set_field_at(1, name="Maps",
                               value=valorant_maps_message(removed_maps,
                                                           selected_map))

            # notify users of map and side pick
            await ctx.send(
                f"You'll be playing on __**{selected_map}**__. {player1.mention} gets their preferred side.")

        # edit original message with new embed
        await main_msg.edit(embed=embed)

    # get winner of the match
    await ctx.send(
        f"{newline}GLHF! Once finished, the winner should say `me`.")
    msg = await bot.wait_for('message', check=playerCheck, timeout=1800)

    # update winner embed
    embed.set_field_at(0,
                       name=f"`                         Game 1                            `",
                       value=f"**Winner:** {msg.author.mention}", inline=False)
    await main_msg.edit(embed=embed)

    return main_msg, embed


async def bo3(ctx: discord.ext.commands.Context, bot: discord.ext.commands.Bot,
              main_message: discord.Message,
              p1: discord.User, p2: discord.User, emb: discord.Embed):
    # setup stuff
    main_msg = main_message
    embed = emb

    # player check function
    def playerCheck(message):
        return message.content.lower() == 'me' and message.channel == ctx.channel

    # stage check function
    def mapCheck(message):
        return capwords(
            message.content) in maps and message.channel == ctx.channel

    # setup players
    player1, player2 = await player_utils.coinflip(ctx, p1, p2)
    await asyncio.sleep(2)

    # maps
    removed_maps = []

    # notifies of veto starts
    await ctx.send(
        f"Starting veto with {player1.mention} as **Team A** and {player2.mention} "
        f"as **Team B** in 5 seconds...")

    # delete all messages and begin veto after 5 seconds
    await asyncio.sleep(5)
    await ctx.channel.purge(after=main_msg)

    for x in range(6):
        if x == 0:
            await ctx.send(
                f"{player1.mention} please select a map for game 1.")
        elif x == 1:
            await ctx.send(
                f"{player2.mention} please select a side for game 1")
        elif x == 2:
            await ctx.send(
                f"{player2.mention} please select a map for game 2.")
        elif x == 3:
            await ctx.send(
                f"{player1.mention} please select a side for game 2.")
        elif x == 4:
            await ctx.send(f"{player1.mention} please veto a map.")
        elif x == 5:
            await ctx.send(f"{player2.mention} please veto a map.")

        # wait for players stage choice
        msg = await bot.wait_for('message', check=mapCheck, timeout=300)

        # remove messages sent after the embed
        await ctx.channel.purge(after=main_msg)

        # if not last map then strike out
        if x != 5:
            # strike out map
            removed_maps.append(capwords(msg.content))
            embed.set_field_at(1, name="Maps",
                               value=valorant_maps_message(removed_maps))
        else:
            removed_maps.append(capwords(msg.content))
            # highlight last map
            selected_map = ""
            for val_map in maps:
                if val_map not in removed_maps:
                    selected_map = val_map
            embed.set_field_at(1, name="Maps",
                               value=valorant_maps_message(removed_maps,
                                                           selected_map))

            # notify users of map and side pick
            await ctx.send(
                f"You'll be playing on __**{selected_map}**__. {player1.mention} gets their preferred side.")

        # edit original message with new embed
        await main_msg.edit(embed=embed)

    # get winner of the match
    await ctx.send(
        f"{newline}GLHF! Once finished, the winner should say `me`.")
    msg = await bot.wait_for('message', check=playerCheck, timeout=1800)

    # update winner embed
    embed.set_field_at(0,
                       name=f"`                         Game 1                            `",
                       value=f"**Winner:** {msg.author.mention}", inline=False)
    await main_msg.edit(embed=embed)

    return main_msg, embed
