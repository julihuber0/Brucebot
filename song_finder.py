"""
song_finder
gets info in inputted song
"""

from import_stuff import bot, cur, main_url, song_name_fix
from create_embed import create_embed
from error_message import error_message

@bot.command(aliases=['song'])
async def song_finder(ctx, *song):
	"""Gets info on inputted song"""
	
	if len(" ".join(song)) > 1:
		song_name = song_name_fix(" ".join(song).replace("'", "''").replace("\"", "''"))
		#id, url, name, first_played, last_played, num_plays

		if cur.execute(f"""SELECT * FROM SONGS WHERE LOWER(song_name) LIKE '{song_name.lower()}'""").fetchone():
			s = cur.execute(f"""SELECT * FROM SONGS WHERE LOWER(song_name) LIKE '{song_name.lower()}'""").fetchone()
		else:
			s = cur.execute(f"""SELECT * FROM SONGS WHERE LOWER(song_name) LIKE '%{song_name.lower()}%'""").fetchone()

		if s:
			f = cur.execute(f"""SELECT event_url FROM EVENTS WHERE event_date LIKE '{str(s[3])}'""").fetchone()
			l = cur.execute(f"""SELECT event_url FROM EVENTS WHERE event_date LIKE '{str(s[4])}'""").fetchone()

			opener = cur.execute(f"""SELECT COUNT(song_url) FROM SETLISTS WHERE song_url LIKE '%{s[1]}%' AND song_num=1 AND set_type NOT IN ('Soundcheck', 'Rehearsal')""").fetchone()
			closer = cur.execute(f"""SELECT COUNT(event_url) FROM EVENTS WHERE setlist LIKE '%, {s[2].replace("'", "''")}'""").fetchone()
			total = cur.execute("""SELECT COUNT(event_id) FROM EVENTS WHERE event_url LIKE '/gig:%'""").fetchone()
			frequency = f"{round((s[5] / total[0] * 100), 2)}%"

			embed = create_embed(s[2], f"[Brucebase Song Page]({main_url}{s[1]})", ctx)

			embed.add_field(name="", value=f"[Lyrics]({main_url}{s[1].replace('/song:', '/lyrics:')})", inline=False)
			embed.add_field(name="Performances:", value=s[5], inline=True)

			if s[5] > 0:
				embed.add_field(name="First Played:",value=f"[{s[3]}]({main_url}{f[0]})", inline=True)
				embed.add_field(name="Last Played:",value=f"[{s[4]}]({main_url}{l[0]})", inline=True)
				embed.add_field(name="Show Opener:", value=opener[0], inline=True)
				embed.add_field(name="Show Closer:", value=closer[0], inline=True)
				embed.add_field(name="Frequency:", value=frequency, inline=True)

			await ctx.send(embed=embed)
		else:
			await ctx.send(f"\nNo Results Found For: {' '.join(song)}")
	else:
		await ctx.send(error_message("song"))
