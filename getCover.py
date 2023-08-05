from importStuff import *

@bot.command(aliases=['cover', 'getcover'])
async def covers(ctx, date):

  if dateChecker(date):
    links = []
    URL = "https://github.com/lilbud/Bootleg-Covers/raw/main/Bruce_Springsteen/Covers/" + date[0:4] + "/" + date
    
    r = requests.get(URL + ".jpg")
  
    if r.status_code == 200:
      links.append((URL + ".jpg"))
    else:
      r = requests.get(URL + ".png")
      if r.status_code == 200:
        links.append((URL + ".png"))
    
    for i in range(1,4):
      r = requests.get(URL + "_" + str(i) + ".jpg")
      
      if r.status_code == 200:
        links.append((URL + "_" + str(i) + ".jpg"))
      else:
        r = requests.get(URL + "_" + str(i) + ".png")
        if r.status_code == 200:
          links.append((URL + "_" + str(i) + ".png"))
    
    if links:
      await ctx.send("\n".join(links))
    else:
      await ctx.send(errorMessage("cover"))
  else:
    await(ctx.send(errorMessage("date")))