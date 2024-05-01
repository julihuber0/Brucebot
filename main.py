"""Main function for this bot."""

import os
import pandas as pd
from import_stuff import bot
from jungleland import jungleland_art, jungleland_torrent
from location_finder import city_finder, country_finder, state_finder
from on_this_day import on_this_day
from relation_find import relation_finder
from setlist_finder import setlist_finder
from song_finder import song_finder
from tour_finder import tour_stats
from album_find import album_finder
from relation_find import relation_finder
from location_finder import city_finder, state_finder, country_finder
from music import randomlive, resume, pause, stop


@bot.event
async def on_ready() -> None:
    """Message to send in log if online and ready."""
    print(f"Bot online and logged in as {bot.user}")


my_secret = os.environ['TOKEN']
bot.run(my_secret)
