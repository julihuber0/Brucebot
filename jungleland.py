from importStuff import *

@bot.command(aliases=['jl', 'jungleland'])
async def junglelandTorrent(ctx, date):

  if dateChecker(date):
    title = cur.execute("""SELECT event_name FROM EVENTS WHERE event_date=%s""", (date,)).fetchone()
    embed = createEmbed("Jungleland Results For: " + date, title[0])
  
    d = date.split("-")
  
    URL = "http://jungleland.dnsalias.com/torrents-browse-date.php?year=" + d[0] + "&month=" + re.sub("^0", "", d[1]) + "&day=" + re.sub("^0", "", d[2]) + "&incldead=1"
  
    embed.add_field(name="", value="[Jungleland](" + URL + ")", inline=False)

    await ctx.send(embed=embed)
  else:
    await ctx.send(errorMessage("date"))

@bot.command(aliases=['artwork'])
async def junglelandArt(ctx, date):

  if dateChecker(date):
    title = cur.execute("""SELECT event_name FROM EVENTS WHERE event_date = %s""", (date,)).fetchone()
    
    links = cur.execute("""SELECT artwork_url FROM ARTWORK WHERE date = %s""", (date, )).fetchall()
    embed = createEmbed("Jungleland Artwork Results For: " + date, title[0])
  
    if links:
      for link in links:
        name = cur.execute("""SELECT artwork_name FROM ARTWORK WHERE artwork_url=%s""", (link[0], )).fetchone()
        embed.add_field(name="", value="- [" + name[0] + "](" + link[0] + ")", inline=False)
    else:
      embed.add_field(name="", value=errorMessage("cover"), inline=False)
  
    await ctx.send(embed=embed)
  else:
    await ctx.send(errorMessage("date"))