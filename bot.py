import asyncio
import os

import discord.ext.commands.errors
from discord.ext import commands
from discord.ext.commands import MissingPermissions

from utils import embeds, player_utils
from utils.message_generators import *
from veto import smash, valorant

intents = discord.Intents.default()
allowed_mentions = discord.AllowedMentions(everyone=False, users=True,
                                           roles=True)
bot = discord.ext.commands.Bot(command_prefix=prefix, intents=intents,
                               description=description, case_insensitive=True,
                               allowed_mentions=allowed_mentions)
BOT_TOKEN = os.getenv('BOT_TOKEN')


@bot.command()
async def veto(ctx, game=None, series_length=None, opponent=None):
    """
    Starts a veto lobby with your opponent
    """
    # let user know if they're missing a parameter
    if game is None or series_length is None or opponent is None:
        text = "Initiate a veto with `ve!veto {game} {series_length} @{" \
               "opponent}` "
        await ctx.send(embed=await embeds.missing_param_error(text))

    elif ctx.channel.id in restricted_channels_ids:
        text = "You can't do that here! Invoke a match chat first with " \
               "`ve!match {@opponent}`"
        await ctx.send(embed=await embeds.missing_permission_error(text))

    # smash best of 3 veto
    elif game.lower() == 'smash' and series_length.lower() == 'bo3':
        # starting/loading embed
        main_msg = await ctx.send(embed=await embeds.starting())

        # player
        player1, player2 = await player_utils.get_players(ctx)

        # send first veto embed
        embed = await embeds.smash_veto(player1, player2, 3)
        await main_msg.edit(embed=embed)

        # run veto with catch statement in case of time out
        try:
            # HIGHER SEED SELECTION
            await ctx.send(f"{newline}Player 1 (the higher seed) say `me`")

            # checks which user says me
            def playerCheck(message):
                return message.content.lower() == 'me' \
                       and message.channel == ctx.channel

            msg = await bot.wait_for('message', check=playerCheck, timeout=300)

            # changes player order if player 2 said they were first seed
            if msg.author == player2:
                player1 = player2
                player2 = ctx.author

            # notifies of veto starts
            await ctx.send(f"Starting veto with {player1.mention} as "
                           f"**Player 1** and {player2.mention} "
                           f"as **Player 2** in 5 seconds...")

            # delete all messages and begin veto after 5 seconds
            await asyncio.sleep(5)
            await ctx.channel.purge(after=main_msg)

            # FIRST GAME VETO PROCESS
            # cross out all counterpick stages as they are not valid for
            # first veto
            embed.set_field_at(2, name="Counterpick Stages",
                               value=counters_message(counters))
            await main_msg.edit(embed=embed)

            # run initial game veto
            main_msg, embed, player1, player2, p1_dsr_stage, p2_dsr_stage = \
                await smash.initial(ctx, bot, main_msg, player1, player2,
                                    embed)

            # SECOND GAME VETO PROCESS
            main_msg, embed, player1, player2, p1_dsr_stage, p2_dsr_stage = \
                await smash.nonInitial(ctx, bot, main_msg, player1, player2,
                                       p1_dsr_stage, p2_dsr_stage, embed,
                                       2, 4, 5)

            # THIRD GAME VETO PROCESS
            # exits if a DSR stage list is longer than 1
            if len(p1_dsr_stage) > 1 or len(p2_dsr_stage) > 1:
                # reset messages
                await ctx.channel.purge(after=main_msg)

                # cross out all of game 3
                embed.set_field_at(6, name='~~`                         Game '
                                           '3                            `~~',
                                   value='~~**Winner:**~~', inline=False)
                embed.set_field_at(7, name="Starter Stages",
                                   value=starters_message(starters))
                embed.set_field_at(8, name="Counterpick Stages",
                                   value=counters_message(counters))
                await main_msg.edit(embed=embed)

                # final message
                await ctx.send("GG!")
                return

            # runs non initial veto with player 1's DSR start on removed stages
            await smash.nonInitial(ctx, bot, main_msg, player1, player2,
                                   p1_dsr_stage, p2_dsr_stage, embed, 3, 7, 8)
            # final message
            await ctx.send("GG!")

        # if the veto times out
        except asyncio.TimeoutError:
            # purge all messages after original message
            await ctx.channel.purge(after=main_msg)

            # get error embed and edit original message
            error_embed = await embeds.timeout_error()
            await main_msg.edit(embed=error_embed)

    # elif smash bo5
    # FIXME LATER - LMAO I COPY PASTED THIS SHIT FROM BO3, DEF NOT OPTIMIZED
    elif game.lower() == 'smash' and series_length.lower() == 'bo5':
        # starting/loading embed
        main_msg = await ctx.send(embed=await embeds.starting())

        # player objects
        player1, player2 = await player_utils.get_players(ctx)

        # send first veto embed
        embed = await embeds.smash_veto(player1, player2, 5)
        await main_msg.edit(embed=embed)

        # run veto with catch statement in case of time out
        try:
            # HIGHER SEED SELECTION
            await ctx.send(f"{newline}Player 1 (the higher seed) say `me`")

            # checks which user says me
            def playerCheck(message):
                return message.content.lower() == 'me' \
                       and message.channel == ctx.channel

            msg = await bot.wait_for('message', check=playerCheck, timeout=300)

            # changes player order if player 2 said they were first seed
            if msg.author == player2:
                player1 = player2
                player2 = ctx.author

            # notifies of veto starts
            await ctx.send(f"Starting veto with {player1.mention} as "
                           f"**Player 1** and {player2.mention} "
                           f"as **Player 2** in 5 seconds...")

            # delete all messages and begin veto after 5 seconds
            await asyncio.sleep(5)
            await ctx.channel.purge(after=main_msg)

            # FIRST GAME VETO PROCESS
            # cross out all counterpick stages as they are not valid for
            # first veto
            embed.set_field_at(2, name="Counterpick Stages",
                               value=counters_message(counters))
            await main_msg.edit(embed=embed)

            # run initial game veto
            main_msg, embed, player1, player2, p1_dsr_stage, p2_dsr_stage = \
                await smash.initial(ctx, bot, main_msg, player1, player2,
                                    embed)

            # SECOND GAME VETO PROCESS
            main_msg, embed, player1, player2, p1_dsr_stage, p2_dsr_stage = \
                await smash.nonInitial(ctx, bot, main_msg, player1, player2,
                                       p1_dsr_stage, p2_dsr_stage, embed,
                                       2, 4, 5)

            # THIRD GAME VETO PROCESS
            main_msg, embed, player1, player2, p1_dsr_stage, p2_dsr_stage = \
                await smash.nonInitial(ctx, bot, main_msg, player1, player2,
                                       p1_dsr_stage, p2_dsr_stage, embed,
                                       3, 7, 8)

            # FOURTH GAME VETO PROCESS
            # exits if a DSR stage list is longer than 2
            if len(p1_dsr_stage) > 2 or len(p2_dsr_stage) > 2:
                # reset messages
                await ctx.channel.purge(after=main_msg)

                # cross out all of game 4
                embed.set_field_at(9, name='~~`                         Game '
                                           '4                            `~~',
                                   value='~~**Winner:**~~', inline=False)
                embed.set_field_at(10, name="Starter Stages",
                                   value=starters_message(starters))
                embed.set_field_at(11, name="Counterpick Stages",
                                   value=counters_message(counters))
                await main_msg.edit(embed=embed)

                # cross out all of game 5
                embed.set_field_at(12, name='~~`                         '
                                            'Game 5                         '
                                            '   `~~',
                                   value='~~**Winner:**~~', inline=False)
                embed.set_field_at(13, name="Starter Stages",
                                   value=starters_message(starters))
                embed.set_field_at(14, name="Counterpick Stages",
                                   value=counters_message(counters))
                await main_msg.edit(embed=embed)

                # send final message and return
                await ctx.send('GG!')
                return

            # run veto for game 4
            main_msg, embed, player1, player2, p1_dsr_stage, p2_dsr_stage = \
                await smash.nonInitial(ctx, bot, main_msg, player1, player2,
                                       p1_dsr_stage, p2_dsr_stage, embed,
                                       4, 10, 11)

            # FIFTH GAME VETO PROCESS
            # exits if a DSR stage list is longer than 2
            if len(p1_dsr_stage) > 2 or len(p2_dsr_stage) > 2:
                # reset messages
                await ctx.channel.purge(after=main_msg)

                # cross out all of game 5
                embed.set_field_at(12, name='~~`                         '
                                            'Game 5                         '
                                            '   `~~',
                                   value='~~**Winner:**~~', inline=False)
                embed.set_field_at(13, name="Starter Stages",
                                   value=starters_message(starters))
                embed.set_field_at(14, name="Counterpick Stages",
                                   value=counters_message(counters))
                await main_msg.edit(embed=embed)

                # send final message and return
                await ctx.send('GG!')
                return

            # run veto for game 5
            main_msg, embed, player1, player2, p1_dsr_stage, p2_dsr_stage = \
                await smash.nonInitial(ctx, bot, main_msg, player1, player2,
                                       p1_dsr_stage, p2_dsr_stage, embed,
                                       5, 13, 14)

            # final message
            await ctx.send('GG!')

        # if the veto times out
        except asyncio.TimeoutError:
            # purge all messages after original message
            await ctx.channel.purge(after=main_msg)

            # get error embed and edit original message
            error_embed = await embeds.timeout_error()
            await main_msg.edit(embed=error_embed)

    elif 'val' in game.lower():
        main_msg = await ctx.send(embed=await embeds.starting())

        # player objects
        player1, player2 = await player_utils.get_players(ctx)

        games = int(series_length[2])

        # send first veto embed
        embed = await embeds.valorant_veto(player1, player2, games)
        await main_msg.edit(embed=embed)

        # run veto
        try:
            # best of 1 veto
            if games == 1:
                embed, main_msg = await valorant.bo1(ctx, bot, main_msg,
                                                     player1, player2, embed)
                await ctx.send('GG!')
            # best of 3 veto
            elif games == 3:
                embed, main_msg = await valorant.bo3(ctx, bot, main_msg,
                                                     player1, player2, embed)
                await ctx.send('GG!')

        # if the veto times out
        except asyncio.TimeoutError:
            # purge all messages after original message
            await ctx.channel.purge(after=main_msg)

            # get error embed and edit original message
            error_embed = await embeds.timeout_error()
            await main_msg.edit(embed=error_embed)


