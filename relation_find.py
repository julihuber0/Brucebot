from import_stuff import bot, cur, main_url
from create_embed import create_embed
from error_message import error_message
import re

def relation_name_fix(name):
    if re.search(" us ", name, re.IGNORECASE):
        return "gary u.s. bonds"
    else:
        return name

@bot.command(aliases=['relation', 'r'])
async def relation_finder(ctx, *name):
    """gets info on bands/people that have played with bruce"""

    nameToFind = relation_name_fix(" ".join(name))

    if len(nameToFind) > 1:
        relationFind = cur.execute(f"""SELECT relation_name, relation_url, appearances, relation_type FROM RELATIONS WHERE LOWER(relation_name) LIKE '%{nameToFind.lower().replace("'", "''")}%'""").fetchone()

        if relationFind:
            name = relationFind[0]
            url = relationFind[1]
            performances = relationFind[2]
            relation_type = relationFind[3]

            embed = create_embed(f"{name} ({relation_type.title()})", f"[Brucebase Page]({main_url}{url})", ctx)

            if int(performances) > 0:
                first_last = cur.execute(f"""SELECT MIN(event_url), MAX(event_url) FROM ON_STAGE WHERE relation_url LIKE '{url}' AND event_url LIKE '/gig:%'""").fetchone()

                first_date = cur.execute(f"""SELECT event_date FROM EVENTS WHERE event_url LIKE '{first_last[0]}'""").fetchall()[0]
                last_date = cur.execute(f"""SELECT event_date FROM EVENTS WHERE event_url LIKE '{first_last[1]}'""").fetchall()[0]

                embed.add_field(name="Performances:", value=f"{performances}", inline=True)
                embed.add_field(name="First Performance:", value=f"[{first_date[0]}]({main_url}{first_last[0]})", inline=True)
                embed.add_field(name="Last Performance:", value=f"[{last_date[0]}]({main_url}{first_last[1]})", inline=True)
            else:
                embed.add_field(name="Performances:", value=f"0", inline=True)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send(error_message("relation"))