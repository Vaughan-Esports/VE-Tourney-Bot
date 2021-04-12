import asyncio
import os

import discord.ext.commands.errors
from discord.ext import commands
from discord.ext.commands import MissingPermissions

from smash.match import Match as SmashMatch
from smash.player import Player
from utils import embeds, player_utils
from utils.message_generators import *
from valorant.match import Match as ValMatch

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


@bot.command(aliases=['ssbu'])
async def smash(ctx, series_length=None, opponent=None):
    """
    Starts a Smash Ult. veto with your opponent
    """

    # guild and category objects
    guild = bot.get_guild(guild_id)
    active_category = guild.get_channel(active_channels_id)

    # check if a valid place to start matches
    if ctx.channel not in active_category.text_channels or \
            ctx.channel.id == match_creation_channel_id:
        text = "You can't do that here! Invoke a match chat first with " \
               "`ve!match {@opponent}`"
        await ctx.send(embed=await embeds.missing_permission_error(text))

    # let user know if they're missing a parameter
    elif series_length is None or opponent is None:
        text = "Initiate a veto with `ve!veto {game} " \
               "{best-of (3 or 5)} @{opponent}` "
        await ctx.send(embed=await embeds.missing_param_error(text))

    # SMASH VETO
    elif series_length == '3' or series_length == '5':
        # get players
        player1, player2 = await player_utils.get_players(ctx)

        # initialize game
        match = SmashMatch(Player(player1),
                           Player(player2),
                           int(series_length))

        # run veto with catch statement in case of time out
        try:
            # run seed selection
            await player_utils.seed_selection(ctx, bot, match)
            await asyncio.sleep(5)

            # run veto's
            while match.winner is None:
                await match.veto(ctx, bot)

        # if the veto times out
        except asyncio.TimeoutError:
            # get error embed and edit original message
            await ctx.send(embed=await embeds.timeout_error())


@bot.command(aliases=['valorant'])
async def val(ctx, series_length=None, opponent=None):
    """
    Runs a VALORANT veto with your opponent
    """
    # guild and category objects
    guild = bot.get_guild(guild_id)
    active_category = guild.get_channel(active_channels_id)

    # check if a valid place to start matches
    if ctx.channel not in active_category.text_channels or \
            ctx.channel.id == match_creation_channel_id:
        text = "You can't do that here! Invoke a match chat first with " \
               "`ve!match {@opponent}`"
        await ctx.send(embed=await embeds.missing_permission_error(text))

    # let user know if they're missing a parameter
    elif series_length is None or opponent is None:
        text = "Initiate a veto with `ve!veto {game} " \
               "{best-of (3 or 5)} @{opponent}` "
        await ctx.send(embed=await embeds.missing_param_error(text))

    elif series_length == '1' or series_length == '3' or series_length == '5':
        # get players
        player1, player2 = await player_utils.get_players(ctx)

        # coinflip to determine seeding
        player1, player2 = await player_utils.coinflip(ctx, player1, player2)
        # initialize game
        match = ValMatch(player1, player2, int(series_length))
        # run veto
        try:
            await match.veto(ctx, bot)

        # if the veto times out
        except asyncio.TimeoutError:
            # get error embed and edit original message
            await ctx.send(embed=await embeds.timeout_error())

    else:
        text = "Matches must either be a best of 1, 3, or 5."
        await ctx.send(embed=await embeds.missing_param_error(text))


@bot.command()
async def match(ctx, opponent=None):
    """
    Creates a private text channel between you and your opponent(s)
    """
    # checks that this it he correct channel to use
    if ctx.channel.id != match_creation_channel_id:
        # get match creation channel object
        match_channel = bot.get_channel(match_creation_channel_id)

        # tell user they have to do it over in match creation channel
        text = f"You can't do that here! Invoke a match chat first over at " \
               f"{match_channel.mention}"
        await ctx.send(embed=await embeds.missing_permission_error(text))

    # let user know if they didn't enter an opponent
    elif opponent is None:
        text = "Initiate a match chat with `ve!match @{opponent}`"
        await ctx.send(embed=await embeds.missing_param_error(text))
        return

    else:
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
            guild.default_role: discord.PermissionOverwrite(
                send_messages=False,
                read_messages=True)
        }

        # create channel
        name = f"{player1.name} vs {player2.name}"
        topic = f"{tourney_name}: {player1.name} vs {player2.name}"
        reason = "User invoked tourney match channel"
        match_channel = await \
            guild.create_text_channel(name,
                                      category=active_category,
                                      topic=topic,
                                      reason=reason,
                                      overwrites=overwrites)

        # send message linking to channel
        await main_msg.edit(embed=await embeds.match_started(match_channel))

        # send instructions into the channel
        await match_channel.send("Once both sides are ready, invoke the veto "
                                 "process with `ve!veto {game}"
                                 "{best-of (3 or 5)} {@opponent}`. "
                                 "For example: `ve!veto smash 3 @Harry`")


@bot.command()
async def close(ctx):
    """
    Moves the channel to the inactive category
    """
    # guild and category objects
    guild = bot.get_guild(guild_id)
    active_category = guild.get_channel(active_channels_id)

    # let user know the channel isn't an active match channel
    if ctx.channel not in active_category.text_channels:
        text = "You can't do that here! You can only close channels in the " \
               "active matches category."
        await ctx.send(embed=await embeds.missing_permission_error(text))

    # let user know they can't close this channel
    elif ctx.channel.id == match_creation_channel_id:
        text = "You can't close this channel! It's not a match channel :smile:"
        await ctx.send(embed=await embeds.missing_permission_error(text))

    else:
        # notifies users of archived channel
        await ctx.send(embed=await embeds.match_archived())

        # guild and category objects
        guild = bot.get_guild(guild_id)
        inactive_category = guild.get_channel(inactive_channels_id)
        # game coordinator role
        game_coordinator = guild.get_role(TO_role_id)

        # overwrites for the match channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                send_messages=False,
                read_messages=True),
            game_coordinator: discord.PermissionOverwrite(add_reactions=True,
                                                          read_messages=True,
                                                          send_messages=True,
                                                          external_emojis=True,
                                                          attach_files=True,
                                                          embed_links=True)
        }

        await ctx.channel.edit(category=inactive_category,
                               overwrites=overwrites)


@bot.command(aliases=['flip'])
async def coinflip(ctx, opponent=None):
    if opponent is None:
        text = "You need to specify an opponent!"
        await ctx.send(embed=await embeds.missing_param_error(text))
    else:
        player1, player2 = await player_utils.get_players(ctx)
        await player_utils.coinflip(ctx, player1, player2)


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
