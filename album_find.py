from import_stuff import bot, cur, main_url, albums
from create_embed import create_embed
from error_message import error_message
import re

# all emotes surrounded by : :
# wiess, btr, theriver, bitusa
# tol, ht, lt, gotj, therising, woad
# wreckingball, highhopes, westernstars, lettertoyou
# otss

def album_name_fix(album):
    album_name = ""
    # if re.search("wiess", album, re.IGNORECASE):
    #     return "the wild, the innocent"
    # elif re.search("btr", album, re.IGNORECASE):
    #     return "born to run"
    # elif re.search("theriver", album, re.IGNORECASE):
    #     return "the river"
    # elif re.search("(bitusa| usa)", album, re.IGNORECASE):
    #     return "born in the u.s.a."
    # elif re.search("tol", album, re.IGNORECASE):
    #     return "tunnel of love"
    # elif re.search("ht", album, re.IGNORECASE):
    #     return "human touch"
    # elif re.search("lt", album, re.IGNORECASE):
    #     return "lucky town"
    # elif re.search("gotj", album, re.IGNORECASE):
    #     return "tom joad"
    # elif re.search("therising", album, re.IGNORECASE):
    #     return "rising"
    # elif re.search("woad", album, re.IGNORECASE):
    #     return "working on a dream"
    # elif re.search("(wb|wreckingball)", album, re.IGNORECASE):
    #     return "wrecking ball"
    # elif re.search("(hh|highhopes)", album, re.IGNORECASE):
    #     return "high hopes"
    # elif re.search("(ws|westernstars)", album, re.IGNORECASE):
    #     return "western stars"
    # elif re.search("(lty|lettertoyou)", album, re.IGNORECASE):
    #     return "letter to you"
    # elif re.search("otss", album, re.IGNORECASE):
    #     return "only the strong survive"
    # elif re.search("nonukes", album, re.IGNORECASE):
    #     return "no nukes"
    # elif re.search("seeger", album, re.IGNORECASE):
    #     return "we shall overcome"
    # elif re.search("tttb", album, re.IGNORECASE):
    #     return "the ties that bind"
    # else:
    #     return album
    
    # album name: [list of shorthand/abbreviations]
    for key, value in albums.items():
        for v in value:
            if v.lower() == album.lower():
                album_name = key
    
    if album_name:
        return album_name
    else:
        return album

@bot.command(aliases=['album', 'a'])
async def album_finder(ctx, *album):
    """Gets info on album"""
    songs = []

    album_to_find = album_name_fix(" ".join(album).replace("'", "''")).lower()
    album_info = cur.execute(f"""SELECT album_name, album_year, song_url FROM ALBUMS WHERE LOWER(album_name) LIKE '%{album_to_find}%' AND album_type LIKE 'studio' ORDER BY song_num ASC""").fetchall()

    if album_info:
        embed = create_embed(album_info[0][0], f"Year: {album_info[0][1]}", ctx)
        plays = cur.execute(f"""select song_name, num_plays FROM SONGS WHERE song_url IN (SELECT song_url FROM ALBUMS WHERE album_name LIKE '{album_info[0][0]}' AND album_type LIKE 'studio') AND num_plays != '' ORDER BY CAST(num_plays as integer) ASC""").fetchall()
        premiere = cur.execute(f"""select song_name, first_played FROM SONGS WHERE song_url IN (SELECT song_url FROM ALBUMS WHERE album_name LIKE '{album_info[0][0]}' AND album_type LIKE 'studio') AND first_played != '' ORDER BY first_played ASC""").fetchall()

        for s in album_info:
            find_song = cur.execute(f"""SELECT song_name, num_plays FROM SONGS WHERE song_url LIKE '{s[2]}'""").fetchone()

            if find_song[1] == "":
                songs.append(f"**{find_song[0]}**")
            else:
                songs.append(find_song[0])
        
        song_list = ", ".join(songs)
        embed.add_field(name="Songs (Bold = Not Played):", value=f"{song_list}", inline=False)

        embed.add_field(name="Most/Least Played:", value=f"{plays[-1][0]} ({plays[-1][1]}) / {plays[0][0]} ({plays[0][1]})", inline=False)

        first_date = cur.execute(f"""SELECT event_date FROM EVENTS WHERE event_url LIKE '{premiere[0][1]}'""").fetchone()
        last_date = cur.execute(f"""SELECT event_date FROM EVENTS WHERE event_url LIKE '{premiere[-1][1]}'""").fetchone()

        embed.add_field(name="First/Last Premiered (Note: Not All Songs Played Live Yet):", value=f"{premiere[0][0]} ([{first_date[0]}]({main_url}{premiere[0][1]})) / {premiere[-1][0]} ([{last_date[0]}]({main_url}{premiere[-1][1]}))", inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send(error_message("album"))