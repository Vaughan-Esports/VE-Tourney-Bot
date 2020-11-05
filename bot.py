import discord
import os
from discord.ext import commands


bot = discord.ext.commands.Bot('!')
BOT_TOKEN = os.getenv('BOT_TOKEN')


@bot.command()
async def veto(ctx, arg, p2):
    if arg == 'smash':
        p1 = ctx.author.mention

        embed = discord.Embed(title="Veto", colour=discord.Colour(0xf8e71c),
                              description="You can find our rulebook [here](https://vaughanesports.org/rules).")
        embed.set_author(name="")
        embed.set_footer(text="Vaughan Esports October 2020 Smash Monthly")
        embed.add_field(name="Players", value=p1, inline=True)
        embed.add_field(name="‎", value=p2, inline=True)
        await ctx.send(embed=embed)


bot.run(BOT_TOKEN)
