"""
Bootleg Finder
Returns a link to SpringsteenLyrics Bootleg Page for the specified Date
"""

from import_stuff import bot, cur, date_checker, location_name_get
from create_embed import create_embed
from error_message import error_message

@bot.command(aliases=['bootleg'])
async def bootleg_find(ctx, date=None):
	"""Returns a link to SpringsteenLyrics Bootleg Page for the specified Date"""

	if date_checker(date) and date is not None:
		event_name = cur.execute(f"""SELECT location_url, show FROM EVENTS WHERE event_date LIKE '{str(date)}'""").fetchone()
		
		if event_name:
			location = location_name_get(event_name[0], event_name[1])

			embed = create_embed(f"Bootlegs For: {date}", location, ctx)
			url = f"[SpringsteenLyrics](https://www.springsteenlyrics.com/bootlegs.php?filter_date={date}&cmd=list&category=filter_date)"
			
			embed.add_field(name="", value=url)
			await ctx.send(embed=embed)
		else:
			await ctx.send(error_message("event"))
	else:
		await ctx.send(error_message("date"))
