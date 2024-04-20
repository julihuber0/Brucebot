"""Relation find."""

import re

from discord.ext import commands

from create_embed import create_embed
from error_message import error_message
from import_stuff import bot, cur, main_url


def relation_name_fix(name: str) -> str:
    """Fix relation names."""
    if re.search(" us ", name, re.IGNORECASE):
        return "gary u.s. bonds"

    return name


def get_relation_type(r_type: str) -> str:
    """Get type of relation to search for."""
    match r_type:
        case "p":
            return "person"
        case "b":
            return "band"
        case _:
            return r_type


@bot.command(aliases=["band", "b", "person", "p"])
async def relation_finder(ctx: commands.Context, *, args: str = "") -> None:
    """Get info on bands/people that have played with bruce."""
    r_type = ctx.invoked_with

    type_find = get_relation_type(r_type)

    name = relation_name_fix(args).lower().replace("'", "''")

    if len(name) > 0:
        res = cur.execute(
            """SELECT relation_name, relation_url, appearances, relation_type FROM
            RELATIONS WHERE LOWER(relation_name) LIKE %s AND appearances != '0'
            AND relation_type LIKE %s""",
            (f"%{name}%", type_find),
        )

        if cur.fetchone():
            cur.execute(
                """SELECT relation_name, relation_url, appearances, relation_type FROM
                RELATIONS WHERE LOWER(relation_name) LIKE %s AND appearances != '0'
                AND relation_type LIKE %s""",
                (f"%{name}%", type_find),
            )

            relation_find = cur.fetchone()
        else:
            cur.execute(
                """SELECT relation_name, relation_url, appearances, relation_type FROM
                RELATIONS WHERE LOWER(relation_name) LIKE %s
                AND appearances != '0' AND relation_type = %s""",
                (f"%{name}%", type_find),
            )

            relation_find = cur.fetchone()

        if relation_find:
            name = relation_find[0]
            url = relation_find[1]
            performances = relation_find[2]
            relation_type = relation_find[3]

            embed = create_embed(
                f"{name} ({relation_type.title()})",
                f"[Brucebase Page]({main_url}{url})",
                ctx,
            )

            if int(performances) > 0:
                cur.execute(
                    """SELECT MIN(event_url), MAX(event_url) FROM ON_STAGE
                    WHERE relation_url = %s AND event_url LIKE %s""",
                    (url, "/gig:%"),
                )

                first_last = cur.fetchone()

                cur.execute(
                    """SELECT event_date FROM EVENTS WHERE event_url = %s""",
                    (first_last[0],),
                )

                first_date = cur.fetchall()[0]

                cur.execute(
                    """SELECT event_date FROM EVENTS WHERE event_url = %s""",
                    (first_last[1],),
                )

                last_date = cur.fetchall()[0]

                embed.add_field(
                    name="Performances:",
                    value=f"{performances}",
                    inline=True,
                )
                embed.add_field(
                    name="First Performance:",
                    value=f"[{first_date[0]}]({main_url}{first_last[0]})",
                    inline=True,
                )
                embed.add_field(
                    name="Last Performance:",
                    value=f"[{last_date[0]}]({main_url}{first_last[1]})",
                    inline=True,
                )
            else:
                embed.add_field(name="Performances:", value="0", inline=True)

            await ctx.send(embed=embed)
        else:
            await ctx.send(error_message("relation"))
    else:
        await ctx.send(error_message("relation"))
