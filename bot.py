import asyncio
import os

import discord.ext.commands.errors
from discord.ext import commands
from discord.ext.commands import MissingPermissions

from utils import embeds, player_utils
from utils.message_generators import *

intents = discord.Intents.default()
allowed_mentions = discord.AllowedMentions(everyone=False,
                                           users=True,
                                           roles=True)
bot = discord.ext.commands.Bot(command_prefix=prefix,
                               intents=intents,
                               description=description,
                               case_insensitive=True,
                               allowed_mentions=allowed_mentions)

BOT_TOKEN = os.getenv('BOT_TOKEN')


@bot.command()
async def veto(ctx, game=None, series_length=None, opponent=None):
    """
    Starts a veto lobby with your opponent
    """
    # let user know if they're missing a parameter
    if game is None or series_length is None or opponent is None:
        text = "Initiate a veto with `ve!veto {game} " \
               "{series_length (3 or 5)} @{opponent}` "
        await ctx.send(embed=await embeds.missing_param_error(text))

    elif ctx.channel.id in restricted_channels_ids:
        text = "You can't do that here! Invoke a match chat first with " \
               "`ve!match {@opponent}`"
        await ctx.send(embed=await embeds.missing_permission_error(text))

    # smash best of 3 veto
    elif game.lower() == 'smash' and '3' in series_length:
        # player
        player1, player2 = await player_utils.get_players(ctx)

        # send first veto embed
        await ctx.send(embed=await embeds.smash_veto(player1, player2, 3))

        # run veto with catch statement in case of time out
        try:


        # if the veto times out
        except asyncio.TimeoutError:
            # get error embed and edit original message
            await ctx.send(embed=await embeds.timeout_error())

    # elif smash bo5
    elif game.lower() == 'smash' and series_length.lower() == 'bo5':
        # player objects
        player1, player2 = await player_utils.get_players(ctx)

        # send first veto embed
        await ctx.send(embed=await embeds.smash_veto(player1, player2, 5))

        # run veto with catch statement in case of time out
        try:


        # if the veto times out
        except asyncio.TimeoutError:
            # get error embed and edit original message
            await ctx.send(embed=await embeds.timeout_error())

    elif 'val' in game.lower():
        # player objects
        player1, player2 = await player_utils.get_players(ctx)

        games = int(series_length[2])

        # send first veto embed
        await ctx.send(embed=embeds.valorant_veto(player1, player2, games))

        # run veto
        try:


        # if the veto times out
        except asyncio.TimeoutError:
            # get error embed and edit original message
            await ctx.send(embed=await embeds.timeout_error())


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
