"""
Bootleg Finder
Returns a link to SpringsteenLyrics Bootleg Page for the specified Date
"""

from import_stuff import bot, cur, date_checker
from create_embed import create_embed
from error_message import error_message

@bot.command(aliases=['bootleg'])
async def bootleg_find(ctx, date=None):
    """Returns a link to SpringsteenLyrics Bootleg Page for the specified Date"""

    if date_checker(date) and date is not None:
        event_name = cur.execute(f"""SELECT event_venue, event_city, event_state, event_country, show FROM EVENTS WHERE event_date LIKE '{str(date)}'""").fetchone()

        if event_name:
            location = ", ".join(list(filter(None, event_name[0:])))
            embed = create_embed(f"Bootlegs For: {date}", location)
            embed.set_author(name=ctx.author.display_name, icon_url=str(ctx.message.author.avatar_url))
            url = f"https://www.springsteenlyrics.com/bootlegs.php?filter_date={date}&cmd=list&category=filter_date"
            embed.add_field(name="", value=f"[SpringsteenLyrics]({url})")
            await ctx.send(embed=embed)
        else:
            await ctx.send(error_message("date"))
    else:
        await ctx.send(error_message("date"))
