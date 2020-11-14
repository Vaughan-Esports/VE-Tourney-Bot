from string import capwords

import discord
from discord.ext import commands

from utils.message_generators import *

from settings import *

# combine lists for all stages list
all_stages = starter_stages + counterpick_stages


async def initial(ctx: discord.ext.commands.Context, bot: discord.ext.commands.Bot, main_msg: discord.Message,
                  player1: discord.User, player2: discord.User, p1_dsr_stage: list, p2_dsr_stage: list,
                  embed: discord.Embed):
    """
    Runs an initial smash veto
    :param ctx:
    :param bot:
    :param main_msg:
    :param player1:
    :param player2:
    :param p1_dsr_stage:
    :param p2_dsr_stage:
    :param embed:
    :return:
    """
    # stage check function
    def stageCheck(message):
        return capwords(message.content) in all_stages and capwords(message.content) not in removed_stages \
               and message.channel == ctx.channel

    # setup stages
    removed_stages = []

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
            await ctx.send(f"{player1.mention} please select the stage from the remaining starters.")

        # wait for players stage choice
        msg = await bot.wait_for('message', check=stageCheck, timeout=300)

        # remove messages sent after the embed
        await ctx.channel.purge(after=main_msg)

        # if stage selection
        if x == 3:
            # highlight selected stage
            embed.set_field_at(1, name="Starter Stages",
                               value=starter_stages_message(removed_stages, capwords(msg.content)))

            # sets DSR stage to selected stage (will wipe losers DSR later)
            p1_dsr_stage.append(capwords(msg.content))
            p2_dsr_stage.append(capwords(msg.content))
        # otherwise edit game 1 embed to remove the stage
        else:
            # add stage to removed list
            removed_stages.append(capwords(msg.content))
            # wipe out stage from embed
            embed.set_field_at(1, name="Starter Stages", value=starter_stages_message(removed_stages))

        # edit original message with new embed
        await main_msg.edit(embed=embed)


async def nonInitial(ctx: discord.ext.commands.Context, bot: discord.ext.commands.Bot, main_msg: discord.Message,
                     player1: discord.User, player2: discord.User, p1_dsr_stage: list, p2_dsr_stage: list,
                     embed: discord.Embed, starter_index: int, counter_index: int, rm_stages=None):
    """
    Runs a nonInitial smash veto process
    :param ctx: context for the message
    :param bot: bot user to use
    :param main_msg: original message to edit
    :param player1: player1 user
    :param player2: player2 user
    :param p1_dsr_stage: player1's DSR'd stages
    :param p2_dsr_stage: player2's DSR'd stages
    :param embed: embed to edit
    :param starter_index: index of start stages field in the embed
    :param counter_index: index of counterpick stages field in the embed
    :param rm_stages: list of removed/veto'd stages
    """

    # if removed stages wasn't given then create empty list
    removed_stages = rm_stages
    if removed_stages is None:
        removed_stages = []

    # stage check function
    def stageCheck(message):
        return capwords(message.content) in all_stages and capwords(message.content) not in removed_stages \
               and message.channel == ctx.channel

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
            if capwords(msg.content) in starter_stages:
                # highlight selected stage
                embed.set_field_at(starter_index, name="Starter Stages",
                                   value=starter_stages_message(removed_stages, capwords(msg.content)))

                # append to both DSR lists (to be removed when winner is decided
                p1_dsr_stage.append(capwords(msg.content))
                p2_dsr_stage.append(capwords(msg.content))
            elif capwords(msg.content) in counterpick_stages:
                # highlight selected stage
                embed.set_field_at(counter_index, name="Counterpick Stages",
                                   value=counterpick_stages_message(removed_stages, capwords(msg.content)))

                # append to both DSR lists (to be removed when winner is decided
                p1_dsr_stage.append(capwords(msg.content))
                p2_dsr_stage.append(capwords(msg.content))
        else:
            # add stage to removed list
            removed_stages.append(capwords(msg.content))

            # check which stage list to wipe out from
            if capwords(msg.content) in starter_stages:
                # wipe out stage from embed
                embed.set_field_at(starter_index, name="Starter Stages", value=starter_stages_message(removed_stages))
            elif capwords(msg.content) in counterpick_stages:
                # wipe out stage from embed
                embed.set_field_at(counter_index, name="Counterpick Stages",
                                   value=counterpick_stages_message(removed_stages))

        # edit original message with new embed
        await main_msg.edit(embed=embed)
