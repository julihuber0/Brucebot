from importStuff import *

@bot.command(aliases=['bootleg'])
async def bootlegFind(ctx, date=None):

  if dateChecker(date) and date is not None:
    event_name = cur.execute("SELECT event_date, event_venue, event_city, event_state, event_country, show FROM EVENTS WHERE event_date=%s", (date,)).fetchone()

    if event_name:
      location = ", ".join(list(filter(None, event_name[1:])))
      embed = createEmbed("Bootlegs For: " + date, location)
      URL = "https://www.springsteenlyrics.com/bootlegs.php?filter_date=%s&cmd=list&category=filter_date" % date
      embed.add_field(name="", value = "[SpringsteenLyrics](" + URL + ")")
      await ctx.send(embed=embed)
    else:
      await ctx.send(errorMessage("date"))
  else:
    await ctx.send(errorMessage("date"))