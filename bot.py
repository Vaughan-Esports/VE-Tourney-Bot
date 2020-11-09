import discord
import os
import settings
from discord.ext import commands


bot = discord.ext.commands.Bot('ve!')
BOT_TOKEN = os.getenv('BOT_TOKEN')


@bot.command()
async def veto(ctx, game, p2):
    """
    Start a veto lobby against an opponent
    """
    if game == 'smash':
        embed = discord.Embed(description=f"{ctx.author.mention} vs {p2}"
                                          f"\n\nThe rulebook can be found [here](https://vaughanesports.org/rules)",
                              color=discord.Color(0xffff00))

        # game 1 embed line
        embed.add_field(name="`Game 1                                               `",
                        value="**Winner:** TBD", inline=False)
        embed.add_field(name="Starter Stages",
                        value="Small Battlefield\nPokemon Stadium 2\nSmashville\nTown and City\nFinal Destination",
                        inline=True)
        embed.add_field(name="Counterpick Stages", value="Kalos Pokemon League\nLylat Cruise\nYoshi's Story",
                        inline=True)

        # game 2 embed line
        embed.add_field(name="`Game 2                                               `",
                        value="**Winner:** TBD", inline=False)
        embed.add_field(name="Starter Stages",
                        value="Small Battlefield\nPokemon Stadium 2\nSmashville\nTown and City\nFinal Destination",
                        inline=True)
        embed.add_field(name="Counterpick Stages", value="Kalos Pokemon League\nLylat Cruise\nYoshi's Story",
                        inline=True)

        # game 3 embed line
        embed.add_field(name="`Game 3                                               `",
                        value="**Winner:** TBD", inline=False)
        embed.add_field(name="Starter Stages",
                        value="Small Battlefield\nPokemon Stadium 2\nSmashville\nTown and City\nFinal Destination",
                        inline=True)
        embed.add_field(name="Counterpick Stages", value="Kalos Pokemon League\nLylat Cruise\nYoshi's Story",
                        inline=True)
        embed.set_footer(icon_url="https://vaughanesports.org/assets/Vaughan%20Esports%20Logo.png",
                         text=settings.tourney_name)
        await ctx.send(embed=embed)

bot.run(BOT_TOKEN)
