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

albums = {"Greetings From Asbury Park, N.J.": ["greetings"],
"The Wild, The Innocent & The E Street Shuffle": ["wiess"],
"Born To Run": ["btr"],
"Darkness On The Edge Of Town": ["darkness"],
"The River": ["theriver"],
"Nebraska": ["nebraska"],
"Born In The U.S.A.": ["bitusa", "born in the usa"],
"Tunnel Of Love": ["tol", "tunnel"],
"Human Touch": ["ht", "humantouch"],
"Lucky Town": ["lt", "luckytown"],
"The Ghost Of Tom Joad": ["gotj", "joad"],
"The Rising": ["therising"],
"Devils & Dust": [2005, "studio"],
"We Shall Overcome": [2006, "studio"],
"Magic": [2007, "studio"],
"Working On A Dream": [2009, "studio"],
"Wrecking Ball": [2012, "studio"],
"High Hopes": [2014, "studio"],
"American Beauty EP": [2014, "studio"],
"Western Stars": [2019, "studio"],
"Letter To You": [2020, "studio"],
"Only The Strong Survive": [2022, "studio"],
"Greatest Hits": [1995, "compilation"],
"Blood Brothers EP": [1996, "compilation"],
"Tracks": [1998, "compilation"],
"18 Tracks": [1999, "compilation"],
"The Essential": [2003, "compilation"],
"Greatest Hits '09": [2009, "compilation"],
"The Promise": [2010, "studio"],
"Collection: 1973-2012": [2012, "compilation"],
"The Ties That Bind": [2015, "compilation"],
"Chapter And Verse": [2016, "compilation"],
"Spare Parts": [2018, "compilation"],
"Live 1975–85": [1986, "live"],
"Chimes Of Freedom EP": [1988, "live"],
"In Concert/MTV Plugged": [1992, "live"],
"Live In New York City": [2001, "live"],
"Hammersmith Odeon, London '75": [2006, "live"],
"Live In Dublin": [2007, "live"],
"Magic Tour Highlights": [2008, "live"],
"Springsteen On Broadway": [2018, "live"],
"Western Stars (Songs From The Film)": [2019, "live"],
"The Legendary 1979 No Nukes Concerts": [2021, "live"]}

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

def location_name_get(location_url):
	location = cur.execute(f"""SELECT venue_name, venue_city, venue_state, venue_country FROM VENUES WHERE venue_url LIKE '{location_url}'""").fetchone()
	return f"{', '.join(list(filter(None, location[0:])))}"