import discord
import os
import settings
from discord.ext import commands

intents = discord.Intents.default()
bot = discord.ext.commands.Bot('ve!', intents=intents, description="Tournament Bot for Vaughan Esports",
                               case_insensitive=True)
BOT_TOKEN = os.getenv('BOT_TOKEN')

# get stage list from settings file
starter_stages = ""  # blank string
# loop through starter stages
for x in range(len(settings.starter_stages)):
    # if first stage then make string the stage name
    if len(starter_stages) == 0:
        starter_stages = f"{settings.starter_stages[x]}\n"
    # else concatenate the new stage name
    else:
        starter_stages = f"{starter_stages}{settings.starter_stages[x]}\n"

counterpick_stages = ""  # blank string
# loop through counterpick stages
for x in range(len(settings.counterpick_stages)):
    # if first stage then make string the stage name
    if len(counterpick_stages) == 0:
        counterpick_stages = f"{settings.counterpick_stages[x]}\n"
    # else concatenate the new stage name
    else:
        counterpick_stages = f"{counterpick_stages}{settings.counterpick_stages[x]}\n"


@bot.command()
async def veto(ctx, game, seriesLength, p2):
    """
    Starts a veto lobby with your opponent
    """
    if game == 'smash':
        embed = discord.Embed(description=f"{ctx.author.mention} vs {p2}"
                                          f"\nThe rulebook can be found [here](https://vaughanesports.org/rules)",
                              color=discord.Color(0xffff00))

        # game 1 embed line
        embed.add_field(name="`                         Game 1                            `",
                        value="**Winner:** TBD", inline=False)
        embed.add_field(name="Starter Stages", value=starter_stages, inline=True)
        embed.add_field(name="Counterpick Stages", value=counterpick_stages, inline=True)

        # game 2 embed line
        embed.add_field(name="`                         Game 2                            `",
                        value="**Winner:** TBD", inline=False)
        embed.add_field(name="Starter Stages", value=starter_stages, inline=True)
        embed.add_field(name="Counterpick Stages", value=counterpick_stages, inline=True)

        # game 3 embed line
        embed.add_field(name="`                         Game 3                            `",
                        value="**Winner:** TBD", inline=False)
        embed.add_field(name="Starter Stages", value=starter_stages, inline=True)
        embed.add_field(name="Counterpick Stages", value=counterpick_stages, inline=True)
        embed.set_footer(icon_url="https://vaughanesports.org/assets/Vaughan%20Esports%20Logo.png",
                         text=f"{settings.tourney_name} | DM Brandon for help or ping here.")

        await ctx.send(embed=embed)

bot.run(BOT_TOKEN)
