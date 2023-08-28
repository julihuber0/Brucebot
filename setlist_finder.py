"""
setlist_finder
gets setlist based on inputted date
"""

from import_stuff import date_checker, cur, bot, main_url
from create_embed import create_embed
from error_message import error_message


@bot.command(aliases=['sl', 'setlist', 'show'])
async def setlist_finder(ctx, date=None):
	"""Gets setlist based on inputted date"""

	if date is None:
		date = cur.execute("""SELECT event_date FROM EVENTS WHERE setlist != '' ORDER BY event_id DESC LIMIT 1""").fetchone()[0]

	if date_checker(date):
		embed = create_embed(f"Brucebase Results for: {date}", "", ctx)

		if cur.execute(f"""SELECT * FROM EVENTS WHERE event_date LIKE '%{str(date)}%'""").fetchall():
			for r in cur.execute(f"""SELECT * FROM EVENTS WHERE event_date LIKE '%{str(date)}%'""").fetchall():
				# id, date, event_url, location_url, venue, city, state, country, show, tour, setlist
				location = ""
				location = ", ".join(list(filter(None, r[4:8])))
				if r[8] != "":
					location += f" ({r[8]})"

				embed.add_field(name="", value=f"[{r[1]}]({main_url}{r[2]})\n*{location}*", inline=False)
				embed.set_footer(text=r[9])

				for s in cur.execute(f"""SELECT * FROM (SELECT DISTINCT ON (set_type) * FROM SETLISTS WHERE event_url LIKE '%{r[2]}%' ORDER BY set_type, setlist_song_id ASC) p ORDER BY setlist_song_id ASC""").fetchall():
					set_l = []

					for t in cur.execute(f"""SELECT song_name, song_url FROM SETLISTS WHERE event_url LIKE '%{r[2]}%' AND set_type LIKE '%{s[5].replace("'", "''")}%' ORDER BY song_num ASC""").fetchall():
						premiere = cur.execute(f"""SELECT first_played FROM SONGS WHERE song_url LIKE '%{t[1]}%'""").fetchone()
						bustout = cur.execute(f"""SELECT event_date FROM EVENTS WHERE tour LIKE '{r[9].replace("'", "''")}' AND setlist LIKE '%{t[0]}%' AND event_date LIKE '{r[1]}' ORDER BY event_id LIMIT 1""").fetchone()

						#check setlist table for song url and tour, order by id ascending, if date equals r[1] (date) and tour = r[9], then bustout

						if premiere and s[5] not in ['Soundcheck', 'Rehearsal']:
							if premiere[0] == r[1]:
								set_l.append(f"{t[0]} **[1]**")
							else:
								set_l.append(t[0])
						elif bustout and s[5] not in ['Soundcheck', 'Rehearsal']:
							set_l.append(f"{t[0]} **[2]**")
						else:
							set_l.append(t[0])

					setlist = ", ".join(set_l)

					if setlist:
						embed.add_field(name=f"{s[5]}:", value=setlist, inline=False)
					else:
						embed.add_field(name=f"{s[5]}:", value="No Set Details Known", inline=False)

			embed.add_field(name="", value="**[1]** - First Known Performance\n**[2]** - Tour Debut")
		else:
			embed.add_field(name="", value="ERROR: Show Not Found", inline=False)

		await ctx.send(embed=embed)
	else:
		await ctx.send(error_message("date"))
