import discord
import sys
import youtube_dl
import asyncio
import os

import configparser
from discord.ext import commands
from utils.config import config
from discord.ext.commands import has_permissions
from utils.Youtube import YoutubeStream, is_url
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

    @commands.command()
    async def play(self, ctx, query: str):
        if query:
            try:
                async with ctx.typing():
                    pl = await YoutubeStream.from_url(query, loop=self.client.loop, stream=True)
                    ctx.voice_client.play(pl, after=lambda e: print('Player error: %s' % e) if e else None)
                await ctx.send(f"Now playing{pl.title}")
            except Exception as error:
                print(error)
                logging.error("MusicCog Error: %s", extra=error)
        else:
            ctx.send(f"Take song name")

    @commands.command()
    async def volume(self, ctx, volume: int):
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
