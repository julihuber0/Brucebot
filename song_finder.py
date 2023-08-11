"""
song_finder
gets info in inputted song
"""

from import_stuff import bot, cur, main_url
from create_embed import create_embed
from error_message import error_message

@bot.command(aliases=['song'])
async def song_finder(ctx, *song):
    """Gets info on inputted song"""

    # 0,  1,    2,     3,     4,     5
    # id, url, name, first, last, num_plays

    if len(" ".join(song)) > 1:
        song_name = " ".join(song).replace("'", "''")

        s = cur.execute(f"""SELECT * FROM SONGS WHERE song_name ILIKE '%{song_name}%'""").fetchone()

        if s:
            f = cur.execute(f"""SELECT event_url FROM EVENTS WHERE event_date = {str(s[3])}""").fetchone()
            l = cur.execute(f"""SELECT event_url FROM EVENTS WHERE event_date = {str(s[4])}""").fetchone()

            opener = cur.execute(f"""SELECT COUNT(song_url) FROM SETLISTS WHERE song_url=\"{s[1]}\" AND song_num=1""").fetchone()
            closer = cur.execute(f"""SELECT COUNT(event_url) FROM EVENTS WHERE setlist LIKE '%{song_name}""").fetchone()

            embed = create_embed(s[2], f"[Brucebase Song Page]({main_url}{s[1]})")

            embed.add_field(name="Performances:", value=s[5], inline=True)
            embed.add_field(name="First Played:",value=f"[{s[3]}]({main_url}{f[0]})", inline=True)
            embed.add_field(name="Last Played:",value=f"[{s[4]}]({main_url}{l[0]})", inline=True)
            embed.add_field(name="Show Opener:", value=opener[0], inline=True)
            embed.add_field(name="Show Closer:", value=closer[0], inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"\nNo Results Found For: {' '.join(song)}")
    else:
        await ctx.send(error_message("song"))
