"""
Bot Info
functions to:
    list commands
    list info
    show status
"""

from import_stuff import bot
from create_embed import create_embed

@bot.command(aliases=['help'])
async def bot_help(ctx):
    """Returns a list of bot commands"""

    embed = create_embed("Brucebot Help", "List of Brucebot Commands")

    embed.add_field(name="Setlist Finder:\t`!sl YYYY-MM-DD`  OR  `!setlist [YYYY-MM-DD]`",
                    value="Returns the setlist of that show from Brucebase",
                    inline=False)

    embed.add_field(name="Cover:\t`!cover YYYY-MM-DD`",
                    value="Will get artwork from my website for that show",
                    inline=False)

    embed.add_field(name="Jungleland:\t`!jl YYYY-MM-DD`",
                    value="Returns link to Jungleland torrents with specified date",
                    inline=False)
    embed.add_field(name="On This Day:\t`!otd`  OR  `!otd MM-DD`",
                    value="Returns a list of shows that happened on this day. Can leave blank for the current day, or enter a specific Month and Day",
                    inline=False)

    embed.add_field(name="Artwork:\t`!artwork YYYY-MM-DD`",
                    value="Returns list of artwork from Jungleland.it",
                    inline=False)

    embed.add_field(name="Bootleg:\t`!bootleg YYYY-MM-DD`",
                    value="Returns link to SpringsteenLyrics with list of Bootlegs for that date",
                    inline=False)

    embed.add_field(name="Info:\t`!info`",
                    value="Returns Info on this Bot",
                    inline=False)

    embed.add_field(name="Song Finder:\t`!song [SONG NAME]`",
                    value="Searches Brucebase for the requested song, returns a link as well as number of times it has been played.",
                    inline=False)

    await ctx.send(embed=embed)


@bot.command(aliases=['info'])
async def bot_info(ctx):
    """Returns information on the bot"""

    embed = create_embed("Brucebot: A Bot to get info on Bruce Springsteen's performing history",
                        "Created by Lilbud (March 2023)")

    embed.add_field(name="My Site:",
                    value="https://lilbud.github.io")

    embed.add_field(name="Sources:",
                    value="* Setlists from [Brucebase](http://brucebase.wikidot.com/)"
                    + "\n* Bootleg info from [SpringsteenLyrics](https://www.springsteenlyrics.com)"
                    + "\n* Bootleg Covers from My Website (see above)"
                    + "\n* Torrent List from [Jungleland](http://jungleland.dnsalias.com)"
                    + "\n* Artwork from [Jungleland.it](http://www.jungleland.it/html/artwork.htm)",
                    inline=False)

    embed.add_field(name="Issues List:",
                    value="* Discord displays images inline, rather than new gallery view"
                    + "\n* Some setlists might have odd formatting"
                    + "\n* Song searching is still very much untested, results might be odd",
                    inline=False)

    embed.add_field(name="Help:",
                    value="Type '!help' to get list of commands",
                    inline="False")

    await ctx.send(embed=embed)


@bot.command(aliases=['status'])
async def bot_status(ctx):
    """Returns a message if bot is online and active"""

    await ctx.send("Someone IS Alive Out There")