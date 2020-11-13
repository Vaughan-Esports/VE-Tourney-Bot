import asyncio
import os
from string import capwords

from utils import embeds
from utils import player_utils
import discord
import utils
from discord.ext import commands
from utils.message_generators import *


intents = discord.Intents.default()
allowed_mentions = discord.AllowedMentions(everyone=False, users=True, roles=True)
bot = discord.ext.commands.Bot('ve!', intents=intents, description="Tournament Bot for Vaughan Esports",
                               case_insensitive=True, allowed_mentions=allowed_mentions)
BOT_TOKEN = os.getenv('BOT_TOKEN')


@bot.command()
async def veto(ctx, game, seriesLength, p2):
    """
    Starts a veto lobby with your opponent
    """
    if game.lower() == 'smash' and seriesLength.lower() == 'bo3':
        # starting/loading embed
        main_msg = await ctx.send(embed=await embeds.starting())

        # player objects
        player1 = ctx.author
        player2 = await bot.fetch_user(p2[3:-1])

        # send first veto embed
        embed = await embeds.smash_veto_bo3(player1, player2)
        await main_msg.edit(embed=embed)

        try:
            # HIGHER SEED SELECTION
            await ctx.send(f"{newline}Player 1 (the higher seed) say `me`")

            # checks which user says me
            def playerCheck(message):
                return message.content.lower() == 'me' and message.channel == ctx.channel

            msg = await bot.wait_for('message', check=playerCheck, timeout=300)

            # changes player order if player 2 said they were first seed
            if msg.author == player2:
                player1 = player2
                player2 = ctx.author

            # notifies of veto starts
            await ctx.send(f"Starting veto with {player1.mention} as **Player 1** and {player2.mention} "
                           f"as **Player 2** in 5 seconds...")

            # delete all messages and begin veto after 5 seconds
            await asyncio.sleep(5)
            await ctx.channel.purge(after=main_msg)

            # setup stages
            removed_stages = []
            p1_dsr_stage = []
            p2_dsr_stage = []
            all_stages = starter_stages + counterpick_stages

            # stage check function
            def stageCheck(message):
                return capwords(message.content) in all_stages and capwords(message.content) not in removed_stages \
                       and message.channel == ctx.channel

            # FIRST GAME VETO PROCESS
            # cross out all counterpick stages as they are not valid for first veto
            embed.set_field_at(2, name="Counterpick Stages",
                               value=counterpick_stages_message(counterpick_stages))
            await main_msg.edit(embed=embed)

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

            # get winner of the match
            await ctx.send(f"{newline}GLHF! Once finished, the winner should say `me`.")
            msg = await bot.wait_for('message', check=playerCheck, timeout=1800)

            # switch player 1 to winner and player 2 to loser
            if msg.author == player2:
                player1, player2, p1_dsr_stage, p2_dsr_stage = await player_utils.swap_players(player1, player2,
                                                                                               p1_dsr_stage,
                                                                                               p2_dsr_stage)

            # remove stage from losers DSR list
            p2_dsr_stage.pop()

            # edit game 1 embed message
            embed.set_field_at(0, name="`                         Game 1                            `",
                               value=f"**Winner:** {player1.mention}", inline=False)
            await main_msg.edit(embed=embed)

            # notify of veto and reset channel after 3 seconds
            await ctx.send(f"Starting Game 2 veto...")
            await asyncio.sleep(3)
            await ctx.channel.purge(after=main_msg)

            # SECOND GAME VETO PROCESS
            # reset veto'd stages
            removed_stages = []

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
                        embed.set_field_at(4, name="Starter Stages",
                                           value=starter_stages_message(removed_stages, capwords(msg.content)))

                        # append to both DSR lists (to be removed when winner is decided
                        p1_dsr_stage.append(capwords(msg.content))
                        p2_dsr_stage.append(capwords(msg.content))
                    elif capwords(msg.content) in counterpick_stages:
                        # highlight selected stage
                        embed.set_field_at(5, name="Counterpick Stages",
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
                        embed.set_field_at(4, name="Starter Stages", value=starter_stages_message(removed_stages))
                    elif capwords(msg.content) in counterpick_stages:
                        # wipe out stage from embed
                        embed.set_field_at(5, name="Counterpick Stages",
                                           value=counterpick_stages_message(removed_stages))

                # edit original message with new embed
                await main_msg.edit(embed=embed)

            # get winner of the match
            await ctx.send(f"{newline}GLHF! Once finished, the winner should say `me`.")
            msg = await bot.wait_for('message', check=playerCheck, timeout=1800)

            # switch player 1 to winner and player 2 to loser
            if msg.author == player2:
                player1, player2, p1_dsr_stage, p2_dsr_stage = await player_utils.swap_players(player1, player2,
                                                                                               p1_dsr_stage,
                                                                                               p2_dsr_stage)

            # remove stage from losers DSR list
            p2_dsr_stage.pop()

            # edit game 2 embed message
            embed.set_field_at(3, name="`                         Game 2                            `",
                               value=f"**Winner:** {player1.mention}", inline=False)
            await main_msg.edit(embed=embed)

            # THIRD GAME VETO PROCESS
            # exits if a DSR stage list is longer than 1
            if len(p1_dsr_stage) > 1 or len(p2_dsr_stage) > 1:
                # reset messages
                await ctx.channel.purge(after=main_msg)

                # cross out all of game 3
                embed.set_field_at(6, name='~~`                         Game 3                            `~~',
                                   value='~~**Winner:**~~', inline=False)
                embed.set_field_at(7, name="Starter Stages", value=starter_stages_message(starter_stages))
                embed.set_field_at(8, name="Counterpick Stages", value=counterpick_stages_message(counterpick_stages))
                await main_msg.edit(embed=embed)

                # final message
                await ctx.send("GG!")
                return

            # notify of veto and reset channel after 3 seconds
            await ctx.send(f"Starting Game 3 veto...")
            await asyncio.sleep(3)
            await ctx.channel.purge(after=main_msg)

            # clears removed stages adds winners DSR stage to it
            removed_stages = [p1_dsr_stage]

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
                        embed.set_field_at(7, name="Starter Stages",
                                           value=starter_stages_message(removed_stages, capwords(msg.content)))

                        # append to both DSR lists (to be removed when winner is decided
                        p1_dsr_stage.append(capwords(msg.content))
                        p2_dsr_stage.append(capwords(msg.content))
                    elif capwords(msg.content) in counterpick_stages:
                        # highlight selected stage
                        embed.set_field_at(8, name="Counterpick Stages",
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
                        embed.set_field_at(7, name="Starter Stages", value=starter_stages_message(removed_stages))
                    elif capwords(msg.content) in counterpick_stages:
                        # wipe out stage from embed
                        embed.set_field_at(8, name="Counterpick Stages",
                                           value=counterpick_stages_message(removed_stages))

                # edit original message with new embed
                await main_msg.edit(embed=embed)

            # get winner of the match
            await ctx.send(f"{newline}GLHF! Once finished, the winner should say `me`.")
            msg = await bot.wait_for('message', check=playerCheck, timeout=1800)

            # edit game 3 embed message
            embed.set_field_at(6, name="`                         Game 3                            `",
                               value=f"**Winner:** {player1.mention}", inline=False)
            await main_msg.edit(embed=embed)

            # final message
            await ctx.send("GG!")

        # if the veto times out
        except asyncio.TimeoutError:
            # purge all messages after original message
            await ctx.channel.purge(after=main_msg)

            # get error embed and edit original message
            error_embed = await embeds.timeout_error()
            await main_msg.edit(embed=error_embed)


bot.run(BOT_TOKEN)