@bot.command()
async def match(ctx, opponent=None):
    """
    Creates a private text channel between you and your opponent(s)
    """
    # let user know if they didn't enter an opponent
    if opponent is None:
        text = "Initiate a match chat with `ve!match @{opponent}`"
        await ctx.send(embed=await embeds.missing_param_error(text))
        return

    # run command if they have proper arguments
    # send initial starting message
    main_msg = await ctx.send(embed=await embeds.starting())

    # player objects
    player1, player2 = await player_utils.get_players(ctx)

    # guild and category objects
    guild = bot.get_guild(guild_id)
    active_category = guild.get_channel(active_channels_id)

    # game coordinator role
    game_coordinator = guild.get_role(TO_role_id)

    # overwrites for the match channel
    overwrites = {
        player1: discord.PermissionOverwrite(add_reactions=True,
                                             read_messages=True,
                                             send_messages=True,
                                             external_emojis=True,
                                             attach_files=True,
                                             embed_links=True),

        player2: discord.PermissionOverwrite(add_reactions=True,
                                             read_messages=True,
                                             send_messages=True,
                                             external_emojis=True,
                                             attach_files=True,
                                             embed_links=True),

        game_coordinator: discord.PermissionOverwrite(add_reactions=True,
                                                      read_messages=True,
                                                      send_messages=True,
                                                      external_emojis=True,
                                                      attach_files=True,
                                                      embed_links=True),
        guild.default_role: discord.PermissionOverwrite(send_messages=False)
    }

    # create channel
    name = f"{player1.name} vs {player2.name}"
    topic = f"{tourney_name}: {player1.name} vs {player2.name}"
    reason = "User invoked tourney match channel"
    match_channel = await guild.create_text_channel(name,
                                                    category=active_category,
                                                    topic=topic,
                                                    reason=reason,
                                                    overwrites=overwrites)

    # send message linking to channel
    await main_msg.edit(embed=await embeds.match_started(match_channel))

    # send instructions into the channel
    await match_channel.send("Once both sides are ready, invoke the veto "
                             "process with `ve!veto {game} "
                             "{series_length} {@opponent}`")


