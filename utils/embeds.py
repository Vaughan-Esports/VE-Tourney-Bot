import discord

from settings import tourney_name, footer_note, footer_icon


async def starting():
    # generate embed with orange colour
    embed = discord.Embed(color=discord.Colour.orange())
    # set starting field
    embed.set_author(name="Starting...")

    # return finished embed
    return embed


async def timeout_error():
    # generate embed with red colour
    embed = discord.Embed(colour=discord.Colour.red())
    # set timeout field
    embed.add_field(name="Timeout Error", value="The match timer has expired.",
                    inline=False)
    # set footer
    embed.set_footer(icon_url=footer_icon,
                     text=f"{tourney_name} | {footer_note}")

    # return finished embed
    return embed


async def missing_param_error(error_message: str):
    # generate embed with red colour
    embed = discord.Embed(color=discord.Colour.red())
    # set title field
    embed.add_field(name=f"Missing Parameter Error", value=error_message)
    # set footer
    embed.set_footer(icon_url=footer_icon,
                     text=f"{tourney_name} | {footer_note}")

    # return finished embed
    return embed


async def invalid_param_error(error_message: str):
    # generate embed with red colour
    embed = discord.Embed(color=discord.Colour.red())
    # set title field
    embed.add_field(name=f"Invalid Parameter Error", value=error_message)
    # set footer
    embed.set_footer(icon_url=footer_icon,
                     text=f"{tourney_name} | {footer_note}")

    # return finished embed
    return embed


async def missing_permission_error(error_message: str):
    # generate embed with red colour
    embed = discord.Embed(color=discord.Colour.red())
    # set title field
    embed.add_field(name=f"Missing Permissions", value=error_message)
    # set footer
    embed.set_footer(icon_url=footer_icon,
                     text=f"{tourney_name} | {footer_note}")

    # return finished embed
    return embed


async def match_started(match_channel: discord.TextChannel):
    # generate embed with green colour
    embed = discord.Embed(color=discord.Colour.green())
    # set title field
    embed.add_field(name=f"Match Started!",
                    value=f"Head on over to it: {match_channel.mention}")
    # set footer
    embed.set_footer(icon_url=footer_icon,
                     text=f"{tourney_name} | {footer_note}")

    # return finished embed
    return embed


async def match_archived():
    # generate embed with yellow colour
    embed = discord.Embed(color=discord.Colour.purple())
    # set title field
    embed.add_field(name=f"Match Concluded!",
                    value=f"Thanks for playing! :smile:")
    # set footer
    embed.set_footer(icon_url=footer_icon,
                     text=f"{tourney_name} | {footer_note}")

    # return finished embed
    return embed


async def purged():
    # generate embed with yellow colour
    embed = discord.Embed(color=discord.Colour.green())
    # set title field
    embed.add_field(name=f"Purged!",
                    value=f"All inactive tournament channels were purged.")
    # set footer
    embed.set_footer(icon_url=footer_icon,
                     text=f"{tourney_name} | {footer_note}")

    # return finished embed
    return embed


async def coinflip_winner(winner: discord.User):
    # generate embed with green colour
    embed = discord.Embed(colour=discord.Colour.green())
    # set starting field
    embed.add_field(name="Coinflip",
                    value=f"{winner.mention} won the coinflip!")

    # return finished embed
    return embed
