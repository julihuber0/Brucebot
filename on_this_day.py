from importStuff import *

@bot.command(aliases=['otd', 'onthisday'])
async def on_this_day(ctx, *date):

  ndate = ""
  
  if not date:
    ndate = "-" + cDate.strftime("%m") + "-" + cDate.strftime("%d")
  else:
    if re.search("\d{2}-\d{2}", date[0]):
      ndate = "-" + date[0]

  if ndate:
    #id, date, event_url, name, location, tour
    otdLinks = cur.execute("""SELECT * FROM EVENTS WHERE event_date LIKE '%""" + ndate + "'").fetchall()
  
    embed = createEmbed("On This Day: " + ndate.strip("-"), "Number of Shows: " + str(len(otdLinks)))
    
    for i in otdLinks:
      embed.add_field(name=i[1][0:4], value="[" + i[3] + "](" + mainURL + i[2] + ")")
  
    await ctx.send(embed=embed)
  else:
    await ctx.send(errorMessage("date"))