"""
jungleland
gets information from Jungleland.dnsalias and Jungleland.it
"""

import re
from import_stuff import bot, date_checker, cur, location_name_get
from error_message import error_message
from create_embed import create_embed


@bot.command(aliases=['jl', 'jungleland'])
async def jungleland_torrent(ctx, date=None):
	"""Returns link to Jungleland Torrents for Specified Date"""

	if date_checker(date) and date is not None:
		location = cur.execute(f"""SELECT location_url, show FROM EVENTS WHERE event_url LIKE '%{str(date)}%'""").fetchone()

		title = location_name_get(location[0])

		if location[1] != "":
			title += f" ({location[1]})"

		# title = ", ".join(filter(None, location))
		embed = create_embed(f"Jungleland Results For: {date}", title, ctx)

		d = date.split("-")

		url = f"http://jungleland.dnsalias.com/torrents-browse-date.php?year={d[0]}&month={re.sub('^0', '', d[1])}&day={re.sub('^0', '', d[-1])}&incldead=1"

		embed.add_field(name="", value=f"[Jungleland]({url})", inline=False)

		await ctx.send(embed=embed)
	else:
		await ctx.send(error_message("date"))


@bot.command(aliases=['artwork'])
async def jungleland_art(ctx, date=None):
	"""Returns list of artwork on Jungleland.it for specified date"""
	if date_checker(date) and date is not None:
		location = cur.execute(f"""SELECT location_url, show FROM EVENTS WHERE event_url LIKE '%{str(date)}%'""").fetchone()

		title = location_name_get(location[0])

		if location[1] != "":
			title += f" ({location[1]})"

		# title = ", ".join(filter(None, location))
		links = cur.execute(f"""SELECT artwork_url FROM ARTWORK WHERE date LIKE '%{str(date)}%'""").fetchall()
		embed = create_embed(f"Jungleland Artwork Results For: {str(date)}", title, ctx)

		if links:
			for link in links:
				name = cur.execute(f"""SELECT artwork_name FROM ARTWORK WHERE artwork_url LIKE '%{link[0]}%'""").fetchone()
				embed.add_field(name="", value=f"- [{name[0]}](http://www.jungleland.it/html/{link[0]})", inline=False)
		else:
			embed.add_field(name="", value=error_message(
				"cover"), inline=False)

		await ctx.send(embed=embed)
	else:
		await ctx.send(error_message("date"))
