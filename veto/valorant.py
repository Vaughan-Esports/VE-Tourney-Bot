import asyncio
from string import capwords

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
        return message.content.lower() == 'me' \
               and message.channel == ctx.channel

    # stage check function
    def mapCheck(message):
        return capwords(message.content) in maps \
               and capwords(message.content) not in removed_maps \
               and message.channel == ctx.channel

    # setup players
    player1, player2 = await player_utils.coinflip(ctx, p1, p2)
    await asyncio.sleep(2)

    # maps
    removed_maps = []

    # notifies of veto starts
    await ctx.send(f"Starting veto with {player1.mention} as **Team A** and "
                   f"{player2.mention} as **Team B** in 5 seconds...")

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
        elif x == 4:
            await ctx.send(f"{player1.mention} what is your "
                           f"preferred starting side?")

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

            # edit original message with new embed
            await main_msg.edit(embed=embed)

            # side selection
            await sideSelection(ctx, bot, player1, player2, embed, 2, True)

        # edit original message with new embed
        await main_msg.edit(embed=embed)

    # get winner of the match
    await ctx.send(
        f"{newline}GLHF! Once finished, the winner should say `me`.")
    msg = await bot.wait_for('message', check=playerCheck, timeout=1800)

    # update winner embed
    embed.set_field_at(0,
                       name=f"`                         Game 1               "
                            f"             `",
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
        return message.content.lower() == 'me' \
               and message.channel == ctx.channel

    # stage check function
    def mapCheck(message):
        return capwords(message.content) in maps \
               and capwords(message.content) not in removed_maps \
               and message.channel == ctx.channel

    # setup players
    player1, player2 = await player_utils.coinflip(ctx, p1, p2)
    await asyncio.sleep(1)

    # maps
    removed_maps = []

    # notifies of veto starts
    await ctx.send(
        f"Starting veto with {player1.mention} as **Team A** "
        f"and {player2.mention} as **Team B** in 5 seconds...")

    # delete all messages and begin veto after 5 seconds
    await asyncio.sleep(5)
    await ctx.channel.purge(after=main_msg)

    for x in range(6):
        if x == 0:
            await ctx.send(
                f"{player1.mention} please select a map for game 1.")
        elif x == 1:
            await sideSelection(ctx, bot, player1, player2, embed, 2, False)

            # remove messages sent after the embed
            await ctx.channel.purge(after=main_msg)

            # edit original message with new embed
            await main_msg.edit(embed=embed)

            continue
        elif x == 2:
            await ctx.send(
                f"{player2.mention} please select a map for game 2.")
        elif x == 3:
            await sideSelection(ctx, bot, player1, player2, embed, 5, True)

            # remove messages sent after the embed
            await ctx.channel.purge(after=main_msg)

            # edit original message with new embed
            await main_msg.edit(embed=embed)

            continue
        elif x == 4:
            await ctx.send(f"{player1.mention} please veto a map.")
        elif x == 5:
            await ctx.send(f"{player2.mention} please veto a map.")

        # wait for players stage choice
        msg = await bot.wait_for('message', check=mapCheck, timeout=300)

        # remove messages sent after the embed
        await ctx.channel.purge(after=main_msg)

        # if not last map then strike out
        # FIXME LATER - definitely could do this more efficiently but its
        # 3 am and im tired bruh
        if x == 0:
            selected_map = capwords(msg.content)
            removed_maps.append(selected_map)
            # select map and strike out rest
            embed.set_field_at(1, name="Maps",
                               value=valorant_maps_message(maps,
                                                           selected_map))

            # strike out for next two games as well
            embed.set_field_at(4, name="Maps",
                               value=valorant_maps_message(removed_maps))
            embed.set_field_at(7, name="Maps",
                               value=valorant_maps_message(removed_maps))

        elif x == 2:
            selected_map = capwords(msg.content)
            removed_maps.append(selected_map)
            # select map and strike out rest
            embed.set_field_at(4, name="Maps",
                               value=valorant_maps_message(maps,
                                                           selected_map))

            # strike out for final game as well
            embed.set_field_at(7, name="Maps",
                               value=valorant_maps_message(removed_maps))

        elif x == 4:
            # strike out map
            removed_maps.append(capwords(msg.content))
            embed.set_field_at(7, name="Maps",
                               value=valorant_maps_message(removed_maps))
        elif x == 5:
            removed_maps.append(capwords(msg.content))
            # highlight last map
            selected_map = ""
            for val_map in maps:
                if val_map not in removed_maps:
                    selected_map = val_map
            embed.set_field_at(7, name="Maps",
                               value=valorant_maps_message(removed_maps,
                                                           selected_map))

            # edit original message with new embed
            await main_msg.edit(embed=embed)

            # side selection
            await sideSelection(ctx, bot, player1, player2, embed, 8, True)

        # edit original message with new embed
        await main_msg.edit(embed=embed)

    # winner tracker
    p1_wins = 0
    p2_wins = 0
    # for loop for each games winners
    for x in range(3):

        # get winner of the match
        await ctx.send(
            f"{newline}You may play now play game {x + 1}. GLHF! Once finished, "
            f"the winner should say `me`.")
        msg = await bot.wait_for('message', check=playerCheck, timeout=1800)

        if msg.author == player1:
            p1_wins += 1
        elif msg.author == player2:
            p2_wins += 1

        # update winner embed
        # if winner
        if p1_wins == 2 or p2_wins == 2:
            embed.set_field_at(x * 3,
                               name=f"~~`                         Game {x + 1}"
                                    f"                            `~~",
                               value=f"~~**Winner:** TBD~~",
                               inline=False)
            embed.set_field_at(x * 3 + 1, name="Maps",
                               value=valorant_maps_message(maps))
            embed.set_field_at(x * 3 + 2, name="Starting Sides",
                               value=f"~~**Attack:** TBD "
                                     f"\n**Defense:** TBD,~~")
            await main_msg.edit(embed=embed)

            continue

        # otherwise update normally
        embed.set_field_at(x * 3,
                           name=f"`                         Game {x + 1}        "
                                f"                    `",
                           value=f"**Winner:** {msg.author.mention}",
                           inline=False)
        await main_msg.edit(embed=embed)

        # remove messages sent after the embed
        await ctx.channel.purge(after=main_msg)

        await ctx.send('GG!')

    return main_msg, embed


async def sideSelection(ctx: discord.ext.commands.Context,
                        bot: discord.ext.commands.Bot,
                        player1: discord.User, player2: discord.User,
                        embed: discord.Embed, embed_index: int, p1_pick: bool):
    # side check function
    def sideCheck(message):
        return 'att' in message.content or 'def' in message.content \
               and message.channel == ctx.channel

    # side selection
    if p1_pick:
        await ctx.send(f"{player1.mention} what is your "
                       f"preferred starting side?")
        msg = await bot.wait_for('message', check=sideCheck, timeout=300)
        if 'att' in msg.content:
            embed.set_field_at(embed_index, name="Starting Sides",
                               value=valorant_sides_message(player1,
                                                            player2,
                                                            True),
                               inline=True)
        elif 'def' in msg.content:
            embed.set_field_at(embed_index, name="Starting Sides",
                               value=valorant_sides_message(player1,
                                                            player2,
                                                            False),
                               inline=True)
    else:
        await ctx.send(f"{player2.mention} what is your "
                       f"preferred starting side?")
        msg = await bot.wait_for('message', check=sideCheck, timeout=300)
        if 'att' in msg.content:
            embed.set_field_at(embed_index, name="Starting Sides",
                               value=valorant_sides_message(player1,
                                                            player2,
                                                            False),
                               inline=True)
        elif 'def' in msg.content:
            embed.set_field_at(embed_index, name="Starting Sides",
                               value=valorant_sides_message(player1,
                                                            player2,
                                                            True),
                               inline=True)
