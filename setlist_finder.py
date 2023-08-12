"""
setlist_finder
gets setlist based on inputted date
"""

from import_stuff import date_checker, cur, bot, main_url, location_name_get
from create_embed import create_embed
from error_message import error_message
import re

@bot.command(aliases=['sl', 'setlist', 'show'])
async def setlist_finder(ctx, date=None):
	"""Gets setlist based on inputted date"""

	if date is None:
		d = cur.execute("""SELECT event_url FROM EVENTS WHERE setlist != '' ORDER BY event_id DESC LIMIT 1""").fetchone()[0]
		date = re.findall("\d{4}-\d{2}-\d{2}", d)[0]

	if date_checker(date):
		embed = create_embed(f"Brucebase Results for: {date}", "", ctx)

		if cur.execute(f"""SELECT * FROM EVENTS WHERE event_url LIKE '%{str(date)}%'""").fetchall():
			for r in cur.execute(f"""SELECT * FROM EVENTS WHERE event_url LIKE '%{str(date)}%'""").fetchall():
				# id, event_url, location_url, show, tour, setlist
				location = ""
				# location = ", ".join(list(filter(None, r[4:8])))
				location = location_name_get(r[2])
				if r[3] != "":
					location += f" ({r[3]})"

				event_date = re.findall("\d{4}-\d{2}-\d{2}", r[1])
				embed.add_field(name="", value=f"[{event_date[0]}]({main_url}{r[1]})\n*{location}*", inline=False)
				embed.set_footer(text=r[4])

				#id, event_url, song_url, song_name, set_type, song_in_set, song_num, segue
				for s in cur.execute(f"""SELECT * FROM (SELECT DISTINCT ON (set_type) * FROM SETLISTS WHERE event_url LIKE '%{r[1]}%' ORDER BY set_type, setlist_song_id ASC) p ORDER BY setlist_song_id ASC""").fetchall():
					set_l = []

					for t in cur.execute(f"""SELECT song_name, song_url, segue FROM SETLISTS WHERE event_url LIKE '%{r[1]}%' AND set_type LIKE '%{s[4].replace("'", "''")}%' ORDER BY song_num ASC""").fetchall():
						premiere = cur.execute(f"""SELECT first_played FROM SONGS WHERE song_url LIKE '%{t[1]}%'""").fetchone()
						bustout = cur.execute(f"""SELECT MIN(event_url) FROM EVENTS WHERE setlist LIKE '%{t[0].replace("'", "''")}%' AND tour = '{r[4].replace("'", "''")}'""").fetchone()

						#check setlist table for song url and tour, order by id ascending, if date equals r[1] (date) and tour = r[9], then bustout
						bustout_date = re.findall("\d{4}-\d{2}-\d{2}", bustout[0])

						if premiere[0] == event_date[0] and s[4] not in ['Soundcheck', 'Rehearsal']:
							if t[2]:
								set_l.append(f"{t[0]} **[1]** > ")
							else:
								set_l.append(f"{t[0]} **[1]**")
						elif bustout_date[0] == event_date[0] and s[4] not in ['Soundcheck', 'Rehearsal']:
							if t[2]:
								set_l.append(f"{t[0]} **[2]** > ")
							else:
								set_l.append(f"{t[0]} **[2]**")
						else:
							if t[2]:
								set_l.append(f"{t[0]} >")
							else:
								set_l.append(f"{t[0]}")

					setlist = (", ".join(set_l)).replace(">,", ">")

					if setlist:
						embed.add_field(name=f"{s[4]}:", value=setlist, inline=False)
					else:
						embed.add_field(name=f"{s[4]}:", value="No Set Details Known", inline=False)

			#embed.add_field(name="", value="**[1]** - First Known Performance")
			embed.add_field(name="", value="**[1]** - First Known Performance\n**[2]** - Tour Debut")
		else:
			embed.add_field(name="", value="ERROR: Show Not Found", inline=False)

		await ctx.send(embed=embed)
	else:
		await ctx.send(error_message("date"))
