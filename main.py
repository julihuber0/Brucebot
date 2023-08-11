from importStuff import bot
from botinfo import bot_info, bot_help
from setlist_finder import setlist_finder
from get_cover import get_cover
from jungleland import jungleland_torrent, jungleland_art
from on_this_day import on_this_day
from song_finder import song_finder
from bootleg import bootleg_find

@bot.event
async def on_ready():
  print(f'Bot online and logged in as {bot.user}')

#keep_alive()
my_secret = os.environ['TOKEN']
bot.run(my_secret)