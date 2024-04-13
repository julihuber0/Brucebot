"""on_this_day
gets events based on inputted day
or the current day if none specified
"""

import datetime
import re

from create_embed import create_embed
from error_message import error_message
from import_stuff import bot, cur, current_date, location_name_get, main_url


@bot.command(aliases=["otd", "onthisday"])
async def on_this_day(ctx, *date):
    """Gets events based on specified month-day input
    or the current day if none specified
    """
    ndate = ""

    if not date:
        ndate = f"-{(current_date.strftime('%m'))}-{current_date.strftime('%d')}"
    elif re.search(r"\d{2}-\d{2}", date[0]):
        ndate = f"-{date[0]!s}"

    if ndate:
        otd_links = cur.execute(
            f"""SELECT event_url, location_url, show, event_date FROM EVENTS WHERE event_date LIKE '%{ndate}' ORDER BY event_id ASC""",
        ).fetchall()

        embed = create_embed(
            f"On This Day: {datetime.datetime.strptime(ndate.strip('-'), '%m-%d').strftime('%B %d')}",
            f"Number of Shows: {len(otd_links)!s}",
            ctx,
        )

        for i in otd_links:
            location = location_name_get(i[1], i[2])

            embed.add_field(
                name=f"{i[3][0:4]}:",
                value=f"[{location}]({main_url}{i[0]})",
                inline=False,
            )

        await ctx.send(embed=embed)
    else:
        await ctx.send(error_message("date"))
