"""
create_embed
returns Discord embed
"""

from import_stuff import discord
import re

def create_embed(title, description, ctx):
	"""Returns a Discord Embed with the provided title and des."""
	embed = discord.Embed(title=title, description=description, color=0x6d3da4)
	embed.set_author(name=f"Requested by: {ctx.author.display_name}", icon_url=str(ctx.author.avatar.url))

	eDate = re.findall("\d{4}", title)

	embed.set_thumbnail(url=f"https://raw.githubusercontent.com/lilbud/lilbud.github.io/main/assets/img/graphics/bootleg-covers/features/bruce/{eDate[0]}.jpg")

	return embed
