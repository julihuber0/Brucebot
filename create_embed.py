"""
create_embed
returns Discord embed
"""

from import_stuff import discord

def create_embed(title, description, ctx):
    """Returns a Discord Embed with the provided title and des."""
    embed = discord.Embed(title=title, description=description, color=0x6d3da4)
    embed.set_author(name=ctx.author.display_name, icon_url=str(ctx.author.avatar.url))

    return embed
