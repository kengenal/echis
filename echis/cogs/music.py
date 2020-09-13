import os
import asyncio
from typing import List

import discord

from discord.ext import commands
from discord.ext.commands import Context, command, group

from echis.model.share import SharedSongs
from echis.modules import mixins
from echis.modules.share_playlist import Share
from echis.modules.youtube import YoutubeStream


class Music(mixins.BaseCog):
    songs = asyncio.Queue()
    play_next_song = asyncio.Event()
    stop: bool = False
    volume: float = 5

    async def play_queue(self, ctx: Context):
        while True:
            if self.songs.empty() or self.stop:
                await ctx.voice_client.disconnect()
                break
            self.play_next_song.clear()
            current = await self.songs.get()
            image = [x for x in current.data["thumbnails"] if x['height'] == 188][0]["url"]

            embed = discord.Embed(title=current.title)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
            ctx.voice_client.play(current, after=lambda e: self.toggle_next() if not self.stop else None)
            await self.play_next_song.wait()

    def toggle_next(self):
        self.client.loop.call_soon_threadsafe(self.play_next_song.set)

    @command()
    async def play(self, ctx: Context, *args: str):
        """ play music from youtube you first you need connect to voice channel """
        query = ' '.join(args)
        async with ctx.typing():
            self.stop = False
            if query:
                player = await YoutubeStream.from_url(query, loop=self.client.loop, stream=True)
                await self.songs.put(player)
            else:
                try:
                    share: List[Share] = SharedSongs.objects
                    for song in share:
                        player = await YoutubeStream.from_url(f"{song.artist} {song.title}", loop=self.client.loop,
                                                              stream=True)
                        await self.songs.put(player)
                except Exception:
                    await ctx.send("nothing to play")
            self.client.loop.create_task(self.play_queue(ctx=ctx))

    @command()
    async def volume(self, ctx: Context, volume: int = None):
        """ Change volume  0 - 10 """
        name = os.getenv("BOT_NAME")
        if not volume:
            return await self.volume_diplay(ctx=ctx, volume=int(ctx.voice_client.source.volume * 10))
        if ctx.voice_client is None:
            return await ctx.send(f"{name} is not connected")
        if volume > 10:
            volume = 10
        ctx.voice_client.source.volume = float(volume / 10)
        self.volume = ctx.voice_client.source.volume
        return await self.volume_diplay(ctx=ctx, volume=volume)

    @command()
    async def stop(self, ctx: Context):
        """ stop playing music """
        ctx.voice_client.stop()
        self.stop = True
        await ctx.voice_client.disconnect()

    @group()
    async def queue(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            pass

    @queue.command()
    async def add(self, ctx: Context, name: str):
        player = await YoutubeStream.from_url(name, loop=self.client.loop, stream=True)
        await self.songs.put(player)
        embed = discord.Embed(title=f"Song {player.title} has been added to playlist")
        await ctx.send(embed=embed)

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                try:
                    channel = ctx.author.voice.channel
                    await channel.connect()
                except discord.errors.ClientException as error:
                    print(error)
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    async def volume_diplay(self, ctx: Context, volume: int):
        display_volume = ":loud_sound:  | "
        for i in range(1, 11):
            if i <= int(volume):
                display_volume += ":metal:"
            else:
                display_volume += ":fist:"
        display_volume += ' |'

        embed = discord.Embed(
            title=display_volume,
            description=f"Volume {volume}/10"
        )
        return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Music(client))
