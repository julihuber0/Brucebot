"""
get_cover
returns covers from my site
"""

# import requests
import httpx
import json
from import_stuff import bot, dateinDB
from error_message import error_message
from bs4 import BeautifulSoup as bs4


@bot.command(aliases=["cover", "getcover"])
async def get_cover(ctx, date=None):
    """Gets covers from my site based in input date"""

    if dateinDB(date):
        links = []
        url = f"https://github.com/lilbud/Bootleg_Covers/tree/main/Bruce_Springsteen/covers/{date[0:4]}"

        with httpx.Client() as client:
            try:
                r = client.get(url)
            except httpx.RequestError as exc:
                print(f"An error occurred while requesting {exc.request.url!r}.")

            soup = bs4(r.text, "lxml")
            covers = json.loads(str(soup.find("p").text))["payload"]["tree"]["items"]

            for cover in covers:
                if date in cover["path"]:
                    links.append(f"https://raw.githubusercontent.com/lilbud/Bootleg_Covers/main/{cover["path"]}")
            
            if links:
                await ctx.send("\n".join(links))
            else:
                await ctx.send(error_message("cover"))
    else:
        await ctx.send(error_message("date"))
