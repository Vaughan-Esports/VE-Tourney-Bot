import asyncio
from string import capwords

import discord
from discord.ext import commands

from utils import player_utils
from utils.message_generators import *

# combine lists for all stages list
all_stages = starters + counters


async def initial(ctx: discord.ext.commands.Context,
                  bot: discord.ext.commands.Bot, main_message: discord.Message,
                  p1: discord.User, p2: discord.User, emb: discord.Embed):
    """
    Runs an initial smash veto
    :param ctx: context for the message
    :param bot: bot user to use
    :param main_message: original message to edit
    :param p1: player1 user
    :param p2: player2 user
    :param emb: embed to edit
    :return:
    """

    # player check function
    def playerCheck(message):
        return message.content.lower() == 'me' and message.channel == ctx.channel

    # stage check function
    def stageCheck(message):
        return capwords(message.content) in all_stages \
               and capwords(message.content) not in removed_stages \
               and message.channel == ctx.channel

    # setup stages
    removed_stages = []
    removed_stages = removed_stages + counters
    p1_dsr_stage = []
    p2_dsr_stage = []

    # setup players
    player1 = p1
    player2 = p2

    # more setup
    main_msg = main_message
    embed = emb

    # loop through 4 stage veto's/selection
    for x in range(4):
        # check which message to send
        if x == 0:
            await ctx.send(f"{player1.mention} please veto a starter.")
        if x == 1:
            await ctx.send(f"{player2.mention} please veto a starter.")
        if x == 2:
            await ctx.send(f"{player2.mention} please veto another starter.")
        if x == 3:
            await ctx.send(f"{player1.mention} please select the stage from "
                           f"the remaining starters.")

        # wait for players stage choice
        msg = await bot.wait_for('message', check=stageCheck, timeout=300)

        # remove messages sent after the embed
        await ctx.channel.purge(after=main_msg)

        # if stage selection
        if x == 3:
            # highlight selected stage
            value = starters_message(removed_stages, capwords(msg.content))
            embed.set_field_at(1, name="Starter Stages",
                               value=value)

            # sets DSR stage to selected stage (will wipe losers DSR later)
            p1_dsr_stage.append(capwords(msg.content))
            p2_dsr_stage.append(capwords(msg.content))
        # otherwise edit game 1 embed to remove the stage
        else:
            # add stage to removed list
            removed_stages.append(capwords(msg.content))
            # wipe out stage from embed
            value = starters_message(removed_stages)
            embed.set_field_at(1, name="Starter Stages", value=value)

        # edit original message with new embed
        await main_msg.edit(embed=embed)

    # get winner of the match
    await ctx.send(f"{newline}GLHF! Once finished, "
                   f"the winner should say `me`.")
    msg = await bot.wait_for('message', check=playerCheck, timeout=1800)

    # switch player 1 to winner and player 2 to loser
    if msg.author == player2:
        player1, player2, p1_dsr_stage, p2_dsr_stage = \
            await player_utils.swap_players(player1, player2,
                                            p1_dsr_stage, p2_dsr_stage)

    # remove stage from losers DSR list
    p2_dsr_stage.pop()

    # edit game 3 embed message
    embed.set_field_at(0, name="`                         Game 1             "
                               "               `",
                       value=f"**Winner:** {player1.mention}", inline=False)
    await main_msg.edit(embed=embed)

    return main_msg, embed, player1, player2, p1_dsr_stage, p2_dsr_stage


async def nonInitial(ctx: discord.ext.commands.Context,
                     bot: discord.ext.commands.Bot,
                     main_message: discord.Message,
                     p1: discord.User, p2: discord.User,
                     p1_dsr: list, p2_dsr: list,
                     emb: discord.Embed,
                     game_num: int, starter_index: int, counter_index: int):
    """
    Runs a nonInitial smash veto process
    :param ctx: context for the message
    :param bot: bot user to use
    :param main_message: original message to edit
    :param p1: player1 user
    :param p2: player2 user
    :param p1_dsr: player1's DSR'd stages
    :param p2_dsr: player2's DSR'd stages
    :param emb: embed to edit
    :param game_num: game number in the set
    :param starter_index: index of start stages field in the embed
    :param counter_index: index of counterpick stages field in the embed
    """

    # setup stuff
    main_msg = main_message
    embed = emb

    # player check function
    def playerCheck(message):
        return message.content.lower() == 'me' \
               and message.channel == ctx.channel

    # stage check function
    def stageCheck(message):
        return capwords(message.content) in all_stages \
               and capwords(message.content) not in removed_stages \
               and message.channel == ctx.channel

    # notify of veto and reset channel after 3 seconds
    await ctx.send(f"Starting Game {game_num} veto...")
    await asyncio.sleep(3)
    await ctx.channel.purge(after=main_msg)

    # setup stages
    removed_stages = []
    p1_dsr_stage = p1_dsr
    p2_dsr_stage = p2_dsr
    removed_stages = removed_stages + p2_dsr_stage

    # setup players
    player1 = p1
    player2 = p2

    # update embed for DSR'd stage
    value1 = starters_message(removed_stages)
    value2 = counters_message(removed_stages)
    embed.set_field_at(starter_index, name="Starter Stages", value=value1)
    embed.set_field_at(counter_index, name="Counterpick Stages", value=value2)
    await main_msg.edit(embed=embed)

    # loop through 3 stage veto's/selection
    for x in range(3):
        if x == 0:
            await ctx.send(f"{player1.mention} please veto a stage.")
        elif x == 1:
            await ctx.send(f"{player1.mention} please veto another stage.")
        elif x == 2:
            await ctx.send(f"{player2.mention} please select the stage.")

        # wait for players stage choice
        msg = await bot.wait_for('message', check=stageCheck, timeout=300)

        # remove messages sent after the embed
        await ctx.channel.purge(after=main_msg)

        # if on stage selection
        if x == 2:
            # highlight selected stage
            value = starters_message(removed_stages, capwords(msg.content))
            embed.set_field_at(starter_index, name="Starter Stages",
                               value=value)
            # highlight selected stage
            value = counters_message(removed_stages, capwords(msg.content))
            embed.set_field_at(counter_index, name="Counterpick Stages",
                               value=value)

            # append to both DSR lists (to be removed when winner is decided
            p1_dsr_stage.append(capwords(msg.content))
            p2_dsr_stage.append(capwords(msg.content))
        else:
            # add stage to removed list
            removed_stages.append(capwords(msg.content))
            # redraw starter stages list
            value = starters_message(removed_stages)
            embed.set_field_at(starter_index, name="Starter Stages",
                               value=value)
            # redraw counterpick stages list
            embed.set_field_at(counter_index, name="Counterpick Stages",
                               value=counters_message(removed_stages))

        # edit original message with new embed
        await main_msg.edit(embed=embed)

    # get winner of the match
    await ctx.send(f"{newline}GLHF! Once finished, the winner should say `me`.")
    msg = await bot.wait_for('message', check=playerCheck, timeout=1800)

    # switch player 1 to winner and player 2 to loser
    if msg.author == player2:
        player1, player2, p1_dsr_stage, p2_dsr_stage = \
            await player_utils.swap_players(player1, player2,
                                            p1_dsr_stage, p2_dsr_stage)

    # remove stage from losers DSR list
    p2_dsr_stage.pop()

    # edit game embed message
    embed.set_field_at(starter_index - 1,
                       name=f"`                         Game {game_num}       "
                            f"                     `",
                       value=f"**Winner:** {player1.mention}", inline=False)
    await main_msg.edit(embed=embed)

    return main_msg, embed, player1, player2, p1_dsr_stage, p2_dsr_stage
