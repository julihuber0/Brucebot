"""Bot Info.

functions to:
- list commands
- list info
- show status
"""

from discord.ext import commands

from create_embed import create_embed
from import_stuff import bot

botcmds = {
    "setlist": {
        "name": "Setlist Finder:\t`!sl YYYY-MM-DD`  OR  `!setlist [YYYY-MM-DD]`",
        "value": "Returns the setlist of that show from Brucebase",
    },
    "cover": {
        "name": "Cover:\t`!cover YYYY-MM-DD`",
        "value": "Will get artwork from my website for that show",
    },
    "jungleland": {
        "name": "Jungleland:\t`!jl YYYY-MM-DD`",
        "value": "Returns link to Jungleland torrents with specified date",
    },
    "otd": {
        "name": "On This Day:\t`!otd`  OR  `!otd MM-DD`",
        "value": "Returns a list of shows that happened on this day. Can leave blank for the current day, or enter a specific Month and Day",  # noqa: E501
    },
    "artwork": {
        "name": "Artwork:\t`!artwork YYYY-MM-DD`",
        "value": "Returns list of artwork from Jungleland.it",
    },
    "bootleg": {
        "name": "Bootleg:\t`!bootleg YYYY-MM-DD`",
        "value": "Returns link to SpringsteenLyrics with list of Bootlegs for that date",  # noqa: E501
    },
    "info": {"name": "Info:\t`!botinfo`", "value": "Returns Info on this Bot"},
    "song": {
        "name": "Song Finder:\t`!song [SONG NAME]`",
        "value": "Searches Brucebase for the requested song, returns a link as well as number of times it has been played.",  # noqa: E501
    },
    "location": {
        "name": "Location Finder:\t`!city [CITY_NAME] / !state [STATE ABBREV] / !country [COUNTRY_NAME]`",  # noqa: E501
        "value": "Searches the database for how many shows have been played in a specified city/state/country.",  # noqa: E501
    },
    "tour": {
        "name": "Tour Stats:\t`!tour [TOUR_NAME]`",
        "value": "Searches the database for the specified tour, and returns stats for it",  # noqa: E501
    },
    "album": {
        "name": "Album Stats:\t`!album [ALBUM] / !a [ALBUM]`",
        "value": "Searches the database for the specified album, and returns stats for it",  # noqa: E501
    },
    "person": {
        "name": "Person Finder:\t`!person [NAME] / !p [NAME]`",
        "value": "Searches the database for the specified person, and returns stats about them",  # noqa: E501
    },
    "band": {
        "name": "Band Finder:\t`!band [NAME] / !b [NAME]`",
        "value": "Searches the database for the specified band, and returns stats about them",  # noqa: E501
    },
}

cmds = [
    "`!sl <yyyy-mm-dd>`, `!setlist <yyyy-mm-dd>` | _Returns the setlist of that show from Brucebase_",  # noqa: E501
    "`!cover <yyyy-mm-dd>` | _Will get artwork from my website for that show_",
    "`!jl <yyyy-mm-dd>` | _Returns link to Jungleland torrents with specified date_",
    "`!otd <mm-dd>` | _Returns a list of shows that happened on a certain day, leave blank for current date_",  # noqa: E501
    "`!artwork <yyyy-mm-dd>` | _Returns list of artwork from Jungleland.it_",
    "`!bootleg <yyyy-mm-dd>` | _Returns link to SpringsteenLyrics with list of Bootlegs for that date_",  # noqa: E501
]

cmds2 = [
    "`!song <song>` | _Searches for the requested song, returns a link as well as number of times it has been played_",  # noqa: E501
    "`!tour <tour>` | _Searches the database for the specified tour, and returns stats for it_",  # noqa: E501
    "",
    "`!album <album name>`, `!a <album name>` | _Searches the database for the specified album, and returns stats for it_",  # noqa: E501
    "`!person <person name>`, `!p <person name>` | _Searches the database for the specified person, and returns stats about them_",  # noqa: E501
    "`!band <band name>`, `!b <band name>` | _Searches the database for the specified band, and returns stats about them_",  # noqa: E501
    "",
    "`!city <city>` | _Searches the database for how many shows have been played in a specified city_",  # noqa: E501
    "`!state <state/abbrev>` | _Searches the database for how many shows have been played in a specified state_",  # noqa: E501
    "`!country <country>` | _Searches the database for how many shows have been played in a specified country_",  # noqa: E501
]


@bot.command(aliases=["bothelp"])
async def bot_help(ctx: commands.Context) -> None:
    """Return a list of bot commands."""
    embed = create_embed(
        "Brucebot Help",
        "Type `!botinfo` for information about this bot",
        ctx,
    )

    embed.add_field(name="Commands:", value="\n".join(cmds), inline=False)
    embed.add_field(name="", value="\n".join(cmds2), inline=False)

    await ctx.send(embed=embed)


@bot.command(aliases=["botinfo"])
async def bot_info(ctx: commands.Context) -> None:
    """Return information on the bot."""
    embed = create_embed(
        "Brucebot: A Bot to get info on Bruce Springsteen's performing history",
        "Created by Lilbud (March 2023)",
        ctx,
    )

    embed.add_field(name="My Site:", value="https://lilbud.github.io")

    embed.add_field(
        name="Sources:",
        value="* Setlists from [Brucebase](http://brucebase.wikidot.com/)"  # noqa: ISC003
        + "\n* Bootleg info from [SpringsteenLyrics](https://www.springsteenlyrics.com)"
        + "\n* Bootleg Covers from My Website (see above)"
        + "\n* Torrent List from [Jungleland](http://jungleland.dnsalias.com)"
        + "\n* Artwork from [Jungleland.it](http://www.jungleland.it/html/artwork.htm)",
        inline=False,
    )

    embed.add_field(
        name="Issues List:",
        value="* Discord displays images inline, rather than new gallery view"  # noqa: ISC003
        + "\n* Some setlists might have odd formatting"
        + "\n* Song searching is still very much untested, results might be odd",
        inline=False,
    )

    embed.add_field(
        name="Help:",
        value="Type '!bothelp' to get list of commands",
        inline="False",
    )

    await ctx.send(embed=embed)


@bot.command(aliases=["botstatus"])
async def bot_status(ctx: commands.Context) -> None:
    """Return a message if bot is online and active."""
    await ctx.send("Someone IS Alive Out There")
