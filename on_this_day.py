"""
on_this_day
gets events based on inputted day
or the current day if none specified
"""

import re
from import_stuff import bot, cur, main_url, cDate, location_name_get
from create_embed import create_embed
from error_message import error_message


@bot.command(aliases=['otd', 'onthisday'])
async def on_this_day(ctx, *date):
	"""
	Gets events based on specified month-day input
	or the current day if none specified
	"""

	ndate = ""

	if not date:
		ndate = f"-{(cDate.strftime('%m'))}-{cDate.strftime('%d')}"
	else:
		if re.search("\d{2}-\d{2}", date[0]):
			ndate = f"-{str(date[0])}"

	if ndate:
		otd_links = cur.execute(f"""SELECT event_url, location_url, show, event_date FROM EVENTS WHERE event_date LIKE '%{ndate}' ORDER BY event_id ASC""").fetchall()

		embed = create_embed(f"On This Day: {ndate.strip('-')}", f"Number of Shows: {str(len(otd_links))}", ctx)

		for i in otd_links:		
			location = location_name_get(i[1])

			if i[2] != "":
				location += f" ({i[2]})"

			embed.add_field(name=f"{i[3][0:4]}:", value=f"[{location}]({main_url}{i[0]})")

		await ctx.send(embed=embed)
	else:
		await ctx.send(error_message("date"))
