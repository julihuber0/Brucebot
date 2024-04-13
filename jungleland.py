"""jungleland gets information from Jungleland.dnsalias and Jungleland.it."""

import re

from discord.ext import commands

from create_embed import create_embed
from error_message import error_message
from import_stuff import bot, cur, date_in_db, location_name_get


@bot.command(aliases=["jl", "jungleland"])
async def jungleland_torrent(ctx: commands.Context, date: str = "") -> None:
    """Return link to Jungleland Torrents for Specified Date."""
    if date_in_db(date):
        location = cur.execute(
            """SELECT location_url, show FROM EVENTS WHERE event_date = %s""",
            (date,),
        ).fetchone()
        title = location_name_get(location[0], location[1])
        embed = create_embed(f"Jungleland Results For: {date}", title, ctx)

        d = date.split("-")

        year = d[0]
        month = re.sub("^0", "", d[1])
        day = re.sub("^0", "", d[-1])

        url = f"http://jungleland.dnsalias.com/torrents-browse-date.php?year={year}&month={month}&day={day}&incldead=1"

        embed.add_field(name="", value=f"[Jungleland]({url})", inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send(error_message("date"))


@bot.command(aliases=["artwork"])
async def jungleland_art(ctx: commands.Context, date: str = "") -> None:
    """Return list of artwork on Jungleland.it for specified date."""
    if date_in_db(date):
        links = cur.execute(
            """SELECT artwork_url FROM ARTWORK WHERE date = %s""",
            (date,),
        ).fetchall()

        if links:
            location = cur.execute(
                """SELECT location_url, show FROM EVENTS WHERE event_date = %s""",
                (date,),
            ).fetchone()
            title = location_name_get(location[0], location[1])
            embed = create_embed(
                f"Jungleland Artwork Results For: {date!s}",
                title,
                ctx,
            )

            for link in links:
                name = cur.execute(
                    """SELECT artwork_name FROM ARTWORK WHERE artwork_url = %s""",
                    (link[0],),
                ).fetchone()
                embed.add_field(
                    name="",
                    value=f"- [{name[0]}](http://www.jungleland.it/html/{link[0]})",
                    inline=False,
                )
        else:
            embed.add_field(name="", value=error_message("cover"), inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send(error_message("date"))
