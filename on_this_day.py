from importStuff import bot
from create_embed import create_embed

@bot.command(aliases=['otd', 'onthisday'])
async def on_this_day(ctx, *date):

  ndate = ""
  
  if not date:
    month = cDate.strftime("%m")
    day = cDate.strftime("%d")
    ndate = f"-{(cDate.strftime('%m'))}-{cDate.strftime('%d')}"
  else:
    if re.search("\d{2}-\d{2}", date[0]):
      ndate = f"-{str(date[0])}"

  if ndate:
    otdLinks = cur.execute(f"""SELECT event_date, event_url, event_venue, event_city, event_state, event_country, show FROM EVENTS WHERE event_date LIKE '%{nDate}'""").fetchall()
  
    embed = createEmbed(f"On This Day: {ndate.strip('-')}", f"Number of Shows: {str(len(otdLinks))}")
    location = ", ".join(list(filter(None, otdLinks[2:])))

    for i in otdLinks:
      embed.add_field(name=i[0][0:4], value=f"[{location}]({mainURL}{i[1]})")
  
    await ctx.send(embed=embed)
  else:
    await ctx.send(errorMessage("date"))