import discord
import sys
import youtube_dl
import asyncio
import os

import configparser
from discord.ext import commands
from libs.config_loader import config
from discord.ext.commands import has_permissions
from libs.Youtube import  YoutubeStream, is_url
import logging
from discord import player
from collections import deque

class MusicCog(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.config = config()
        self.settings = self.config["SETTINGS"]
        self.is_play = False
        self.play_next_song = asyncio.Event()
        self.songs_url_queue = asyncio.Queue()
        self.songs = asyncio.Queue()
        self.play_next_song = asyncio.Event()


    async def audio_player_task(self, ctx):
        while True:
            self.play_next_song.clear()
            current = await self.songs.get()
            ctx.voice_client.play(current, after=self.toggle_next)
            await ctx.send(f"Now playing {current.title}")
            await self.play_next_song.wait()
        #ctx.voice_client.disconnect()


    def toggle_next(self):
        self.client.loop.call_soon_threadsafe(self.play_next_song.set)


    @commands.command()
    async def play(self, ctx, query:str):
        if query:
            try:
                async with ctx.typing():
                    player = await YoutubeStream.from_url(query, loop=self.client.loop, stream=False)
                    await self.songs.put(player)
                    await self.client.loop.create_task(self.audio_player_task(ctx))
                    
            except Exception as error:
                #logging.error("MusicCog Error: %s", extra=error)
                print(error)
        else:
            ctx.send(f"Take song name")
        
 
    @commands.command()
    async def volume(self, ctx, volume:int):
        volume_graph = volume
        name = self.settings["bot_name"]
        if ctx.voice_client is None:
            return await ctx.send(f"{name} is not connected")
        if volume > 1000:
            volume = 1000
        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}")


    @commands.command()
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()


    @commands.command()
    async def skip(self, ctx):
        self.toggle_next()

    @commands.command()
    async def queue(self, ctx, query:str=None, song:str=None):
        if query is None:
            embed = discord.Embed(colour=discord.Color.teal())
            i = 1
            for son in self.songs:
                embed.add_field(name=i, value=son.title, inline=True)
                i += 1
            await ctx.send(embed=embed)
        elif query == 'add' and song is not None:
            player = await YoutubeStream.from_url(song, loop=self.client.loop, stream=False)
            await self.songs.put(player)
            await ctx.send(f"Song [{player.title}] has been added to queue")
    
    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                try:
                    if self.config.has_option("SETTINGS", "music_channel"):
                        conf = self.config["SETTINGS"]["music_channel"]
                        if str(conf) == str(ctx.message.channel.name):
                            channel = ctx.author.voice.channel
                            await channel.connect()
                    else:
                        channel = ctx.author.voice.channel
                        await channel.connect()
                except discord.errors.ClientException as error:
                    logging.error("Connect Error: %s", extra=error)
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


def setup(client):
    client.add_cog(MusicCog(client))
