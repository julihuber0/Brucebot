from importStuff import *

@bot.command(aliases=['sl', 'setlist', 'show'])
async def setlistFinder(ctx, date):

  if dateChecker(date):
    embed = createEmbed("Brucebase Results for: " + date, "")

    if cur.execute("""SELECT * FROM EVENTS WHERE event_date LIKE '%""" + date + "%'").fetchall():
      for r in cur.execute("""SELECT * FROM EVENTS WHERE event_date = %s""", (date,)).fetchall():
        #id, date, event_url, name, location, tour

        embed.add_field(name="", value="[" + r[1] + "](" + mainURL + r[2] + ")\n*" + r[3] + "*", inline=False)
        embed.set_footer(text=r[5])

        #SELECT DISTINCT ON (set_type) * FROM SETLISTS WHERE event_url = %s ORDER BY setlist_song_id ASC

        for s in cur.execute("""SELECT * FROM (SELECT DISTINCT ON (set_type) * FROM SETLISTS WHERE event_url=%s ORDER BY set_type, setlist_song_id ASC) p ORDER BY setlist_song_id ASC""", (r[2],)).fetchall():
          setL = []
          key = ""
          temp = cur.execute("""SELECT song_name, song_url FROM SETLISTS WHERE event_url = %s AND set_type = %s ORDER BY song_num ASC""", (r[2], s[5],)).fetchall()
      
          for t in temp:
            #setL = []
            premiere = bustout = ""
            #song = t[0].replace("'", "''")
            date = "'%" + date + "%'"
            song = "'%" + t[0].replace("'", "''") + "%'"
            premiere = cur.execute("""SELECT event_url FROM EVENTS WHERE setlist LIKE %s ORDER BY event_id ASC""", (song,)).fetchone() #ORDER BY event_id ASC
            bustout = cur.execute("""SELECT event_url FROM EVENTS WHERE tour = %s AND tour != '' AND setlist LIKE %s ORDER BY event_id ASC""", (r[5], song,)).fetchone()

            if premiere:
              if premiere[0] == r[2]:
                setL.append(t[0] + " **[2]**")
              else:
                setL.append("p: " + premiere[0][0:10])
            elif bustout:
              if bustout[0] == r[2]:
                setL.append(t[0] + " **[1]**")
              else:
                setL.append("b:" + bustout[0][0:10])
            else:
              setL.append(t[0])
            #setL.append(premiere[0], bustout[0])
  
          setlist = ", ".join(setL)
    
          if setlist:
            embed.add_field(name=s[5] + ":", value=setlist, inline=False)
          else:
            embed.add_field(name=s[5] + ":", value="No Set Details Known", inline=False)
  
      embed.add_field(name="", value="**[1]** - Tour Debut\n**[2]** - First Known Performance")
    else:
      embed.add_field(name="", value="ERROR: Show Not Found", inline=False)
    
    await ctx.send(embed=embed)
  else:
    await ctx.send(errorMessage("date"))