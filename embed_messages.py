import discord
from message_generators import *
from settings import *


async def timeout_error_message():
    error_embed = discord.Embed(color=0xff0000)
    error_embed.add_field(name="Timeout Error", value="The match timer has expired.", inline=False)
    error_embed.set_footer(icon_url=footer_icon, text=f"{tourney_name} | {footer_note}")

    # return embed
    return error_embed


async def smash_veto_bo3(player1, player2):
    # create embed
    embed = discord.Embed(title="Smash Ultimate Best-of-3 Veto",
                          description=f"{player1.mention} vs {player2.mention}"
                                      f"\nThe rulebook can be found [here]({rulebook_url})",
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
    embed.set_footer(icon_url=footer_icon, text=f"{tourney_name} | {footer_note}")

    # return the embed
    return embed
