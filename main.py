from importStuff import *
from botinfo import botInfo, botHelp
from setlistFinder import setlistFinder
from getCover import covers
from jungleland import junglelandTorrent
from on_this_day import on_this_day
from songFinder import sFind
from bootleg import bootlegFind

@bot.event
async def on_ready():
  print(f'Bot online and logged in as {bot.user}')

#keep_alive()
my_secret = os.environ['TOKEN']
bot.run(my_secret)