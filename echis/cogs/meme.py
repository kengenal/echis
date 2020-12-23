import os

import discord

from discord.ext.commands import Context, command

from echis.main.settings import MEME_CHANNEL
from echis.modules import mixins
from echis.modules.meme import RedditMeme


class Meme(mixins.BaseCog, name="Meme"):
    @command(pass_context=True)
    async def meme(self, ctx: Context, what: str = None):
        """ send random meme from reddit, you can add parameter like !meme dark-meme """
        current_channel = ctx.message.channel.name
        channel_name = None
        if MEME_CHANNEL:
            channel_name = MEME_CHANNEL
        if str(current_channel) == str(channel_name):
            try:
                reddit = RedditMeme()
                get_meme = reddit.by_query(what) if what else reddit.random
                embed = discord.Embed(title=get_meme[0]["title"], color=discord.Color.dark_blue())
                embed.set_image(url=get_meme[0]["url"])
                await ctx.send(embed=embed)
            except Exception as error:
                await self.send_to_admin(error)


def setup(client):
    client.add_cog(Meme(client))
