"""Bootleg Finder
Returns a link to SpringsteenLyrics Bootleg Page for the specified Date
"""

from create_embed import create_embed
from error_message import error_message
from import_stuff import bot, cur, date_in_db, location_name_get


@bot.command(aliases=["bootleg"])
async def bootleg_find(ctx, date=None):
    """Returns a link to SpringsteenLyrics Bootleg Page for the specified Date"""
    if date_in_db(date):
        event_name = cur.execute(
            f"""SELECT location_url, show FROM EVENTS WHERE event_date LIKE '{date!s}'""",
        ).fetchone()

        location = location_name_get(event_name[0], event_name[1])

        embed = create_embed(f"Bootlegs For: {date}", location, ctx)
        url = f"[SpringsteenLyrics](https://www.springsteenlyrics.com/bootlegs.php?filter_date={date}&cmd=list&category=filter_date)"

        embed.add_field(name="", value=url)
        await ctx.send(embed=embed)
    else:
        await ctx.send(error_message("date"))