@bot.command()
async def close(ctx):
    """
    Moves the channel to the inactive category
    """
    # message placeholder
    main_msg = await ctx.send(embed=await embeds.starting())

    if ctx.channel.id in restricted_channels_ids:
        text = "You can't do that here! You can only close channels in the " \
               "active matches category."
        await main_msg.edit(embed=await embeds.missing_permission_error(text))

    else:
        # guild and category objects
        guild = bot.get_guild(guild_id)
        inactive_category = guild.get_channel(inactive_channels_id)

        # overwrites for the match channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                send_messages=False)
        }

        await ctx.channel.edit(category=inactive_category,
                               overwrites=overwrites)
        # notifies users of archived channel
        await main_msg.edit(embed=await embeds.match_archived())


@bot.command()
async def coinflip(ctx, opponent=None):
    if opponent is None:
        text = "You need to specify an opponent!"
        await ctx.send(embed=await embeds.missing_param_error(text))
    else:
        await player_utils.coinflip(ctx, ctx.author, ctx.message.mentions[0])


@bot.command()
@commands.has_permissions(administrator=True)
async def purge(ctx):
    """
    Purges all channels in the inactive category
    """
    # message placeholder
    main_msg = await ctx.send(embed=await embeds.starting())

    # guild and category objects
    guild = bot.get_guild(guild_id)
    inactive_category = guild.get_channel(inactive_channels_id)

    for channel in inactive_category.text_channels:
        await channel.delete()

    await main_msg.edit(embed=await embeds.purged())


@purge.error
async def purge_error(ctx, error):
    if isinstance(error, MissingPermissions):
        text = "You don't have permission to purge tournament channels!"
        await ctx.send(embed=await embeds.missing_permission_error(text))


bot.run(BOT_TOKEN)
