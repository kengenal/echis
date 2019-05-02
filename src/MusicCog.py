import discord
import sys
import youtube_dl
import asyncio
import os
import configparser
from discord.ext import commands
from src.lib.config_loader import config
from discord.ext.commands import has_permissions
from src.lib.Youtube import YoutubeSearch, YoutubeStream, is_url

from discord import player


class MusicCog(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.config = config()
        self.settings = self.config["SETTINGS"]
        self.is_play = False
        self.songs = []

    async def audio_player_task(self, ctx, player):
        while True:
            songs = self.songs
            if not player.is_playing() and songs != []:
                print(songs[0].title)
                player.play(songs[0])
                if self.is_play:
                    await ctx.send(f"Next in queue : {songs[0].title}")
                else:
                    await ctx.send(f"Now playing : {songs[0].title}")
                self.songs.remove(songs[0])
            elif self.songs == []:
                break

    @commands.command()
    async def play(self, ctx, query:str):
        url = None
        if is_url(query) or str(self.config["TOKENS"]["youtube"]) is None:
            url = query
        else:
            search = YoutubeSearch(str(self.config["TOKENS"]["youtube"]))
            search.run()
            url = search.get_url
        async with ctx.typing():
            self.songs.insert(0, await YoutubeStream.from_url(url, loop=self.client.loop, stream=False))
            player = ctx.voice_client
            self.client.loop.create_task(self.audio_player_task(ctx, player))

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
        url = None
        if is_url(query) or str(self.config["TOKENS"]["youtube"]) is None:
            url = query
        else:
            search = YoutubeSearch(str(self.config["TOKENS"]["youtube"]))
            search.run()
            url = search.get_url
        if url:
            self.songs.append(await YoutubeStream.from_url(url, loop=self.client.loop, stream=False))
            await ctx.send(f"Song {query} has been added to queue")

    @commands.command()
    async def remove(self, ctx, query):
        if isinstance(query, int):
            self.songs.remove(query)
        else:
            url = None
            if is_url(query) or str(self.config["TOKENS"]["youtube"]) is None:
                url = query
            else:
                search = YoutubeSearch(str(self.config["TOKENS"]["youtube"]))
                search.run()
                url = search.get_url
            
            take = await YoutubeStream.from_url(url, loop=self.client.loop, stream=True)
            self.songs.remove(take)
        await ctx.send(f"Song {query} has been removed from queue")
        

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
                if str(self.settings["music_channel"]):
                    channel = self.client.get_channel(int(self.settings["music_channel"]))
                else:
                    channel = ctx.author.voice.channel
                await channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()



def setup(client):
    client.add_cog(MusicCog(client))