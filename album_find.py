"""Album finder."""

from discord.ext import commands

from create_embed import create_embed
from error_message import error_message
from import_stuff import albums, bot, cur, main_url


def album_name_fix(album: str) -> str:
    """Fix incorrect album names."""
    album_name = ""

    # album name: [list of shorthand/abbreviations]
    for key, value in albums.items():
        for v in value:
            if v.lower() == album.lower():
                album_name = key

    if album_name:
        return album_name

    return album


def check_database_for_album(album: str) -> bool:
    """Search database for album."""
    check = cur.execute(
        """SELECT EXISTS(SELECT 1 FROM ALBUMS WHERE LOWER(album_name) = %s)""",
        (album),
    ).fetchone()

    if check:
        return True

    return False


@bot.command(aliases=["album", "a"])
async def album_finder(ctx: commands.Context, *, args: str = "") -> None:
    """Get info on album."""
    songs = []
    note = ""
    input_fixed = album_name_fix(args.replace("'", "''"))

    if check_database_for_album(input_fixed) and input_fixed.lower() != "tracks":
        info = cur.execute(
            """SELECT album_name, album_year, song_url FROM ALBUMS WHERE
            LOWER(album_name) = %s ORDER BY song_num ASC""",
            (input_fixed.lower()),
        ).fetchall()
        embed = create_embed(info[0][0], f"Year: {info[0][1]}", ctx)

        plays = cur.execute(
            """select song_name, num_plays FROM SONGS WHERE song_url IN
            (SELECT song_url FROM ALBUMS WHERE album_name LIKE
            %s) AND num_plays != ''
            ORDER BY CAST(num_plays as integer) ASC""",
            (info[0][0]),
        ).fetchall()
        premiere = cur.execute(
            """select song_name, first_played FROM SONGS WHERE song_url
            IN (SELECT song_url FROM ALBUMS WHERE album_name LIKE
            %s) AND first_played != ''
            ORDER BY first_played ASC""",
            (info[0][0]),
        ).fetchall()

        for s in info:
            find_song = cur.execute(
                """SELECT song_name, num_plays FROM SONGS WHERE song_url LIKE %s""",
                (s[2]),
            ).fetchone()

            if find_song[1] == "":
                songs.append(f"**{find_song[0]}**")
                note = " (Note: Not All Songs Played Live Yet)"
            else:
                songs.append(find_song[0])

        embed.add_field(
            name="Songs (Bold = Not Played):",
            value=f"{', '.join(songs)}",
            inline=False,
        )

        embed.add_field(
            name="Most/Least Played:",
            value=f"{plays[-1][0]} ({plays[-1][1]})\n{plays[0][0]} ({plays[0][1]})",
            inline=False,
        )

        first_date = cur.execute(
            """SELECT event_date FROM EVENTS WHERE event_url LIKE %s""",
            (premiere[0][1]),
        ).fetchone()
        last_date = cur.execute(
            """SELECT event_date FROM EVENTS WHERE event_url LIKE %s""",
            (premiere[-1][1]),
        ).fetchone()

        embed.add_field(
            name=f"First/Last Premiered{note}:",
            value=f"{premiere[0][0]} ([{first_date[0]}]({main_url}{premiere[0][1]}))\n{premiere[-1][0]} ([{last_date[0]}]({main_url}{premiere[-1][1]}))",  # noqa: E501
            inline=False,
        )

        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{error_message('album')}, No results for: {input_fixed}")
