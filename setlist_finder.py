"""setlist_finder gets setlist based on inputted date."""

from discord.ext import commands

from create_embed import create_embed
from error_message import error_message
from import_stuff import bot, cur, date_in_db, location_name_get, main_url


@bot.command(aliases=["sl", "setlist", "show"])
async def setlist_finder(ctx: commands.Context, date: str = "") -> None:  # noqa: C901, PLR0912
    """Get setlist based on input date."""
    if date == "":
        date = cur.execute(
            """SELECT event_date FROM EVENTS WHERE setlist != ''
            ORDER BY event_id DESC LIMIT 1""",
        ).fetchone()[0]

    if date_in_db(date):
        embed = create_embed(f"Brucebase Results For: {date}", "", ctx)
        get_events = cur.execute(
            """SELECT * FROM EVENTS WHERE event_date = %s""",
            (date,),
        ).fetchall()
        invalid_sets = []

        for i in cur.execute(
            """SELECT set_type FROM (SELECT DISTINCT ON (set_type) * FROM SETLISTS WHERE
            set_type SIMILAR TO '%(Soundcheck|Rehearsal|Pre-)%') p""",
        ).fetchall():
            invalid_sets.append(i[0])  # noqa: PERF401

        if get_events:
            for r in get_events:
                tags = []

                if r[7]:
                    tags.append("Bootleg")

                if r[8]:
                    tags.append("Official Release")

                if not r[7] and not r[8]:
                    tags.append("Uncirculating")

                location = location_name_get(r[3], r[4])
                releases = f"**Releases:** {', '.join(tags)}"

                embed.add_field(
                    name="",
                    value=f"[{r[1]} - {location}]({main_url}{r[2]})\n{releases}",
                    inline=False,
                )
                embed.set_footer(text=r[5])

                has_setlist = cur.execute(
                    """SELECT EXISTS(SELECT 1 FROM SETLISTS WHERE event_url LIKE %s)""",
                    (r[2],),
                ).fetchone()

                if has_setlist[0] != 0:
                    location = setlist = indicator = ""

                    for s in cur.execute(
                        """SELECT set_type FROM (SELECT DISTINCT ON (set_type) * FROM
                        SETLISTS WHERE event_url LIKE %s) p ORDER BY
                        setlist_song_id ASC""",
                        (r[2],),
                    ).fetchall():
                        set_l = []

                        set_songs = cur.execute(
                            """SELECT song_name, song_url, segue FROM SETLISTS
                            WHERE event_url LIKE %s AND set_type =
                            %s ORDER BY setlist_song_id ASC""",
                            (r[2], s[0].replace("'", "''")),
                        ).fetchall()

                        for song in set_songs:
                            indicator = note = segue = ""
                            premiere = cur.execute(
                                """SELECT EXISTS(SELECT 1 FROM SONGS WHERE song_url
                                LIKE %s AND first_played LIKE %s)""",
                                (song[1], r[2]),
                            ).fetchone()
                            # bustout = cur.execute(
                            #     """SELECT MIN(event_url) FROM EVENTS WHERE setlist
                            #     LIKE %s AND tour LIKE %s""",
                            #     (
                            #         f"%{song[0].replace("'", "''")}%",
                            #         r[5].replace("'", "''"),
                            #     ),
                            # ).fetchone()

                            """indicator is [1] or [2]"""
                            if s[0] not in invalid_sets:  # noqa: SIM102
                                if premiere[0] != 0:
                                    indicator = " **[1]**"

                                # if bustout[0] == r[2]:
                                #     indicator = " **[2]**"

                            if song[2]:
                                segue = " >"

                            set_l.append(f"{song[0]}{indicator}{segue}")

                        setlist = ", ".join(set_l).replace(">,", ">")

                        if not r[7] and not r[8]:
                            note = "(Setlist May Be Incomplete)"

                        embed.add_field(
                            name=f"{s[0]} {note}:",
                            value=setlist,
                            inline=False,
                        )
                else:  # end "if has_setlist"
                    embed.add_field(
                        name="",
                        value=error_message("no-setlist"),
                        inline=False,
                    )

            embed.add_field(
                name="",
                value="**[1]** - First Known Performance\n**[2]** - Tour Debut",
            )
        else:  # end "if get_events"
            embed.add_field(name="", value=error_message("show"), inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{error_message('date')} - {date}")
