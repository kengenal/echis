import os
import discord

from discord.ext import commands
from discord.ext.commands import Context, command

from echis.utils import mixins
from echis.utils.Youtube import YoutubeStream


class MusicCog(mixins.BaseCog):

    @command()
    async def play(self, ctx: Context, *args: str):
        query = ' '.join(args)
        if query:
            async with ctx.typing():
                player = await YoutubeStream.from_url(query,
                                                      loop=self.client.loop, stream=True)
                ctx.voice_client.play(player,
                                      after=lambda e: print('Player _error: %s' % e))
                return await ctx.send(f"Now playing {player.title}")
        else:
            return await ctx.send(f"Take song name")

    @command()
    async def volume(self, ctx: Context, volume: int = None):
        """ Change volume  0 - 100 'volume 50' """
        name = os.getenv("BOT_NAME")
        if not volume:
            return await ctx.send(f"volume : {int(ctx.voice_client.source.volume * 100) / 100}")
        if ctx.voice_client is None:
            return await ctx.send(f"{name} is not connected")
        if volume > 100:
            volume = 100
        ctx.voice_client.source.volume = volume / 100
        return await ctx.send(f"Changed volume to {volume}/100")

    @command()
    async def stop(self, ctx: Context):
        await ctx.voice_client.disconnect()

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


def setup(client):
    client.add_cog(MusicCog(client))
