"""
create_embed
returns Discord embed
"""

from import_stuff import discord

def create_embed(title, description):
    """Returns a Discord Embed with the provided title and des."""

    return discord.Embed(title=title, description=description, color=0x6d3da4)
