import asyncio
import discord
import os
from settings import *
from discord.ext import commands

intents = discord.Intents.default()
allowed_mentions = discord.AllowedMentions(everyone=False, users=True, roles=True)
bot = discord.ext.commands.Bot('ve!', intents=intents, description="Tournament Bot for Vaughan Esports",
                               case_insensitive=True, allowed_mentions=allowed_mentions)
BOT_TOKEN = os.getenv('BOT_TOKEN')


def starter_stages_message(removed_stages=None, selected_stage=None):
    """
    Generates starter stages list
    :param removed_stages: list of veto'd stages (exact spellings)
    :return: string for embed value
    """
    # blank string
    message = ""
    # loop through starter stages
    for x in range(len(starter_stages)):
        # if removed stages is none then don't worry about striking out
        if removed_stages is not None:
            # crosses stage out if its in the removed_stages list
            if starter_stages[x] in removed_stages:
                message = f"{message}~~{starter_stages[x]}~~\n"
            # bolds the stage if its selected
            elif starter_stages[x] == selected_stage:
                message = f"{message}⮕**{starter_stages[x]}**\n"
            # else concatenate the new stage name regularly
            else:
                message = f"{message}{starter_stages[x]}\n"
        # else concatenate the new stage name regularly
        else:
            message = f"{message}{starter_stages[x]}\n"
    return message


def counterpick_stages_message(removed_stages=None):
    """
    Generates counterpick stages list
    :param removed_stages: list of veto'd stages (exact spellings)
    :return: string for embed value
    """
    # blank string
    message = ""
    # loop through counterpick stages
    for x in range(len(counterpick_stages)):
        # if removed stages is none then don't worry about striking out
        if removed_stages is not None:
            # crosses stage out if its in the removed_stages list
            if starter_stages[x] in removed_stages:
                message = f"{message}~~{counterpick_stages[x]}~~\n"
            # else concatenate the new stage name regularly
            else:
                message = f"{message}{counterpick_stages[x]}\n"
        # else concatenate the new stage name regularly
        else:
            message = f"{message}{counterpick_stages[x]}\n"
    return message


@bot.command()
async def veto(ctx, game, seriesLength, p2):
    """
    Starts a veto lobby with your opponent
    """
    if game == 'smash' and seriesLength == 'bo3':
        embed = discord.Embed(description=f"{ctx.author.mention} vs {p2}"
                                          f"\nThe rulebook can be found [here](https://vaughanesports.org/rules)",
                              color=discord.Color(0xffff00))

        # game 1 embed line
        embed.add_field(name="`                         Game 1                            `",
                        value="**Winner:** TBD", inline=False)
        embed.add_field(name="Starter Stages", value=starter_stages_message(), inline=True)
        embed.add_field(name="Counterpick Stages", value=counterpick_stages_message(), inline=True)

        # game 2 embed line
        embed.add_field(name="`                         Game 2                            `",
                        value="**Winner:** TBD", inline=False)
        embed.add_field(name="Starter Stages", value=starter_stages_message(), inline=True)
        embed.add_field(name="Counterpick Stages", value=counterpick_stages_message(), inline=True)

        # game 3 embed line
        embed.add_field(name="`                         Game 3                            `",
                        value="**Winner:** TBD", inline=False)
        embed.add_field(name="Starter Stages", value=starter_stages_message(), inline=True)
        embed.add_field(name="Counterpick Stages", value=counterpick_stages_message(), inline=True)
        embed.set_footer(icon_url="https://vaughanesports.org/assets/Vaughan%20Esports%20Logo.png",
                         text=f"{tourney_name} | DM Brandon for help or ping here.")

        main_msg = await ctx.send(embed=embed)

        # setup removed stages
        removed_stages = []

        # determine higher seed
        player1 = ctx.author.mention
        player2 = p2
        player_msg = await ctx.send("Player 1 (the higher seed) say \"**me**\"")

        # checks which user says me
        def playerCheck(message):
            return message.content == 'me' and message.channel == ctx.channel

        msg = await bot.wait_for('message', check=playerCheck)
        # changes player order if player 2 said they were first seed
        if msg.author.mention == player2:
            player1 = msg.author.mention
            player2 = ctx.author.mention
        players_msg = await ctx.send(f"Starting veto with {player1} as **Player 1** and {player2} as **Player 2**.")
        # delete all messages and begin veto after 5 seconds
        await asyncio.sleep(5)
        await player_msg.delete()
        await msg.delete()
        await players_msg.delete()

        # stage check function
        def stageCheck(message):
            return message.content.title() in starter_stages and message.content.title() not in removed_stages \
                   and message.channel == ctx.channel

        # first game veto process
        for x in range(4):
            # create msg variable
            veto_msg = None
            if x == 0:
                veto_msg = await ctx.send(f"{player1} please veto a starter.")
            if x == 1:
                veto_msg = await ctx.send(f"{player2} please veto a starter.")
            if x == 2:
                veto_msg = await ctx.send(f"{player2} please veto another starter.")
            if x == 3:
                veto_msg = await ctx.send(f"{player1} please pick a map from the remaining starters.")

            # players message
            msg = await bot.wait_for('message', check=stageCheck)

            # remove messages
            await veto_msg.delete()
            await msg.delete()

            # edit game 1 embed to remove the stage
            if x == 3:
                embed.set_field_at(1, name="Starter Stages",
                                   value=starter_stages_message(removed_stages, msg.content.title()))
            else:
                # add stage to removed list
                removed_stages.append(msg.content.title())
                embed.set_field_at(1, name="Starter Stages", value=starter_stages_message(removed_stages))

            # edit original message with new embed
            await main_msg.edit(embed=embed)


bot.run(BOT_TOKEN)
