"""
get_cover
returns covers from my site
"""

# import requests
import httpx
import re
from import_stuff import bot, dateinDB
from error_message import error_message
from bs4 import BeautifulSoup as bs4


@bot.command(aliases=["cover", "getcover"])
async def get_cover(ctx, date=None):
    """Gets covers from my site based in input date"""

    if dateinDB(date):
        links = []
        date_string = '{"name":"' + date
        url = f"https://github.com/lilbud/Bootleg_Covers/raw/main/Bruce_Springsteen/covers/{date[0:4]}/"

        with httpx.Client() as client:
            try:
                r = client.get(url).text
            except httpx.RequestError as exc:
                print(f"An error occurred while requesting {exc.request.url!r}.")

            # r = requests.get(url).text
            soup = bs4(r, "lxml")

            for s in soup.text.split(","):
                if date_string in s:
                    for m in re.findall(f'{date}.*[^"]', s):
                        links.append(f"{url}{m}")

            if links:
                await ctx.send("\n".join(links))
            else:
                await ctx.send(error_message("cover"))
    else:
        await ctx.send(error_message("date"))
