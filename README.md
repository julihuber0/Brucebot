# Brucebot
Discord Bot that works with the Databruce project

This repo is the code behind the Discord bot, the code is hosted on Heroku.

See [this](https://github.com/lilbud/Databruce) repo for the Databruce project, which is an SQLite database + associated Python scripts that handle building/updating the database.

While the bot is largely my own code (plus bits from various online forums/posts/stack overflow pages/documentation/etc.) The inspiration for the bots design is owed to the Not Fade Away discord server (and the bots creator, Deadandy), who has a similar bot which provided much of the concept for what I wanted my bot to look like visually. As the first iteration was simply just normal discord text messages with setlists contained in a code block.

Its not a 1:1 exact copy of their embed, but enough to where I feel I should probably mention it.

## Changelog (as best as I can):

- 2023-08-30: Fixed show closer not showing correct value, was using the wrong variable this whole time.
- 2023-08-29: Added link to song lyrics when available.
- 2023-08-15: Added song abbreviation checking again. Was removed when migrating from Repl -> Heroku, but reimplemented recently. Can be added to as more abbreviations/input corrections are needed.
- 2023-08-11: Added song occurence frequency, idea borrowed from bot mentioned above.
- 2023-08-10: Changed '!sl' default command, now will get most recent show instead of erroring out.
- 2023-08-10: Added searching by city/state/country
- 2023-08-06: Migrated bot to Heroku. Got a year of credits from Github for being a student developer. Plus Heroku provides nearly 24/7 runtime, where Repl requires some hacks to have the bot online for a long time, and I could never get those to work. I could've paid like $7 a month to repl for always-on repls, but I'm broke. Heroku (after credits) should only come to a buck or two a month, which is much more reasonable.
- 2023-07-25: Bot fully converted to use [Databruce](https://github.com/lilbud/Databruce) database. Bot originally just scraped Brucebase for the requested info, which was slow, and prone to formatting errors. I worked on the database and converted bot features to point to the database. As of this point, the only scraping needed is to get covers from my github repo.
- 2023-06-14: Started converting bot functions to use database instead of scraping.
- 2023-06-05: Updated bot to format responses using Discord Embeds, rather just normal messages with the setlists in code blocks. Some updated commands as well.
- 2023-03-28: Formatting fixes, mainly with multi-events and missing setlist events showing up wrong.
- 2023-03-27: First public release of bot, hosted on Repl and held together with bubble gum and duct tape. It still is, but thats beside the point.