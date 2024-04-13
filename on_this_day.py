"""on_this_day gets events based on inputted day or the current day if none specified."""  # noqa: E501

import datetime
import re

from discord.ext import commands

from create_embed import create_embed
from error_message import error_message
from import_stuff import bot, cur, current_date, location_name_get, main_url


@bot.command(aliases=["otd", "onthisday"])
async def on_this_day(ctx: commands.Context, *, args: str = "") -> None:
    """Get events based on specified month-day input or the current day if none."""
    ndate = ""

    if not args:
        ndate = f"-{(current_date.strftime('%m'))}-{current_date.strftime('%d')}"
    elif re.search(r"\d{2}-\d{2}$", args):
        ndate = f"-{args}"

    if ndate:
        otd_links = cur.execute(
            """SELECT event_url, location_url, show, event_date FROM EVENTS WHERE
                event_date LIKE %s ORDER BY event_id ASC""",
            (f"%{ndate}",),
        ).fetchall()

        embed = create_embed(
            f"On This Day: {datetime.datetime.strptime(ndate.strip('-'), '%m-%d').strftime('%B %d')}",  # noqa: DTZ007, E501
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
