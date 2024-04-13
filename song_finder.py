"""song_finder
gets info in inputted song
"""

import re

from discord.ext import commands
from fuzzywuzzy import process

from create_embed import create_embed
from error_message import error_message
from import_stuff import bot, cur, main_url


def song_name_fix(song: str) -> str:
    """Fixes some possible incorrect song inputs, and also expands abbreviations"""
    # if song is not None:
    #     if re.search(" usa", song, re.IGNORECASE):
    #         pattern = "usa"
    #         replace = "u.s.a."
    #     elif re.search("bitusa", song, re.IGNORECASE):
    #         pattern = "bitusa"
    #         replace = "born in the u.s.a."
    #     elif re.search("btr", song, re.IGNORECASE):
    #         pattern = "btr"
    #         replace = "born to run"
    #     elif re.search("rosie", song, re.IGNORECASE):
    #         pattern = "rosie"
    #         replace = "rosalita"

    #     if pattern and replace:
    #         return re.sub(pattern, replace, song, flags=re.IGNORECASE)

    #     return song

    if re.search("btr", song):
        return re.sub("btr", "born to run", song)
    elif re.search("rosie", song):  # noqa: RET505
        return re.sub("rosie", "rosalita", song)

    return song


@bot.command(aliases=["song"])
async def song_finder(ctx: commands.Context, *, args: str = "") -> None:
    """Get info on inputted song."""
    args = args.replace("’", "'").replace("‘", "'").replace("”", '"').replace("‟", '"')

    if len(args) > 1:
        song_name = song_name_fix(re.sub("['\"]", "''", args))
        # id, url, name, first_played_url, last_played_url, num_plays, opener, closer, frequency

        songs = cur.execute("""SELECT song_name FROM SONGS""").fetchall()

        result = process.extractOne(song_name, songs)[0]

        s = cur.execute(
            f"""SELECT * FROM SONGS WHERE song_name = '{result[0]}'""",
        ).fetchone()

        # if cur.execute(
        #     f"""SELECT * FROM SONGS WHERE LOWER(song_name) LIKE '{song_name.lower()}'"""
        # ).fetchone():
        #     s = cur.execute(
        #         f"""SELECT * FROM SONGS WHERE LOWER(song_name) LIKE '{song_name.lower()}'"""
        #     ).fetchone()
        # else:
        #     s = cur.execute(
        #         f"""SELECT * FROM SONGS WHERE LOWER(song_name) LIKE '%{song_name.lower()}%'"""
        #     ).fetchone()

        if s:
            f = cur.execute(
                f"""SELECT event_date FROM EVENTS WHERE event_url LIKE '{s[3]!s}'""",
            ).fetchone()
            l = cur.execute(
                f"""SELECT event_date FROM EVENTS WHERE event_url LIKE '{s[4]!s}'""",
            ).fetchone()

            embed = create_embed(s[2], f"[Brucebase Song Page]({main_url}{s[1]})", ctx)

            embed.add_field(
                name="",
                value=f"[Lyrics]({main_url}{s[1].replace('/song:', '/lyrics:')})",
                inline=False,
            )

            if s[5] != "" and int(s[5]) > 0:
                embed.add_field(name="Performances:", value=s[5], inline=True)
                embed.add_field(
                    name="First Played:",
                    value=f"[{f[0]}]({main_url}{s[3]})",
                    inline=True,
                )
                embed.add_field(
                    name="Last Played:",
                    value=f"[{l[0]}]({main_url}{s[4]})",
                    inline=True,
                )
                embed.add_field(name="Show Opener:", value=s[6], inline=True)
                embed.add_field(name="Show Closer:", value=s[7], inline=True)
                embed.add_field(name="Frequency:", value=f"{s[8]}%", inline=True)
            else:
                embed.add_field(name="Performances:", value="0", inline=True)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"\nNo Results Found For: {' '.join(song)}")
    else:
        await ctx.send(error_message("song"))
