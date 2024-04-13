"""create_embed returns Discord embed."""

from discord.ext import commands

from import_stuff import discord


def create_embed(title: str, description: str, ctx: commands.Context) -> discord.Embed:
    """Return a Discord Embed with the provided title and des."""
    embed = discord.Embed(title=title, description=description, color=0x6D3DA4)
    embed.set_author(
        name=f"Requested by: {ctx.author.display_name}",
        icon_url=str(ctx.author.avatar.url),
    )

    return embed
