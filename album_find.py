from import_stuff import bot, cur, main_url, albums
from create_embed import create_embed
from error_message import error_message
import re

album_name = note = ""
songs = []

def album_name_fix(album):
    # album name: [list of shorthand/abbreviations]
    for key, value in albums.items():
        for v in value:
            if v.lower() == album.lower():
                album_name = key
    
    if album_name:
        return album_name
    else:
        return album
    
def checkDBforalbum(album):
    check = cur.execute(f"""SELECT EXISTS(SELECT 1 FROM ALBUMS WHERE LOWER(album_name) LIKE '{album}')""").fetchone()

    if check:
        return True

    return False

@bot.command(aliases=['album', 'a'])
async def album_finder(ctx, *album):
    """Gets info on album"""
    input = " ".join(album).replace("'", "''")
    inputFixed = album_name_fix(input)

    if checkDBforalbum(inputFixed) and inputFixed.lower() != "tracks":
        info = cur.execute(f"""SELECT album_name, album_year, song_url FROM ALBUMS WHERE LOWER(album_name) LIKE '{inputFixed.lower()}' ORDER BY song_num ASC""").fetchall()
        embed = create_embed(info[0], f"Year: {info[1]}", ctx)

        plays = cur.execute(f"""select song_name, num_plays FROM SONGS WHERE song_url IN (SELECT song_url FROM ALBUMS WHERE album_name LIKE '{info[0][0]}') AND num_plays != '' ORDER BY CAST(num_plays as integer) ASC""").fetchall()
        premiere = cur.execute(f"""select song_name, first_played FROM SONGS WHERE song_url IN (SELECT song_url FROM ALBUMS WHERE album_name LIKE '{info[0][0]}') AND first_played != '' ORDER BY first_played ASC""").fetchall()

        for s in info:
            find_song = cur.execute(f"""SELECT song_name, num_plays FROM SONGS WHERE song_url LIKE '{s[2]}'""").fetchone()

            #               name - num plays
            # most: plays[-1][0] - plays[-1][1]
            # least: plays[0][0] - plays[0][1]

            if find_song[1] == "":
                songs.append(f"**{find_song[0]}**")
                note = " (Note: Not All Songs Played Live Yet)"
            else:
                songs.append(find_song[0])
        
        song_list = ", ".join(songs)
        embed.add_field(name="Songs (Bold = Not Played):", value=f"{song_list}", inline=False)

        embed.add_field(name="Most Played:", value=f"{plays[-1][0]} ({plays[-1][1]})", inline=False)
        embed.add_field(name="Least Played:", value=f"{plays[0][0]} ({plays[0][1]})", inline=False)

        first_date = cur.execute(f"""SELECT event_date FROM EVENTS WHERE event_url LIKE '{premiere[0][1]}'""").fetchone()
        last_date = cur.execute(f"""SELECT event_date FROM EVENTS WHERE event_url LIKE '{premiere[-1][1]}'""").fetchone()

        embed.add_field(name=f"First/Last Premiered{note}:", value=f"{premiere[0][0]} ([{first_date[0]}]({main_url}{premiere[0][1]})) / {premiere[-1][0]} ([{last_date[0]}]({main_url}{premiere[-1][1]}))", inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{error_message('album')}, No results for: {album}")

    # if album_info and album_info[0][0] != "Tracks":
    #     embed = create_embed(album_info[0][0], f"Year: {album_info[0][1]}", ctx)
    #     plays = cur.execute(f"""select song_name, num_plays FROM SONGS WHERE song_url IN (SELECT song_url FROM ALBUMS WHERE album_name LIKE '{album_info[0][0]}') AND num_plays != '' ORDER BY CAST(num_plays as integer) ASC""").fetchall()
    #     premiere = cur.execute(f"""select song_name, first_played FROM SONGS WHERE song_url IN (SELECT song_url FROM ALBUMS WHERE album_name LIKE '{album_info[0][0]}') AND first_played != '' ORDER BY first_played ASC""").fetchall()

    #     for s in album_info:
    #         find_song = cur.execute(f"""SELECT song_name, num_plays FROM SONGS WHERE song_url LIKE '{s[2]}'""").fetchone()

    #         if find_song[1] == "":
    #             songs.append(f"**{find_song[0]}**")
    #         else:
    #             songs.append(find_song[0])
        
    #     song_list = ", ".join(songs)
    #     embed.add_field(name="Songs (Bold = Not Played):", value=f"{song_list}", inline=False)

    #     embed.add_field(name="Most/Least Played:", value=f"{plays[-1][0]} ({plays[-1][1]}) / {plays[0][0]} ({plays[0][1]})", inline=False)

    #     first_date = cur.execute(f"""SELECT event_date FROM EVENTS WHERE event_url LIKE '{premiere[0][1]}'""").fetchone()
    #     last_date = cur.execute(f"""SELECT event_date FROM EVENTS WHERE event_url LIKE '{premiere[-1][1]}'""").fetchone()

    #     embed.add_field(name="First/Last Premiered (Note: Not All Songs Played Live Yet):", value=f"{premiere[0][0]} ([{first_date[0]}]({main_url}{premiere[0][1]})) / {premiere[-1][0]} ([{last_date[0]}]({main_url}{premiere[-1][1]}))", inline=False)

    #     await ctx.send(embed=embed)
    # else:
    #     await ctx.send(f"{error_message('album')}, No results for: {album_to_find}")