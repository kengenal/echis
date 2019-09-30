import discord

from discord.ext import commands
from utils.config import config
from utils.meme import NineGag, RedditMeme


class MemeCog(commands.Cog, name="Memes"):
    def __init__(self, client):
        self.client = client
        self.config = config()

    @commands.command(pass_context=True)
    async def reddit(self, ctx, what: str = None):
        chan = ctx.message.channel.name
        reddit = RedditMeme()
        if what is not None:
            data = reddit.query(query=what, limit=1)
        else:
            data = reddit.random(limit=1)
        channel_name = None
        if self.config.has_option("SETTINGS", "meme"):
            channel_name = self.config["SETTINGS"]["meme"]
        if str(chan) == str(channel_name):
            try:
                embed = discord.Embed(title=data[0]["title"], color=discord.Color.dark_blue())
                embed.set_image(url=data[0]["url"])
                await ctx.send(embed=embed)
            except Exception as error:
                admin = self.config["SETTINGS"]['admin_channel']
                channel = self.client.get_channel(int(admin))
                await channel.send(f'Error : {error}')

    @commands.command(pass_context=True)
    async def nine(self, ctx):
        chan = ctx.channel.name
        channel_name = None
        if self.config.has_option("SETTINGS", "meme"):
            channel_name = self.config["SETTINGS"]["meme"]
        if str(chan) == str(channel_name):
            try:
                nine = NineGag()
                data = nine.random()
                embed = discord.Embed(title=data['title'], color=discord.Color.dark_blue())
                if data['type'] == "img":
                    embed.set_image(data["url"])
                else:
                    embed.add_field(value=data["url"], name="ninegag")
                await ctx.send(embed=embed)
            except Exception as error:
                admin = self.config["SETTINGS"]['admin_channel']
                channel = self.client.get_channel(int(admin))
                await channel.send(f'Error : {error}')


def setup(client):
    client.add_cog(MemeCog(client))
