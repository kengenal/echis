import asyncio
from typing import List

import discord

from discord.ext import commands
from discord.ext.commands import Context, command, group

from echis import BotClient
from echis.main import settings
from echis.main.settings import BOT_NAME
from echis.model.share import SharedSongs
from echis.modules import mixins
from echis.modules.youtube import YoutubeStream


class Music(mixins.BaseCog):

    def __init__(self, client: BotClient):
        super().__init__(client)
        self.play_next_song = asyncio.Event()
        self.in_queue: List[YoutubeStream] = []
        self.stop: bool = False
        self.set_volume: float = settings.DEFAULT_VOLUME
        self.is_playing = False
        self.current_song: str = ""

    async def play_queue(self, ctx: Context):
        while True:
            if not self.in_queue or self.stop:
                await ctx.voice_client.disconnect()
                break
            self.play_next_song.clear()
            self.is_playing = True
            current = self.in_queue[0]
            self.current_song = current.title
            self.in_queue.pop(0)
            image = [x for x in current.data["thumbnails"] if x['height'] == 188][0]["url"]
            embed = discord.Embed(title=current.title)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
            ctx.voice_client.play(current, after=lambda e: self.toggle_next())

            ctx.voice_client.source.volume = float(self.set_volume)
            await self.play_next_song.wait()

    def toggle_next(self):
        self.client.loop.call_soon_threadsafe(self.play_next_song.set)

    @command(pass_context=True)
    async def play(self, ctx: Context, *args: str):
        """ play music from youtube you first you need connect to voice channel """
        query = ' '.join(args)
        try:
            songs: List[str] = [query] if query else SharedSongs.get_songs_to_play()
            self.stop = False
            for song in songs:
                player = await YoutubeStream.from_url(song, loop=self.client.loop, stream=True)
                self.in_queue.append(player)
        except Exception as error:
            await self.send_to_admin(error=error)
            await ctx.send(embed=discord.Embed(title="nothing to play"))
        if not self.is_playing:
            async with ctx.typing():
                self.client.loop.create_task(self.play_queue(ctx=ctx))

    @command(pass_context=True)
    async def volume(self, ctx: Context, volume: int = None):
        """ Change volume  0 - 10 """
        name = BOT_NAME
        if ctx.voice_client is None:
            return await ctx.send(embed=discord.Embed(title=f":face_with_symbols_over_mouth: {name} is not connected"))
        if not volume:
            return await self.volume_display(ctx=ctx, volume=int(ctx.voice_client.source.volume * 10))
        if volume > 10:
            volume = 10
        ctx.voice_client.source.volume = float(volume / 10)
        self.set_volume = ctx.voice_client.source.volume
        return await self.volume_display(ctx=ctx, volume=volume)

    @command(pass_context=True, aliases=['next'])
    async def skip(self, ctx: Context):
        """ Skip song """
        ctx.voice_client.stop()

    @command(pass_context=True, aliases=['leave'])
    async def stop(self, ctx: Context):
        """ stop playing music """
        ctx.voice_client.stop()
        self.stop = True
        self.is_playing = False
        self.in_queue = []

    @group(pass_context=True)
    async def queue(self, ctx: Context):
        """ Show queue """
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="In queue: ")
            embed.add_field(name=f"1. {self.current_song} - Now playing", inline=False, value=":metal:")
            key = 2
            for queue in self.in_queue:
                embed.add_field(name=f"{key}. {queue.title}", inline=False, value=":metal:")
                key += 1
            await ctx.send(embed=embed)

    @queue.command(pass_context=True)
    async def add(self, ctx: Context, name: str):
        """ Add song to queue """
        if len(self.in_queue) >= settings.QUEUE_LIMIT:
            return await ctx.send(embed=discord.Embed(title="Queue is full"))
        player = await YoutubeStream.from_url(name, loop=self.client.loop, stream=True)
        self.in_queue.append(player)
        embed = discord.Embed(title=f"Song {player.title} has been added to playlist")
        await ctx.send(embed=embed)

    @queue.command(pass_context=True)
    async def remove(self, ctx: Context, position: int):
        """ remove position form queue """
        index = position - 1 if position >= 0 else None
        message = ":neutral_face: Position not found"
        if index == 0 and index:
            message = "Cannot remove first element from queue"
        elif index and not index > len(self.in_queue):
            get_element = self.in_queue[index]
            self.in_queue.pop(index)
            message = f"Song {get_element.title} has been removed from queue"
        return await ctx.send(embed=discord.Embed(title=message))

    @play.before_invoke
    async def ensure_voice(self, ctx: Context):
        if ctx.voice_client is None:
            if ctx.author.voice:
                try:
                    channel = ctx.author.voice.channel
                    await channel.connect()
                except discord.errors.ClientException as error:
                    await self.send_to_admin(error=error)
            else:
                await ctx.send(embed=discord.Embed(title="You are not connected to a voice channel."))
                raise commands.CommandError("You are not connected to a voice channel.")

    @staticmethod
    async def volume_display(ctx: Context, volume: int):
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
