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
		r = requests.get(f"{url}{date}.jpg")

		if r.status_code == 200:
			links.append((f"{url}{date}.jpg"))
		else:
			r = requests.get(f"{url}{date}.png")
			if r.status_code == 200:
				links.append((f"{url}{date}.png"))

		for i in range(1, 4):
			r = requests.get(f"{url}{date}_{i}.jpg")

			if r.status_code == 200:
				links.append((f"{url}{date}_{i}.jpg"))
			else:
				r = requests.get(f"{url}{date}_{i}.png")
				if r.status_code == 200:
					links.append((f"{url}{date}_{i}.png"))

		if links:
			await ctx.send("\n".join(links))
		else:
			await ctx.send(error_message("cover"))
	else:
		await(ctx.send(error_message("date")))
