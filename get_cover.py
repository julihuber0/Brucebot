"""
get_cover
returns covers from my site
"""

import requests
import re
from import_stuff import bot, dateinDB
from error_message import error_message
from bs4 import BeautifulSoup as bs4
import discord
from discord import Webhook
import aiohttp


@bot.command()
async def send_webhook(ctx, links):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url("webhook_url", session=session)

        # e = discord.Embed(title="Title", description="Description")
        # e.add_field(name="Field 1", value="Value 1")
        # e.add_field(name="Field 2", value="Value 2")
        match (len(links)):
            case 1:
                embed1 = discord.Embed(url="https://lilbud.github.io").set_image(
                    url=links[0]
                )
                await webhook.send(embeds=[embed1])
            case 2:
                embed1 = discord.Embed(url="https://lilbud.github.io").set_image(
                    url=links[0]
                )
                embed2 = discord.Embed(url="https://lilbud.github.io").set_image(
                    url=links[1]
                )
                await webhook.send(embeds=[embed1, embed2])
            case 3:
                embed1 = discord.Embed(url="https://lilbud.github.io").set_image(
                    url=links[0]
                )
                embed2 = discord.Embed(url="https://lilbud.github.io").set_image(
                    url=links[1]
                )
                embed3 = discord.Embed(url="https://lilbud.github.io").set_image(
                    url=links[2]
                )
                await webhook.send(embeds=[embed1, embed2, embed3])
            case 4:
                embed1 = discord.Embed(url="https://lilbud.github.io").set_image(
                    url=links[0]
                )
                embed2 = discord.Embed(url="https://lilbud.github.io").set_image(
                    url=links[1]
                )
                embed3 = discord.Embed(url="https://lilbud.github.io").set_image(
                    url=links[2]
                )
                embed4 = discord.Embed(url="https://lilbud.github.io").set_image(
                    url=links[3]
                )
                await webhook.send(embeds=[embed1, embed2, embed3, embed4])


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
                    # embed1 = discord.Embed(url="https://lilbud.github.io").set_image(
                    #     url=links[0]
                    # )

            if links:
                await send_webhook(ctx, links)

            # await ctx.send("\n".join(links))

        else:
            await ctx.send(error_message("cover"))
    else:
        await ctx.send(error_message("date"))
