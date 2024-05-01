"""Location."""

import re

from discord.ext import commands

from create_embed import create_embed
from error_message import error_message
from import_stuff import bot, cur, main_url, states_and_provinces_abbrev


def city_name_fixer(city_name: str) -> str:
    """List of city names to fix, or shorthand names like 'philly'."""
    match city_name:
        case "st. paul" | "st paul":
            return "saint paul"
        case "philly":
            return "philadelphia"
        case _:
            return city_name


@bot.command(aliases=["city"])
async def city_finder(ctx: commands.Context, *, args: str = "") -> None:
    """Find inputted city in locations."""
    if len(args) > 1:
        city_name = city_name_fixer(args.replace("'", "''").lower())

        cur.execute(
            """SELECT MIN(event_url), MAX(event_url), COUNT(event_url) FROM EVENTS WHERE
            location_url IN (SELECT venue_url FROM VENUES WHERE LOWER(venue_city) = %s)
            AND tour != ''""",
            (city_name,),
        )

        first_last = cur.fetchall()[0]

        if first_last and first_last[2] > 0:
            first_date = re.findall(r"\d{4}-\d{2}-\d{2}", first_last[0])
            last_date = re.findall(r"\d{4}-\d{2}-\d{2}", first_last[1])

            embed = create_embed(f"Database Results for: {city_name}", "", ctx)
            embed.add_field(
                name="Number of Shows:",
                value=str(first_last[2]),
                inline=True,
            )
            embed.add_field(
                name="First Show:",
                value=f"[{first_date[0]}]({main_url}{first_last[0]})",
                inline=True,
            )
            embed.add_field(
                name="Last Show:",
                value=f"[{last_date[0]}]({main_url}{first_last[1]})",
                inline=True,
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"No Results for {city_name}")
    else:
        await ctx.send(error_message("input"))


@bot.command(aliases=["state"])
async def state_finder(ctx: commands.Context, *, args: str = "") -> None:
    """Find state in locations."""
    state_abbrev = ""
    if len(args) >= 2:  # noqa: PLR2004
        for key, value in states_and_provinces_abbrev.items():
            if key.lower() == args or value.lower() == args:
                state_abbev = key
                state_name = value
    else:
        await ctx.send(error_message("input"))

    if len(state_abbev) == 2 or len(state_name) > 2:  # noqa: PLR2004
        cur.execute(
            """SELECT MIN(event_url), MAX(event_url), COUNT(event_url) FROM EVENTS WHERE
            location_url IN (SELECT venue_url FROM VENUES WHERE LOWER(venue_state) = %s)
              AND tour != ''""",
            (state_abbrev,),
        )

        first_last = cur.fetchall()[0]

        if first_last and first_last[2] > 0:
            first_date = re.findall(r"\d{4}-\d{2}-\d{2}", first_last[0])
            last_date = re.findall(r"\d{4}-\d{2}-\d{2}", first_last[1])

            embed = create_embed(f"Database Results for: {state_name.title()}", "", ctx)
            embed.add_field(
                name="Number of Shows:",
                value=str(first_last[2]),
                inline=True,
            )
            embed.add_field(
                name="First Show:",
                value=f"[{first_date[0]}]({main_url}{first_last[0]})",
                inline=True,
            )
            embed.add_field(
                name="Last Show:",
                value=f"[{last_date[0]}]({main_url}{first_last[1]})",
                inline=True,
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"No Results for {state_name.title()}")
    else:
        await ctx.send(error_message("input"))


@bot.command(aliases=["country"])
async def country_finder(ctx: commands.Context, *, args: str = "") -> None:
    """Find country."""
    if len(args) > 1:
        country_name = args.replace("'", "''").lower()
        cur.execute(
            """SELECT MIN(event_url), MAX(event_url), COUNT(event_url) FROM EVENTS WHERE
            location_url IN (SELECT venue_url FROM VENUES WHERE LOWER(venue_country)
            = %s) AND tour != ''""",
            (country_name,),
        )

        first_last = cur.fetchall()[0]

        if first_last and first_last[2] > 0:
            first_date = re.findall(r"\d{4}-\d{2}-\d{2}", first_last[0])
            last_date = re.findall(r"\d{4}-\d{2}-\d{2}", first_last[1])

            embed = create_embed(
                f"Database Results for: {country_name.title()}",
                "",
                ctx,
            )
            embed.add_field(
                name="Number of Shows:",
                value=str(first_last[2]),
                inline=True,
            )
            embed.add_field(
                name="First Show:",
                value=f"[{first_date[0]}]({main_url}{first_last[0]})",
                inline=True,
            )
            embed.add_field(
                name="Last Show:",
                value=f"[{last_date[0]}]({main_url}{first_last[1]})",
                inline=True,
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"No Results for {country_name.title()}")
    else:
        await ctx.send(error_message("input"))
