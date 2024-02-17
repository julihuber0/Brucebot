"""
get_cover
returns covers from my site
"""

import requests
import re
from import_stuff import bot, dateinDB, discord
from error_message import error_message
from bs4 import BeautifulSoup as bs4


@bot.command(aliases=["cover", "getcover"])
async def get_cover(ctx, date=None):
    """Gets covers from my site based in input date"""

    if dateinDB(date):
        links = []
        date_string = '{"name":"' + date
        git_url = f"https://github.com/lilbud/Bootleg_Covers/raw/main/Bruce_Springsteen/covers/{date[0:4]}/"

        r = requests.get(git_url).text
        soup = bs4(r, "lxml")

        for s in soup.text.split(","):
            if date_string in s:
                for m in re.findall(f'{date}.*[^"]', s):
                    links.append(f"{git_url}{m}")

        if links:
            for link in links:
                embed = discord.Embed(url="https://lilbud.github.io").set_image(
                    url=link
                )
            # await ctx.send("\n".join(links))
            await ctx.send(embed=embed)
        else:
            await ctx.send(error_message("cover"))
    else:
        await ctx.send(error_message("date"))
