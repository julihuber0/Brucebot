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
        base_url = "https://raw.githubusercontent.com/lilbud/Bootleg_Covers/main"
        url = f"Bruce_Springsteen/covers/{date[0:4]}/{date}"

        with httpx.Client() as client:
            try:
                r = client.get(
                    "https://api.github.com/repos/lilbud/Bootleg_Covers/git/trees/main?recursive=1",
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"
                    },
                )
            except httpx.RequestError as exc:
                print(f"An error occurred while requesting {exc.request.url!r}.")

            res = r.json()

            links = [
                f"{base_url}/{img['path']}" for img in res["tree"] if url in img["path"]
            ]

            if links:
                await ctx.send("\n".join(links))
            else:
                await ctx.send(error_message("cover"))
    else:
        await ctx.send(error_message("date"))
