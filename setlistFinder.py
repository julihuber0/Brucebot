from importStuff import *

@bot.command(aliases=['sl', 'setlist', 'show'])
async def setlistFinder(ctx, date):

  if dateChecker(date):
    embed = createEmbed("Brucebase Results for: " + date, "")
    
    if cur.execute("""SELECT * FROM EVENTS WHERE event_date='""" + date + "'").fetchall():
      for r in cur.execute("""SELECT * FROM EVENTS WHERE event_date='""" + date + "'").fetchall():
        #id, date, event_url, name, location, tour

        embed.add_field(name="", value="[" + r[1] + "](" + mainURL + r[2] + ")\n*" + r[3] + "*", inline=False)
        embed.set_footer(text=r[5])

        for s in cur.execute("""SELECT DISTINCT(set_type) FROM SETLISTS WHERE event_url=""" + r[2] + """ ORDER BY setlist_song_id ASC""").fetchall():
          setL = []
          key = ""
          temp = cur.execute("""SELECT song_name, song_url FROM SETLISTS WHERE event_url=""" + r[2] + """ AND set_type=""" + s[0] + """ORDER BY song_num ASC""").fetchall()
      
          for t in temp:
            song = t[0].replace("'", "''")
            premiere = cur.execute("""SELECT * FROM EVENTS WHERE setlist LIKE '%""" + song + "%' ORDER BY event_id ASC").fetchone()
            bustout = cur.execute("""SELECT * FROM EVENTS WHERE tour=""" + r[5] + """AND tour != '' AND setlist LIKE '%""" + song + "%' ORDER BY event_id ASC", (r[5],)).fetchone()
  
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
            embed.add_field(name=s[0] + ":", value=setlist, inline=False)
          else:
            embed.add_field(name=s[0] + ":", value="No Set Details Known", inline=False)
  
      embed.add_field(name="", value="**[1]** - Tour Debut\n**[2]** - First Known Performance")
    else:
      embed.add_field(name="", value="ERROR: Show Not Found", inline=False)
    
    await ctx.send(embed=embed)
  else:
    await ctx.send(errorMessage("date"))