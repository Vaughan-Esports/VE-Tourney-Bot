import asyncio
import os
import secrets
from os.path import join, dirname

import discord.ext.commands.errors
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from dotenv import load_dotenv

from lol.match import Match as LoLMatch
from osu.match import Match as osuMatch
from settings import active_channels_id, inactive_channels_id, veto_timeout, \
    aram_example
from settings import guild_id, TO_role_id, match_creation_channel_id
from settings import prefix, description, tourney_name, init_match_message
from settings import smash_example, valorant_example, osu_example
from smash.match import Match as SmashMatch
from smash.player import Player
from utils import embeds, player_utils
from utils.checks import doneCheck, URLCheck
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

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


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
        text = "Initiate a veto with `ve!smash " \
               "{best-of} @opponent` "
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

    else:
        text = f"Matches must either be a best of 3 or 5.\n\n" \
               f"Example: {smash_example}"
        await ctx.send(embed=await embeds.invalid_param_error(text))


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

        # start delay
        await ctx.send(f"Starting veto with {player1.mention} as "
                       f"**Captain 1** and {player2.mention} "
                       f"as **Captain 2** in 5 seconds...")
        await asyncio.sleep(5)

        # run veto
        try:
            await match.veto(ctx, bot)

        # if the veto times out
        except asyncio.TimeoutError:
            # get error embed and edit original message
            await ctx.send(embed=await embeds.timeout_error())

    else:
        text = f"Matches must either be a best of 1, 3, or 5.\n\n" \
               f"Example: {valorant_example}"
        await ctx.send(embed=await embeds.invalid_param_error(text))


@bot.command()
async def osu(ctx, series_length=None, opponent=None):
    """
    Starts an osu! veto with your opponent
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

    # OSU VETO
    elif series_length == '3' or series_length == '5' or series_length == '7':
        # get players
        player1, player2 = await player_utils.get_players(ctx)

        # coinflip to determine seeding
        player1, player2 = await player_utils.coinflip(ctx, player1, player2)

        # send creation info
        msg = await ctx.send(f'{player1.mention}, setup a lobby with '
                             f'the commands in `osu!`: \n\n'
                             f'`!mp make VES: {player1.name} vs {player2.name}`'
                             f'\n'
                             f'`!mp password {secrets.randbits(16)}`'
                             f'\n'
                             f'`!mp size 5`'
                             f'\n'
                             f'`!mp set 2 3`'
                             f'\n\n')
        await ctx.send(f'Say `done` when finished and '
                       f'{player2.mention} has joined the lobby.')

        # pin the message
        await msg.pin()

        await bot.wait_for('message',
                           check=doneCheck(ctx),
                           timeout=veto_timeout)

        # get match history link
        await ctx.send(f'Paste the match history link into chat.'
                       f'\nFound here: https://media.discordapp.net/attachments/832801322771808317/842564411817197598/unknown.png?width=457&height=225')

        msg = await bot.wait_for('message',
                                 check=URLCheck(ctx),
                                 timeout=veto_timeout)

        # initialize game
        match = osuMatch(player1,
                         player2,
                         int(series_length),
                         msg.content)

        # start delay
        await ctx.send(f"Starting veto with {player1.mention} as "
                       f"**Player 1** and {player2.mention} "
                       f"as **Player 2** in 5 seconds...")
        await asyncio.sleep(5)

        # run veto
        try:
            while match.winner is None:
                await match.veto(ctx, bot)

        # if the veto times out
        except asyncio.TimeoutError:
            # get error embed and edit original message
            await ctx.send(embed=await embeds.timeout_error())

    else:
        text = f"Matches must either be a best of 3, 5, or 7.\n\n" \
               f"Example: {osu_example}"
        await ctx.send(embed=await embeds.invalid_param_error(text))


@bot.command()
async def aram(ctx, series_length=None, opponent=None):
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
        text = "Initiate a veto with `ve!aram " \
               "{best-of} @opponent` "
        await ctx.send(embed=await embeds.missing_param_error(text))

    # SMASH VETO
    elif series_length == '3' or series_length == '5':
        # get players
        player1, player2 = await player_utils.get_players(ctx)

        # initialize game
        match = LoLMatch(player1, player2, int(series_length))

        # run veto with catch statement in case of time out
        try:

            # run veto's
            while match.winner is None:
                await match.veto(ctx, bot)

        # if the veto times out
        except asyncio.TimeoutError:
            # get error embed and edit original message
            await ctx.send(embed=await embeds.timeout_error())

    else:
        text = f"Matches must either be a best of 3 or 5.\n\n" \
               f"Example: {aram_example}"
        await ctx.send(embed=await embeds.invalid_param_error(text))


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
        await match_channel.send(init_match_message)


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

        # notifies users of archived channel
        await ctx.send(embed=await embeds.match_archived())


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


bot.run(os.getenv('BOT_TOKEN'))
