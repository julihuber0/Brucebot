"""
Bootleg Finder
Returns a link to SpringsteenLyrics Bootleg Page for the specified Date
"""

from importStuff import bot, cur, dateChecker, createEmbed, errorMessage

@bot.command(aliases=['bootleg'])
async def bootleg_find(ctx, date=None):
    """Returns a link to SpringsteenLyrics Bootleg Page for the specified Date"""

    if dateChecker(date) and date is not None:
        event_name = cur.execute(f"""SELECT event_venue, event_city, event_state, event_country, show FROM EVENTS WHERE event_date=\"{date}\"""").fetchone()

        if event_name:
            location = ", ".join(list(filter(None, event_name[0:])))
            embed = createEmbed(f"Bootlegs For: \"{date}\"", location)
            url = f"https://www.springsteenlyrics.com/bootlegs.php?filter_date={date}&cmd=list&category=filter_date"
            embed.add_field(name="", value=f"[SpringsteenLyrics]({url})")
            await ctx.send(embed=embed)
        else:
            await ctx.send(errorMessage("date"))
    else:
        await ctx.send(errorMessage("date"))
