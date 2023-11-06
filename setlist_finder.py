"""
setlist_finder
gets setlist based on inputted date
"""

from import_stuff import dateinDB, cur, bot, main_url, location_name_get
from create_embed import create_embed
from error_message import error_message
import re

@bot.command(aliases=['sl', 'setlist', 'show'])
async def setlist_finder(ctx, date=None):
	"""Gets setlist based on input date"""

	if date is None:
		date = cur.execute("""SELECT event_date FROM EVENTS WHERE setlist != '' ORDER BY event_id DESC LIMIT 1""").fetchone()[0]

	if dateinDB(date):
		embed = create_embed(f"Brucebase Results For: {date}", "", ctx)
		get_events = cur.execute(f"""SELECT * FROM EVENTS WHERE event_date LIKE '{str(date)}'""").fetchall()
		invalid_sets = []
		
		for i in cur.execute(f"""SELECT set_type FROM (SELECT DISTINCT ON (set_type) * FROM SETLISTS WHERE set_type SIMILAR TO '%(Soundcheck|Rehearsal|Pre-)%') p""").fetchall():
			invalid_sets.append(i[0])

		if get_events:
			for r in get_events:
				tags = []
				# id, date, event_url, location_url, show, tour, setlist, bootleg, livedl

				if r[7]:
					tags.append('Bootleg')
				
				if r[8]:
					tags.append('Official Release')
				
				if not r[7] and not r[8]:
					tags.append("Uncirculating")

				location = location_name_get(r[3], r[4])
				releases = f"**Releases:** {', '.join(tags)}"

				embed.add_field(name="", value=f"[{r[1]} - {location}]({main_url}{r[2]})\n{releases}", inline=False)
				embed.set_footer(text=r[5])

				has_setlist = cur.execute(f"""SELECT EXISTS(SELECT 1 FROM SETLISTS WHERE event_url LIKE '{r[2]}')""").fetchone()

				if has_setlist[0] != 0:
					location = setlist = indicator = ""

					#id, event_url, song_url, song_name, set_type, song_in_set, song_num, segue
					for s in cur.execute(f"""SELECT set_type FROM (SELECT DISTINCT ON (set_type) * FROM SETLISTS WHERE event_url LIKE '{r[2]}') p ORDER BY setlist_song_id ASC""").fetchall():
						set_l = []
					
						set_songs = cur.execute(f"""SELECT song_name, song_url, segue FROM SETLISTS WHERE event_url LIKE '{r[2]}' AND set_type LIKE '%{s[0].replace("'", "''")}%' ORDER BY setlist_song_id ASC""").fetchall()

						for song in set_songs:
							indicator = note = segue = ""
							premiere = cur.execute(f"""SELECT EXISTS(SELECT 1 FROM SONGS WHERE song_url LIKE '{song[1]}' AND first_played LIKE '{r[2]}')""").fetchone()
							bustout = cur.execute(f"""SELECT MIN(event_url) FROM EVENTS WHERE setlist LIKE '%{s[0].replace("'", "''")}%' AND tour = '{r[5].replace("'", "''")}' AND event_url LIKE '{r[2]}'""").fetchone()

							# indicator is [1] or [2]
							if s[0] not in invalid_sets:
								if premiere[0] != 0:
									indicator = " **[1]**"
								if bustout[0] == r[2]:
									indicator = " **[2]**"
									
							if song[2]:
								segue = " >"

							set_l.append(f"{song[0]}{indicator}{segue}")

						setlist = ", ".join(set_l).replace(">,", ">")

						if not r[7] and not r[8]:
							note = "(Setlist May Be Incomplete)"

						embed.add_field(name=f"{s[0]} {note}:", value=setlist, inline=False)
				else: # end "if has_setlist"
					embed.add_field(name="", value=error_message("no-setlist"), inline=False)

			embed.add_field(name="", value="**[1]** - First Known Performance\n**[2]** - Tour Debut")
		else: # end "if get_events"
			embed.add_field(name="", value=error_message("show"), inline=False)

		await ctx.send(embed=embed)
	else:
		await ctx.send(f"{error_message('date')} - {date}")
