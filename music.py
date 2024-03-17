from import_stuff import bot
from discord import FFmpegPCMAudio

voice_clients = {}

@bot.command()
async def randomlive(ctx):
    if (ctx.author.voice):
        try:
            voice = await ctx.message.author.voice.channel.connect()
            voice_clients[voice.guild.id] = voice
        except:
            await ctx.send("There was an error when connecting the music bot")
        
        voice_cl = voice_clients[ctx.guild.id]
        source = FFmpegPCMAudio('btr.m4a')
        voice_cl.play(source)

    else:
        await ctx.send("This command only works when you're in a voice channel")


@bot.command(asiases=['leave'])
async def leave(ctx):
    if (ctx.voice_client):
        voice = voice_clients[ctx.guild.id]
        voice.stop()
        await voice.disconnect()

    else:
        await ctx.send("The bot is currently in no voice channels")


@bot.command()
async def pause(ctx):
    voice = voice_clients[ctx.guild.id]
    if (voice.is_playing()):
        voice.pause()
    else:
        await ctx.send("Nothing is playing at the moment")


@bot.command()
async def resume(ctx):
    voice = voice_clients[ctx.guild.id]
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("There is noting paused at the moment")


@bot.command()
async def stop(ctx):
    voice = voice_clients[ctx.guild.id]
    voice.stop()