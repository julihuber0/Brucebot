from import_stuff import bot
from nextcord import FFmpegPCMAudio
import random as rn
import pandas as pd

voice_clients = {}
queues = {}
title_array = pd.read_csv('/music/songs.csv').values[:,0]

def check_queue(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        filename = queues[id].pop(0)
        path = '/music/' + filename
        source = FFmpegPCMAudio(path)
        voice.pause()
        voice.play(source, after=lambda x=None: check_queue(ctx, id))

def fill_queue(id):
    rn.shuffle(title_array)
    queues[id] = title_array.tolist()

@bot.command()
async def randomlive(ctx):
    if (ctx.author.voice):
        try:
            voice = await ctx.message.author.voice.channel.connect()
            voice_clients[voice.guild.id] = voice
        except:
            await ctx.send("There was an error when connecting the music bot")
        
        id = ctx.guild.id
        fill_queue(id)
        voice_cl = voice_clients[id]
        filename = queues[id].pop(0)
        path = '/music/' + filename
        source = FFmpegPCMAudio(path)
        voice_cl.play(source, after=lambda x=None: check_queue(ctx, id))

    else:
        await ctx.send("This command only works when you're in a voice channel")


@bot.command(asiases=['leave'])
async def leave(ctx):
    if (ctx.voice_client):
        voice = voice_clients[ctx.guild.id]
        await stop(ctx)
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
    queues[ctx.guild.id] = []
    voice.stop()

@bot.command()
async def skip(ctx):
    id = ctx.guild.id
    check_queue(ctx, id)

@bot.command()
async def reshuffle(ctx):
    id = ctx.guild.id
    if queues[id] != []:
        queue = queues[id]
        rn.shuffle(queue)
        queues[id] = queue
    else:
        await ctx.send("Queue is currently empty")