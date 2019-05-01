import discord
import sys
import youtube_dl
#import asyncio

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

    @commands.command(pass_context=True)
    async def play(self, ctx, query:str):
        url = None
        if is_url(query) or str(self.config["TOKENS"]["youtube"]) is None:
            url = query
        else:
            search = YoutubeSearch(str(self.config["TOKENS"]["youtube"]))
            search.run()
            url = search.get_url
        async with ctx.typing():
            player = await YoutubeStream.from_url(url, loop=self.client.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send(f"Now playing{player.title}")

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