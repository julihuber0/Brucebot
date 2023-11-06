import os
import json
import re
botcmds = {
    "setlist": {
        "name": r"Setlist Finder:\t`!sl YYYY-MM-DD`  OR  `!setlist [YYYY-MM-DD]`",
        "value": "Returns the setlist of that show from Brucebase",
    },
    "cover": {
        "name": r"Cover:\t`!cover YYYY-MM-DD`",
        "value": "Will get artwork from my website for that show",
    },
    "jungleland": {
        "name": r"Jungleland:\t`!jl YYYY-MM-DD`",
        "value": "Returns link to Jungleland torrents with specified date",
    },
    "otd": {
        "name": r"On This Day:\t`!otd`  OR  `!otd MM-DD`",
        "value": "Returns a list of shows that happened on this day. Can leave blank for the current day, or enter a specific Month and Day",
    },
    "artwork": {
        "name": r"Artwork:\t`!artwork YYYY-MM-DD`",
        "value": "Returns list of artwork from Jungleland.it",
    },
    "bootleg": {
        "name": r"Bootleg:\t`!bootleg YYYY-MM-DD`",
        "value": "Returns link to SpringsteenLyrics with list of Bootlegs for that date",
    },
    "info": {
        "name": r"Info:\t`!info`",
        "value": "Returns Info on this Bot"
    },
    "song": {
        "name": r"Song Finder:\t`!song [SONG NAME]`",
        "value": "Searches Brucebase for the requested song, returns a link as well as number of times it has been played.",
    },
    "location": {
        "name": r"Location Finder:\t`!city [CITY_NAME] / !state [STATE ABBREV] / !country [COUNTRY_NAME]`",
        "value": "Searches the database for how many shows have been played in a specified city/state/country.",
    },
    "tour": {
        "name": r"Tour Stats:\t`!tour [TOUR_NAME]`",
        "value": "Searches the database for the specified tour, and returns stats for it",
    },
    "album": {
        "name": r"Album Stats:\t`!album [ALBUM] / !a [ALBUM]`",
        "value": "Searches the database for the specified album, and returns stats for it",
    },
    "person": {
        "name": r"Person Finder:\t`!person [NAME] / !p [NAME]`",
        "value": "Searches the database for the specified person, and returns stats about them",
    },
    "band": {
        "name": r"Band Finder:\t`!band [NAME] / !b [NAME]`",
        "value": "Searches the database for the specified band, and returns stats about them",
    },
}


for i in botcmds.keys():
    print(botcmds[i]["name"])
    print(botcmds[i]["value"])
