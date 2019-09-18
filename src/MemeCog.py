import discord
import sys

import configparser
from discord.ext import commands
from utils.reddit import Meme
from utils.config import config
from utils.nine_gag import NineGag

class MemeCog(commands.Cog, name="Memes"):
    def __init__(self, client):
        self.client = client
        self.config = config()

    @commands.command(pass_context=True)
    async def reddit(self, ctx):
        chan = ctx.message.channel.name
        if self.config.has_option("URLS", "reddit"):
            url = self.config["URLS"]["reddit"]

            get = Meme(url)
            get.run()
            title = str(get.title)
            image = get.image
            channel_name = None

            if self.config.has_option("SETTINGS", "meme"):
                channel_name = self.config["SETTINGS"]["meme"]
            if str(chan) == str(channel_name):
                try:
                    embed = discord.Embed(title=title, color=discord.Color.dark_blue())
                    embed.set_image(url=image)
                    await ctx.send(embed=embed)
                except Exception as error:
                    await ctx.send(f"Error : {error}")
            elif channel_name is None:
                try:
                    embed = discord.Embed(title=title, color=discord.Color.dark_blue())
                    embed.set_image(url=image)
                    await ctx.send(embed=embed)
                except Exception as error:
                    await ctx.send(f"Error : {error}")

    @commands.command(pass_context=True)
    async def nine(self, ctx, what:str="hot", range_meme:int=1):
        if range_meme < 10:
            range_meme = 10
        if range_meme > 1:
            range_meme = 1
        gag = {}
        nine = NineGag()
        if what == "fresh":
            gag = nine.fresh(range_meme)
        elif what == "hot":
            gag = nine.hot(range_meme)
        elif what == "dark":
            gag = nine.dark_hot(range_meme)
        elif what == "dark_fresh":
            gag = nine.dark_fresh(range_meme)
        elif what == "poland":
            gag = nine.poland_hot(range_meme)
        elif what == "poland_fresh":
            gag = nine.poland_fresh(range_meme)
        elif what == "random":
            gag = nine.random()

        for val in gag:
            try:
                embed = discord.Embed(title=val["title"], color=discord.Color.dark_blue())
                embed.set_image(url=val["url"])
                await ctx.send(embed=embed)
                print(val["url"])

            except Exception as error:
                await ctx.send(f"Error : {error}")


def setup(client):
    client.add_cog(MemeCog(client))
