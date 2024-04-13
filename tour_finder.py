"""Tour finder."""

import re

from discord.ext import commands

from create_embed import create_embed
from error_message import error_message
from import_stuff import bot, cur, main_url


def tour_name_fix(tour: str) -> str:  # noqa: PLR0911
    """Tour name fixer."""
    # btr, river, bitusa, tol, other band, human touch, lucky town
    if tour == "btr":
        return "born to run"
    elif tour == "river":  # noqa: RET505
        return "the river tour"
    elif tour == "bitusa":
        return "born in the u.s.a. tour"
    elif re.search("(tunnel|tol)", tour, re.IGNORECASE):
        return "tunnel of love"
    elif re.search("usa", tour, re.IGNORECASE):
        return tour.replace("usa", "u.s.a.")
    elif re.search("(92|93)", tour, re.IGNORECASE):
        return "world tour 1992-93"
    elif re.search("(16|2016)", tour, re.IGNORECASE):
        return "the river tour '16"
    else:
        return tour


@bot.command(aliases=["tour"])
async def tour_stats(ctx: commands.Context, *, args: str = "") -> None:
    """Get stats for a specific tour."""
    # id, url, name, first_show_url, last_show_url, num_shows, num_songs

    if len(args) > 1:
        tour_name = tour_name_fix(args).replace("'", "''")
        stats = ""

        if cur.execute(
            """SELECT * FROM TOURS WHERE tour_name = %s""",
            (tour_name,),
        ).fetchall():
            stats = cur.execute(
                """SELECT * FROM TOURS WHERE tour_name = %s""",
                (tour_name,),
            ).fetchall()[0]
        elif cur.execute(
            """SELECT * FROM TOURS WHERE tour_name ILIKE %s""",
            (f"%{tour_name}%",),
        ).fetchall():
            stats = cur.execute(
                """SELECT * FROM TOURS WHERE tour_name ILIKE %s""",
                (f"%{tour_name}%",),
            ).fetchall()[0]

        if stats != "":
            first_show = cur.execute(
                """SELECT event_date FROM EVENTS WHERE tour LIKE
                %s AND event_url = %s AND event_url LIKE %s""",
                ("%" + stats[2].replace("'", "''") + "%", stats[3], "/gig:%"),
            ).fetchall()[0]
            last_show = cur.execute(
                """SELECT event_date FROM EVENTS WHERE tour LIKE
                %s AND event_url = %s AND event_url LIKE %s""",
                ("%" + stats[2].replace("'", "''") + "%", stats[4], "/gig:%"),
            ).fetchall()[0]

            embed = create_embed(
                f"Tour: {stats[2]}",
                f"[Tour Stats]({main_url}{stats[1]}) | [Tour Songs]({main_url}{stats[1].replace('shows', 'songs')})",  # noqa: E501
                ctx,
            )

            # first show, last show, num shows, num songs
            embed.add_field(name="Number of Shows:", value=f"{stats[5]}", inline=False)
            embed.add_field(
                name="First Show:",
                value=f"[{first_show[0]}]({main_url}{stats[3]!s})",
                inline=False,
            )
            embed.add_field(
                name="Last Show:",
                value=f"[{last_show[0]}]({main_url}{stats[4]!s})",
                inline=False,
            )
            embed.add_field(name="Number of Songs:", value=f"{stats[6]}", inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(error_message("tour"))
    else:
        await ctx.send(error_message("tour"))
