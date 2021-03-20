from smash import match
from utils.message_generators import *


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


async def flipping_coin(dot):
    # generate embed with blue colour
    embed = discord.Embed(colour=discord.Colour.blue())
    # set starting field
    embed.set_author(name=f"Flipping coin{'.' * dot}")

    # return finished embed
    return embed


async def coinflip_winner(winner: discord.User):
    # generate embed with green colour
    embed = discord.Embed(colour=discord.Colour.green())
    # set starting field
    embed.set_author(name=f"{winner.name} won the coinflip!")

    # return finished embed
    return embed


async def smash_veto(max_games: int, match: match.Match):
    # generate embed
    desc = f"{match.players[0].mention} vs {match.players[1].mention} " \
           f"\nThe rulebook can be found [here]({rulebook_url})"
    embed = discord.Embed(title=f"Smash Ultimate Best-of-{max_games} Veto",
                          description=desc,
                          color=discord.Colour.gold())

    # loop through max games times and generate embed fields
    for x in range(1, max_games + 1):
        embed.add_field(
            name=f"`                         Game {x}                         "
                 f"   `",
            value="**Winner:** TBD", inline=False)
        # x - 1 because its using index num
        embed.add_field(name="Starter Stages",
                        value=match.games[x - 1].starters_embed(),
                        inline=True)
        embed.add_field(name="Counterpick Stages",
                        value=match.games[x - 1].counters_embed(),
                        inline=True)

    # set footer
    embed.set_footer(icon_url=footer_icon,
                     text=f"{tourney_name} | {footer_note}")

    # return finished embed
    return embed


async def valorant_veto(player1: discord.User, player2: discord.User,
                        max_games: int):
    # generate embed
    desc = f"**Captains:** {player1.mention}, {player2.mention} " \
           f"\nThe rulebook can be found [here]({rulebook_url})"
    embed = discord.Embed(title=f"VALORANT Best-of-{max_games} Veto",
                          description=desc,
                          color=discord.Colour.gold())

    # loop through max games times and generate embed fields
    for x in range(1, max_games + 1):
        embed.add_field(
            name=f"`                         Game {x}                         "
                 f"   `",
            value="**Winner:** TBD", inline=False)
        embed.add_field(name="Maps", value=valorant_maps_message(),
                        inline=True)

        embed.add_field(name="Starting Sides", value=f"**Attack:** TBD "
                                                     f"\n**Defense:** TBD",
                        inline=True)

    # set footer
    embed.set_footer(icon_url=footer_icon,
                     text=f"{tourney_name} | {footer_note}")

    # return finished embed
    return embed
