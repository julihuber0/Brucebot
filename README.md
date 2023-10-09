# Brucebot

Discord Bot that works with the Databruce project

This repo is the code behind the Discord bot, the code is hosted on Heroku.

See [this](https://github.com/lilbud/Databruce) repo for the Databruce project, which is an SQLite database + associated Python scripts that handle building/updating the database.

While the bot is largely my own code (plus bits from various online forums/posts/stack overflow pages/documentation/etc.) The inspiration for the bots design is owed to the Not Fade Away discord server (and the bots creator, Deadandy), who has a similar bot which provided much of the concept for what I wanted my bot to look like visually. As the first iteration was simply just normal discord text messages with setlists contained in a code block.

Its not a 1:1 exact copy of their embed, but enough to where I feel I should probably mention it.

## Changelog (as best as I can)

- 2023-10-13: added "relation finder", which will return info on a specified person or band
- 2023-10-13: added "album find", returns stats on an album (song list, most/least played, first/last premiered)
- 2023-10-11: modified the database to only count song opener/closer if the known setlist is more than a single song. As it's unknown exactly where in the set it falls.
- 2023-10-11: on the database, SONGS and TOURS originally just pointed to an event date, which is now changed to the event url. Reason being it's more accurate if there are multiple events on a single date, and the code would just return the first date match which might not be accurate.
- 2023-10-09: while back updated the database and accidentally removed the date column from events (when meaning to from setlist). Ended up modifying the code to work without it as I deemed it unnecessary, then I found out. Added it back, and redid all the code.
- 2023-10-05: added many of the bot functions to the plain database, stuff like song frequency, tour first/last, num times song opened/closed show, and also added a check if the show circulates as a bootleg or has an official release (thanks to the list on brucebase)
- 2023-09-23: added segue arrows to the setlist output. Actually added a column to the database named "segue", which is either true or false. Then in the bot code, I added a check to insert a segue arrow instead of a comma. Just makes things look a little cleaner, and makes it clearer what songs are transitioned into the next or not.
- 2023-09-03: fixed 'on this day' showing out of date order, was missing an "ORDER BY" on the SQL query.  
- 2023-09-01: reimplemented showing of tour debuts in the setlist finder embed. This was a baffling bug, as this feature worked no problem on repl, but stopped working on heroku. Even considering that the databases are technically different (SQLite vs PostgreSQL), they have the same data. And the queries are mostly identical, and the rest work no problem, except tour debuts. No matter what, I couldn't get this query to work in the bot. I could get it to work locally in SQLite, and even on WSL (Win. Subsystem for Linux, the SQLite -> PGSQL converter is only on Linux natively.) The query would work, even testing on Heroku through their "dataclips" option (an SQL interpreter for the database). Finally got it to work by condensing down the branching if statement to determine premiere/bustout/none.
- 2023-08-31: improved speed of 'get_cover'. First method broke a bit ago (web scraping), then I switched to passing a request to my covers Github repo for "images with this date in the name + _NUM + .jpg/.png". This was slow. Was able to find a new way to web scrape the repo, much faster.
- 2023-08-30: Fixed show closer not showing correct value, was using the wrong variable this whole time.
- 2023-08-29: Added link to song lyrics when available.
- 2023-08-15: Added song abbreviation checking again. Was removed when migrating from Repl -> Heroku, but reimplemented recently. Can be added to as more abbreviations/input corrections are needed.
- 2023-08-11: Added song occurence frequency, idea borrowed from bot mentioned above.
- 2023-08-10: Changed '!sl' default command, now will get most recent show instead of erroring out.
- 2023-08-10: Added searching by city/state/country
- 2023-08-06: Migrated bot to Heroku. Got a year of credits from Github for being a student developer. Plus Heroku provides nearly 24/7 runtime, where Repl requires some hacks to have the bot online for a long time, and I could never get those to work. I could've paid like $7 a month to repl for always-on repls, but I'm broke. Heroku (after credits) should only come to a buck or two a month, which is much more reasonable.
- 2023-07-25: Bot fully converted to use [Databruce](https://github.com/lilbud/Databruce) database. Bot originally just scraped Brucebase for the requested info, which was slow, and prone to formatting errors. I worked on the database and converted bot features to point to the database. As of this point, the only scraping needed is to get covers from my github repo.
- 2023-07-07: Added '!artwork', which returns a list of artwork for the inputted date from [Jungleland.it](http://www.jungleland.it/html/artwork.htm). At some point later I worked on implementing the artwork into an sqlite database to speed up the results (as web scraping is quite slow). I'm writing this changelog months later so specific dates are unknown.
- 2023-06-14: Started converting bot functions to use database instead of scraping.
- 2023-06-05: Updated bot to format responses using Discord Embeds, rather just normal messages with the setlists in code blocks. Some updated commands as well.
- 2023-03-28: Formatting fixes, mainly with multi-events and missing setlist events showing up wrong.
- 2023-03-27: First public release of bot, hosted on Repl and held together with bubble gum and duct tape. It still is, but thats beside the point.
