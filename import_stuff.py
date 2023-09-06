"""
import_stuff
all of the import statements needed for the bot
"""

import re
import os
import datetime
import psycopg
import urllib.parse as urlparse
from zoneinfo import ZoneInfo
import discord
from discord.ext import commands

months = ['_None', 'January', 'February', 'March', 'April', 'May', 'June',
		  'July', 'August', 'September', 'October', 'November', 'December']

#from https://gist.github.com/rogerallen/1583593?permalink_comment_id=3699885#gistcomment-3699885
states_and_provinces_abbrev = {
	'AL': 'Alabama',
	'AB': 'Alberta',
	'AK': 'Alaska',
	'AZ': 'Arizona',
	'AR': 'Arkansas',
	'BC': 'British Columbia',
	'CA': 'California',
	'CO': 'Colorado',
	'CT': 'Connecticut',
	'DE': 'Delaware',
	'FL': 'Florida',
	'GA': 'Georgia',
	'HI': 'Hawaii',
	'ID': 'Idaho',
	'IL': 'Illinois',
	'IN': 'Indiana',
	'IA': 'Iowa',
	'KS': 'Kansas',
	'KY': 'Kentucky',
	'LA': 'Louisiana',
	'ME': 'Maine',
	'MD': 'Maryland',
	'MA': 'Massachusetts',
	'MI': 'Michigan',
	'MN': 'Minnesota',
	'MS': 'Mississippi',
	'MO': 'Missouri',
	'MT': 'Montana',
	'NB': 'New Brunswick',
	'NE': 'Nebraska',
	'NV': 'Nevada',
	'NH': 'New Hampshire',
	'NJ': 'New Jersey',
	'NM': 'New Mexico',
	'NY': 'New York',
	'NC': 'North Carolina',
	'ND': 'North Dakota',
	'OH': 'Ohio',
	'OK': 'Oklahoma',
	'ON': 'Ontario',
	'OR': 'Oregon',
	'PA': 'Pennsylvania',
	'QC': 'Quebec',
	'RI': 'Rhode Island',
	'SC': 'South Carolina',
	'SD': 'South Dakota',
	'TN': 'Tennessee',
	'TX': 'Texas',
	'UT': 'Utah',
	'VT': 'Vermont',
	'VA': 'Virginia',
	'WA': 'Washington',
	'WV': 'West Virginia',
	'WI': 'Wisconsin',
	'WY': 'Wyoming',
	'DC': 'District of Columbia',
}

cDate = datetime.datetime.now(ZoneInfo('US/Eastern'))

main_url = "http://brucebase.wikidot.com"

url = urlparse.urlparse(os.environ['DATABASE_URL'])
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

# conn = sqlite3.connect(os.path.abspath(__file__) + "\Databruce\_database\database.sqlite")
conn = psycopg.connect(
	dbname=dbname,
	user=user,
	password=password,
	host=host,
	port=port
)
cur = conn.cursor()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

def date_checker(date):
	if date is not None:
		if re.search("\d{4}-\d{2}-\d{2}", date):
			return True
		else:
			return False
	else:
		return False

def song_name_fix(song):
	pattern = replace = ""
	"""Fixes some possible incorrect song inputs, and also expands abbreviations"""
	if song is not None:
		if re.search(" usa", song, re.IGNORECASE):
			pattern = "usa"
			replace = "u.s.a."
		elif re.search("bitusa", song, re.IGNORECASE):
			pattern = "bitusa"
			replace = "born in the u.s.a."
		elif re.search("btr", song, re.IGNORECASE):
			pattern = "btr"
			replace = "born to run"
		elif re.search("rosie", song, re.IGNORECASE):
			pattern = "rosie"
			replace = "rosalita"

		if pattern and replace:
			return re.sub(pattern, replace, song, flags=re.IGNORECASE)
		else:
			return song

def tour_name_fix(tour):
	#btr, river, bitusa, tol, other band, human touch, lucky town
	if tour is not None:
		if tour == "btr":
			tour = "born to run"
		elif tour == "river":
			tour = "the river tour"
		elif tour == "bitusa":
			tour = "born in the u.s.a. tour"
		elif re.search("usa", tour, re.IGNORECASE):
			tour.replace("usa", "u.s.a.")
		elif re.search("(92|93)", tour, re.IGNORECASE):
			tour = "world tour 1992-93"
		elif re.search("(16|2016)"):
			tour = "the river tour \'16"

		return tour