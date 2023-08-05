from importStuff import *

@bot.command(aliases=['song'])
async def sFind(ctx, *song):
  #0,  1,    2,     3,     4,     5
  #id, url, name, first, last, num_plays
  song_name = " ".join(song).replace("'", "''")
  s = cur.execute("""SELECT * FROM SONGS WHERE song_name LIKE '%""" + song_name + "%'").fetchone()

  if s:
    f = cur.execute("""SELECT event_url FROM EVENTS WHERE event_date=?""", (s[3],)).fetchone()
    l = cur.execute("""SELECT event_url FROM EVENTS WHERE event_date=?""", (s[4],)).fetchone()

    opener = cur.execute("""SELECT COUNT(song_url) FROM SETLISTS WHERE song_url=? AND song_num=1""", (s[1],)).fetchone()
    closer = cur.execute("""SELECT COUNT(event_url) FROM EVENTS WHERE setlist LIKE '%""" + song_name + "'").fetchone()

    embed = createEmbed(s[2], "[Brucebase Song Page](" + mainURL + s[1] + ")")

    embed.add_field(name="Performances:", value=s[5], inline=True)
    embed.add_field(name="First Played:", value="[" + s[3] + "](" + mainURL + f[0] + ")", inline=True)
    embed.add_field(name="Last Played:", value="[" + s[4] + "](" + mainURL + l[0] + ")", inline=True)
    embed.add_field(name="Show Opener:", value=opener[0], inline=True)
    embed.add_field(name="Show Closer:", value=closer[0], inline=True)
    await ctx.send(embed=embed)
  else:
    await ctx.send("\nNo Results Found For: " + " ".join(song))