import discord
from settings import *


async def timeout_error_message(original_message):
    error_embed = discord.Embed(color=0xff0000)
    error_embed.add_field(name="Timeout Error", value="The match timer has expired.", inline=False)
    error_embed.set_footer(icon_url=footer_icon, text=f"{tourney_name} | {footer_note}")
    await original_message.edit(embed=error_embed)
