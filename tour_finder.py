import re
from import_stuff import bot, cur, main_url, tour_name_fix
from create_embed import create_embed
from error_message import error_message

@bot.command(aliases=['tour'])
async def tour_stats(ctx, *tour):
    #id, url, name, num_shows, num_songs

    if len(" ".join(tour)) > 1:
        tour_name = tour_name_fix(" ".join(tour).replace("'", "''"))

        if cur.execute(f"""SELECT * FROM TOURS WHERE tour_name ILIKE '{tour_name}'""").fetchall():
            stats = cur.execute(f"""SELECT * FROM TOURS WHERE tour_name ILIKE '{tour_name}'""").fetchall()[0]
        else:
            stats = cur.execute(f"""SELECT * FROM TOURS WHERE tour_name ILIKE '%{tour_name}%'""").fetchall()[0]

        if stats:
            first_last = cur.execute(f"""SELECT MIN(event_date), MAX(event_date) FROM EVENTS WHERE tour LIKE '{stats[2].replace("'", "''")}' AND event_url LIKE '/gig:%'""").fetchall()[0]
            
            first_link = cur.execute(f"""SELECT event_url FROM EVENTS WHERE event_date LIKE '{first_last[0]}'""").fetchone()[0]
            last_link = cur.execute(f"""SELECT event_url FROM EVENTS WHERE event_date LIKE '{first_last[1]}'""").fetchone()[0]

            embed = create_embed(f"Tour: {stats[2]}", f"[Tour Stats]({main_url}{stats[1]}) | [Tour Songs]({main_url}{stats[1].replace('shows', 'songs')})", ctx)

            #first show, last show, num shows, num songs
            embed.add_field(name="Number of Shows:", value=f"{stats[3]}", inline=False)
            embed.add_field(name="First Show:", value=f"[{first_last[0]}]({main_url}{first_link})", inline=False)
            embed.add_field(name="Last Show:", value=f"[{first_last[1]}]({main_url}{last_link})", inline=False)
            embed.add_field(name="Number of Songs:", value=f"{stats[4]}", inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(error_message("tour"))
    else:
        await ctx.send(error_message("tour"))