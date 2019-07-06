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


class MusicCog(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.config = config()
        self.settings = self.config["SETTINGS"]
        self.is_play = False
        self.songs = asyncio.Queue()
        self.play_next_song = asyncio.Event()


    @commands.command()
    async def play(self, ctx, query:str):
        if query:
            #await self.songs.put(query)
            player = ctx.voice_client
            try:
                async with ctx.typing():
                    player = await YoutubeStream.from_url(query, loop=self.client.loop, stream=False)
                    ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                    await ctx.send(f"Now playing{player.title}")
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
    async def add(self, ctx, query:str):
        if query:
            await self.songs.put(query)
            await ctx.send(f"Song [{query}] has been added to queue")
        else:
            await ctx.send("You can take song name")


    @commands.command()
    async def queue(self, ctx):
        embed = discord.Embed(colour=discord.Color.teal())
        i = 1
        for son in self.songs:
            embed.add_field(name=i, value=son.title, inline=True)
            i += 1
        await ctx.send(embed=embed)
    
    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                try:
                    if int(self.settings["music_channel"]):
                        channel = self.client.get_channel(int(self.settings["music_channel"]))
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
