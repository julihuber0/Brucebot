from import_stuff import bot, main_url, cur, states_and_provinces_abbrev
from create_embed import create_embed
from error_message import error_message
import re

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

		first_last = cur.execute(f"""SELECT MIN(event_url), MAX(event_url), COUNT(event_url) FROM EVENTS WHERE location_url IN (SELECT venue_url FROM VENUES WHERE LOWER(venue_city) LIKE '{city_name}') AND tour != ''""").fetchall()[0]
		# last_event = cur.execute(f"""SELECT event_url FROM EVENTS WHERE location_url IN (SELECT venue_url FROM VENUES WHERE LOWER(venue_city) LIKE '{city_name}') AND setlist != '' AND tour != '' ORDER BY event_id DESC""").fetchone()

		if first_last and first_last[2] > 0:
			first_date = re.findall("\d{4}-\d{2}-\d{2}", first_last[0])
			last_date = re.findall("\d{4}-\d{2}-\d{2}", first_last[1])

			embed = create_embed(f"Database Results for: {city_name}", "", ctx)
			embed.add_field(name="Number of Shows:", value=str(first_last[2]), inline=True)
			embed.add_field(name="First Show:", value=f"[{first_date[0]}]({main_url}{first_last[0]})", inline=True)
			embed.add_field(name="Last Show:", value=f"[{last_date[0]}]({main_url}{first_last[1]})", inline=True)
			await ctx.send(embed=embed)
		else:
			await ctx.send(f"No Results for {city_name}")
	else:
		await ctx.send(error_message('input'))


@bot.command(aliases=['state'])
async def state_finder(ctx, *state):
	state_abbrev = ""
	if len(" ".join(state)) >= 2:
		for key, value in states_and_provinces_abbrev.items():
			if key.lower() == "".join(state).lower():
				state_abbev = key
				state_name = value
			elif value.lower() == " ".join(state).lower():
				state_abbev = key
				state_name = value
	else:
		await ctx.send(error_message('input'))

	if len(state_abbev) == 2 or len(state_name) > 2:

		# first = cur.execute(f"""SELECT event_date, event_url FROM EVENTS WHERE location_url IN (SELECT venue_url FROM VENUES WHERE venue_state LIKE '{state_abbev}') AND tour != '' GROUP BY event_url ORDER_BY event_id ASC""").fetchall()
		# last = cur.execute(f"""SELECT event_date, event_url FROM EVENTS WHERE location_url IN (SELECT venue_url FROM VENUES WHERE venue_state LIKE '{state_abbev}') AND tour != '' GROUP BY event_url ORDER BY event_id DESC""").fetchall()

		first_last = cur.execute(f"""SELECT MIN(event_url), MAX(event_url), COUNT(event_url) FROM EVENTS WHERE location_url IN (SELECT venue_url FROM VENUES WHERE LOWER(venue_state) LIKE '{state_abbrev}') AND tour != ''""").fetchall()[0]

		if first_last and first_last[2] > 0:
			first_date = re.findall("\d{4}-\d{2}-\d{2}", first_last[0])
			last_date = re.findall("\d{4}-\d{2}-\d{2}", first_last[1])

			embed = create_embed(f"Database Results for: {state_name.title()}", "", ctx)
			embed.add_field(name="Number of Shows:", value=str(first_last[2]), inline=True)
			embed.add_field(name="First Show:", value=f"[{first_date[0]}]({main_url}{first_last[0]})", inline=True)
			embed.add_field(name="Last Show:", value=f"[{last_date[0]}]({main_url}{first_last[1]})", inline=True)
			await ctx.send(embed=embed)
		else:
			await ctx.send(f"No Results for {state_name.title()}")
	else:
		await ctx.send(error_message('input'))

@bot.command(aliases=['country'])
async def country_finder(ctx, *country):
	if len(" ".join(country)) > 1:
		country_name = " ".join(country).replace("'", "''").lower()
		# events = cur.execute(f"""SELECT event_date, event_url FROM EVENTS WHERE location_url IN (SELECT venue_url FROM VENUES WHERE LOWER(venue_country) LIKE '{country_name}') AND tour != '' ORDER BY event_id ASC""").fetchall()
		# last = cur.execute(f"""SELECT event_date, event_url FROM EVENTS WHERE location_url IN (SELECT venue_url FROM VENUES WHERE LOWER(venue_country) LIKE '{country_name}') AND setlist != '' AND tour != '' ORDER BY event_id DESC""").fetchall()

		first_last = cur.execute(f"""SELECT MIN(event_url), MAX(event_url), COUNT(event_url) FROM EVENTS WHERE location_url IN (SELECT venue_url FROM VENUES WHERE LOWER(venue_country) LIKE '{country_name}') AND tour != ''""").fetchall()[0]

		if first_last and first_last[2] > 0:
			first_date = re.findall("\d{4}-\d{2}-\d{2}", first_last[0])
			last_date = re.findall("\d{4}-\d{2}-\d{2}", first_last[1])

			embed = create_embed(f"Database Results for: {country_name.title()}", "", ctx)
			embed.add_field(name="Number of Shows:", value=str(first_last[2]), inline=True)
			embed.add_field(name="First Show:", value=f"[{first_date[0]}]({main_url}{first_last[0]})", inline=True)
			embed.add_field(name="Last Show:", value=f"[{last_date[0]}]({main_url}{first_last[1]})", inline=True)
			await ctx.send(embed=embed)
		else:
			await ctx.send(f"No Results for {country_name.title()}")
	else:
		await ctx.send(error_message('input'))