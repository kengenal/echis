import discord
import sys

import configparser
from discord.ext import commands
from libs.Meme import Meme
from libs.config_loader import config

class MemeCog(commands.Cog, name="Memes"):
    def __init__(self, client):
        self.client = client
        self.config = config()

    @commands.command(pass_context=True)
    async def meme(self, ctx):
        chan  = ctx.message.channel.name
        channel_id = self.config["SETTINGS"]["meme"]
        url = self.config["URLS"]["reddit"]
        if str(chan) == str(channel_id):
            try:
                get = Meme(url)
                get.run()
                title = str(get.title)
                image = get.image

                embed = discord.Embed(title=title, color=discord.Color.dark_blue())
                embed.set_image(url=image)
                await ctx.send(embed=embed)
            except Exception as error:
                await ctx.send(f"Error : {error}")
  
  
def setup(client):
    client.add_cog(MemeCog(client))