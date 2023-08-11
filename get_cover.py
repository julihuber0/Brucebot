"""
get_cover
returns covers from my site
"""

import requests
from import_stuff import bot, date_checker
from error_message import error_message

@bot.command(aliases=['cover', 'getcover'])
async def get_cover(ctx, date=None):
    """Gets covers from my site based in input date"""

    if date_checker(date) and date is not None:
        links = []
        url = f"https://github.com/lilbud/Bootleg-Covers/raw/main/Bruce_Springsteen/Covers/{date[0:4]}/"
        r = requests.get(url + f"{date}.jpg", timeout=5)

        if r.status_code == 200:
            links.append((url + f"{date}.jpg"))
        else:
            r = requests.get(url + f"{date}.png", timeout=5)
            if r.status_code == 200:
                links.append((url + f"{date}.png"))

        for i in range(1, 4):
            r = requests.get(url + f"{date}_{str(i)}.jpg", timeout=5)

            if r.status_code == 200:
                links.append((url + f"{date}_{str(i)}.jpg"))
            else:
                r = requests.get(url + f"{date}_{str(i)}.png", timeout=5)
                if r.status_code == 200:
                    links.append((url + f"{date}_{str(i)}.png"))

        if links:
            await ctx.send("\n".join(links))
        else:
            await ctx.send(error_message("cover"))
    else:
        await(ctx.send(error_message("date")))
