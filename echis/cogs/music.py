import os

from discord.ext import commands
from discord.ext.commands import Context

from echis.utils import mixins
from echis.utils.Youtube import YoutubeStream


class MusicCog(mixins.BaseCog):

    @commands.command()
    async def play(self, ctx: Context, query: str):
        if query:
            async with ctx.typing():
                pl = await YoutubeStream.from_url(query, loop=self.client.loop, stream=True)
                ctx.voice_client.play(pl, after=lambda e: print('Player _error: %s' % e) if e else None)
            await ctx.send(f"Now playing{pl.title}")

        else:
            await ctx.send(f"Take song name")

    @commands.command()
    async def volume(self, ctx: Context, volume: int):
        name = os.getenv("BOT_NAME")
        if ctx.voice_client is None:
            return await ctx.send(f"{name} is not connected")
        if volume > 1000:
            volume = 1000
        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}")

    @commands.command()
    async def stop(self, ctx: Context):
        await ctx.voice_client.disconnect()


def setup(client):
    client.add_cog(MusicCog(client))
