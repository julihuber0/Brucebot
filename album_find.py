from import_stuff import bot, cur, main_url
from create_embed import create_embed
from error_message import error_message
import re

# all emotes surrounded by : :
# greetings, wiess, btr, darkness, theriver, bitusa
# tol, ht, lt, gotj, therising, devils, magic, woad
# wreckingball, highhopes, westernstars, lettertoyou
# otss

# 7585, broadway, dublin, essential, greatesthits, livenyc
# nonukes, seeger, thepromise, tracks, tttb

def album_name_fix(album): # wiess, btr, bitusa, tol, ht, lt, joad, woad, wb, hh, ws, lty, otss
    if re.search(":*wiess:*", album, re.IGNORECASE):
        return "the wild, the innocent"
    elif re.search(":*btr:*", album, re.IGNORECASE):
        return "born to run"
    elif re.search(":*(bitusa| usa):*", album, re.IGNORECASE):
        return "born in the u.s.a."
    elif re.search(":*(tol|tunnel):*", album, re.IGNORECASE):
        return "tunnel of love"
    elif re.search(":*ht:*", album, re.IGNORECASE):
        return "human touch"
    elif re.search(":*lt:*", album, re.IGNORECASE):
        return "lucky town"
    elif re.search(":*gotj:*", album, re.IGNORECASE):
        return "tom joad"
    elif re.search(":*woad:*", album, re.IGNORECASE):
        return "working on a dream"
    elif re.search(":*wb:*", album, re.IGNORECASE):
        return "wrecking ball"
    elif re.search(":*hh:*", album, re.IGNORECASE):
        return "high hopes"
    elif re.search(":*ws:*", album, re.IGNORECASE):
        return "western stars"
    elif re.search(":*lty:*", album, re.IGNORECASE):
        return "letter to you"
    elif re.search(":*otss:*", album, re.IGNORECASE):
        return "strong survive"
    elif re.search(":*livenyc:*", album, re.IGNORECASE):
        return "Live In New York City"
    elif re.search(":*nonukes:*", album, re.IGNORECASE):
        return "no nukes"
    elif re.search(":*seeger:*", album, re.IGNORECASE):
        return "we shall overcome"
    elif re.search(":*7585:*", album, re.IGNORECASE):
        return "the promise"
    elif re.search(":*tttb:*", album, re.IGNORECASE):
        return "the ties that bind"
    else:
        return album
    

@bot.command(aliases=['album'])
async def album_finder(ctx, *album):
    """Gets info on album"""
    songs = []

    for a in cur.execute(f"""SELECT DISTINCT(album_name) FROM ALBUMS""").fetchall():
        if a[0].lower() == "".join(album).strip(":").lower():
            album_to_find = a[0]
        else:
            album_to_find = album_name_fix(" ".join(album))
    
    # album name
    # year
    # songs
    # most played/least played
    # first/last premiered

    album_info = cur.execute(f"""SELECT album_name, album_year, song_url FROM ALBUMS WHERE album_name LIKE '{album_to_find.replace("'", "''")}' ORDER BY song_num ASC""").fetchall()

    if album_info:
        embed = create_embed(album_info[0][0], f"Year: {album_info[1]}", ctx)

        for s in album_info:
            find_song = cur.execute(f"""SELECT song_name FROM SONGS WHERE song_url LIKE '{s[2]}'""").fetchone()
            songs.append(find_song[0])
        
        song_list = ", ".join(songs)
        embed.add_field(name="Songs:", value=f"{song_list}", inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send(error_message("album"))