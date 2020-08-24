import os

import discord

from discord.ext import commands
from discord.ext.commands import Context

from echis.utils import mixins
from echis.utils.meme import RedditMeme


class MemeCog(mixins.BaseCog, name="Memes"):
    @commands.command(pass_context=True)
    async def meme(self, ctx: Context, what: str = None):
        chan = ctx.message.channel.name
        reddit = RedditMeme()
        if what is not None:
            data = reddit.query(query=what, limit=1)
        else:
            data = reddit.random(limit=1)
        channel_name = None
        if os.getenv("MEME"):
            channel_name = os.getenv("MEME")
        if str(chan) == str(channel_name):
            try:
                embed = discord.Embed(title=data[0]["title"], color=discord.Color.dark_blue())
                embed.set_image(url=data[0]["url"])
                await ctx.send(embed=embed)
            except Exception as error:
                await self.send_to_admin(error)


def setup(client):
    client.add_cog(MemeCog(client))
