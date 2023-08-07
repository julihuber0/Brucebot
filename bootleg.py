from importStuff import *

@bot.command(aliases=['bootleg'])
async def bootlegFind(ctx, date=None):

  if dateChecker(date) and date is not None:
    event_name = cur.execute("SELECT event_name FROM EVENTS WHERE event_date=%s", (date,)).fetchone()

    if event_name:
      embed = createEmbed("Bootlegs For: " + date, event_name[0])
      URL = "https://www.springsteenlyrics.com/bootlegs.php?filter_date=%s&cmd=list&category=filter_date" % date
      embed.add_field(name="", value = "[SpringsteenLyrics](" + URL + ")")
      await ctx.send(embed=embed)
    else:
      await ctx.send(errorMessage("date"))
  else:
    await ctx.send(errorMessage("date"))