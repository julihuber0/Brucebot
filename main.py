import os
from import_stuff import bot
from bot_info import bot_info, bot_help
from setlist_finder import setlist_finder
from get_cover import get_cover
from jungleland import jungleland_torrent, jungleland_art
from on_this_day import on_this_day
from song_finder import song_finder
from bootleg import bootleg_find
from location_finder import city_finder, state_finder, country_finder

@bot.event
async def on_ready():
	print(f'Bot online and logged in as {bot.user}')

my_secret = os.environ['TOKEN']
bot.run(my_secret)