"""
on_this_day
gets events based on inputted day
or the current day if none specified
"""

import re
from import_stuff import bot, cur, main_url, cDate
from create_embed import create_embed
from error_message import error_message


@bot.command(aliases=['otd', 'onthisday'])
async def on_this_day(ctx, *date):
    """
    Gets events based on specified month-day input
    or the current day if none specified
    """

    ndate = ""

    if not date:
        ndate = f"-{(cDate.strftime('%m'))}-{cDate.strftime('%d')}"
    else:
        if re.search("\d{2}-\d{2}", date[0]):
            ndate = f"-{str(date[0])}"

    if ndate:
        otd_links = cur.execute(f"""SELECT event_date, event_url, event_venue, event_city, event_state, event_country, show FROM EVENTS WHERE event_date LIKE '%{ndate}'""").fetchall()

        embed = create_embed(f"On This Day: {ndate.strip('-')}", f"Number of Shows: {str(len(otd_links))}")
        location = ", ".join(list(filter(None, otd_links[2:7])))

        for i in otd_links:
            embed.add_field(name=i[0][0:4], value=f"[{location}]({main_url}{i[1]})")

        await ctx.send(embed=embed)
    else:
        await ctx.send(error_message("date"))
