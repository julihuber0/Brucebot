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

        for s in cur.execute("""SELECT DISTINCT set_type, setlist_song_id FROM SETLISTS WHERE event_url = %s ORDER BY setlist_song_id ASC""", (r[2],)).fetchall():
          setL = []
          key = ""
          temp = cur.execute("""SELECT song_name, song_url FROM SETLISTS WHERE event_url = %s AND set_type = %s ORDER BY song_num ASC""", (r[2], s[0],)).fetchall()
      
          for t in temp:
            #song = t[0].replace("'", "''")
            song = "'%" + t[0] + "%'"
            premiere = cur.execute("""SELECT * FROM EVENTS WHERE setlist LIKE '%""" + date + "%' ORDER BY event_id ASC").fetchone() #ORDER BY event_id ASC
            bustout = cur.execute("""SELECT * FROM EVENTS WHERE tour = %s AND tour != '' AND setlist LIKE %s ORDER BY event_id ASC""", (r[5],song,)).fetchone()

            if premiere:
              if premiere[2] == r[2]:
                setL.append(t[0] + " **[" + str(2) + "]**")
            elif bustout:
              if bustout[2] == r[2]:
                setL.append(t[0] + " **[" + str(1) + "]**") 
              else:
                setL.append(t[0])
            else:
              setL.append(t[0])
  
          setlist = ", ".join(setL)
    
          if setlist:
            embed.add_field(name=s[0] + ":", value=setlist[:5990], inline=False)
          else:
            embed.add_field(name=s[0] + ":", value="No Set Details Known", inline=False)
  
      embed.add_field(name="", value="**[1]** - Tour Debut\n**[2]** - First Known Performance")
    else:
      embed.add_field(name="", value="ERROR: Show Not Found", inline=False)
    
    await ctx.send(embed=embed)
  else:
    await ctx.send(errorMessage("date"))