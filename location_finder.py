from import_stuff import bot, main_url, cur, states_and_provinces_abbrev
from create_embed import create_embed
from error_message import error_message

def city_name_fixer(city_name):
    """running list of city names to fix, or shorthand names like 'philly'"""
    match city_name:
        case 'st. paul' | 'st paul':
            return "saint paul"
        case 'philly':
            return "philadelphia"
        case _:
            return city_name

@bot.command(aliases=['city'])
async def city_finder(ctx, *city):
    if len(" ".join(city)) > 1:
        city_name = city_name_fixer(" ".join(city).replace("'", "''").lower())

        events = cur.execute(f"""SELECT event_date, event_url, event_city FROM EVENTS WHERE LOWER(event_city) LIKE '%{city_name}%' AND tour != '' ORDER BY event_id ASC""").fetchall()
        last = cur.execute(f"""SELECT event_date, event_url, event_city FROM EVENTS WHERE LOWER(event_city) LIKE '%{city_name}%' AND setlist != '' AND tour != '' ORDER BY event_id DESC""").fetchall()

        if events:
            embed = create_embed(f"Database Results for: {events[0][2]}", "", ctx)
            embed.add_field(name="Number of Shows:", value=str(len(events)), inline=True)
            embed.add_field(name="First Show:", value=f"[{events[0][0]}]({main_url}{events[0][1]})", inline=True)
            embed.add_field(name="Last Show:", value=f"[{last[0][0]}]({main_url}{last[0][1]})", inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"No Results for {city_name}")
    else:
        await ctx.send(error_message('input'))


@bot.command(aliases=['state'])
async def state_finder(ctx, *state):
    if len(" ".join(state)) >= 2:
        for key, value in states_and_provinces_abbrev.items():
            if key.lower() == "".join(state).lower():
                state_abbev = key
                state_name = value
            elif value.lower() == " ".join(state).lower():
                state_abbev = key
                state_name = value

    if len(state_abbev) == 2 or len(state_name) > 2:
        events = cur.execute(f"""SELECT event_date, event_url, event_state FROM EVENTS WHERE event_state LIKE '%{state_abbev}%' AND tour != '' ORDER BY event_id ASC""").fetchall()
        last = cur.execute(f"""SELECT event_date, event_url, event_state FROM EVENTS WHERE event_state LIKE '%{state_abbev}%' AND setlist != '' AND tour != '' ORDER BY event_id DESC""").fetchall()

        if events:
            embed = create_embed(f"Database Results for: {state_name}", "", ctx)
            embed.add_field(name="Number of Shows:", value=str(len(events)), inline=True)
            embed.add_field(name="First Show:", value=f"[{events[0][0]}]({main_url}{events[0][1]})", inline=True)
            embed.add_field(name="Last Show:", value=f"[{last[0][0]}]({main_url}{last[0][1]})", inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"No Results for {state_name}")
    else:
        await ctx.send(error_message('input'))

@bot.command(aliases=['country'])
async def country_finder(ctx, *country):
    if len(" ".join(country)) > 1:
        country_name = " ".join(country).replace("'", "''").lower()
        events = cur.execute(f"""SELECT event_date, event_url, event_country FROM EVENTS WHERE LOWER(event_country) LIKE '%{country_name}%' AND tour != '' ORDER BY event_id ASC""").fetchall()
        last = cur.execute(f"""SELECT event_date, event_url, event_country FROM EVENTS WHERE LOWER(event_country) LIKE '%{country_name}%' AND setlist != '' AND tour != '' ORDER BY event_id DESC""").fetchall()

        if events:
            embed = create_embed(f"Database Results for: {events[0][2]}", "", ctx)
            embed.add_field(name="Number of Shows:", value=str(len(events)), inline=True)
            embed.add_field(name="First Show:", value=f"[{events[0][0]}]({main_url}{events[0][1]})", inline=True)
            embed.add_field(name="Last Show:", value=f"[{last[0][0]}]({main_url}{last[0][1]})", inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"No Results for {country_name}")
    else:
        await ctx.send(error_message('input'))