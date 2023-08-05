import re, discord, os, datetime, sqlite3, requests
from zoneinfo import ZoneInfo
from discord.ext import commands
#from keep_alive import keep_alive
from createEmbed import createEmbed
from errormsg import errorMessage

months = ['_None', 'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December']
cDate = datetime.datetime.now(ZoneInfo('US/Eastern'))

mainURL = "http://brucebase.wikidot.com"

conn = sqlite3.connect(os.path.abspath(__file__) + "\Databruce\_database\database.sqlite")
cur = conn.cursor()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = '!', intents=intents, help_command=None)

def dateChecker(date):
  if re.search("\d{4}-\d{2}-\d{2}", date):
    return True
  else:
    return False