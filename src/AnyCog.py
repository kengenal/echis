import discord
import sys

import configparser
from discord.ext import commands
from src.lib.config_loader import config
from discord.ext.commands import has_permissions

class AnyCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = config()

    @commands.command(pass_context=True)
    async def help(self, ctx):
        author = ctx.message.author
        embed = discord.Embed(colour=discord.Color.blue())
        embed.set_author(name="Help - Commands")
        for key in self.config["HELP"]:
            embed.add_field(name=f"!{key}", value=self.config["HELP"][key], inline=True)
        await ctx.send(author, embed=embed)

    @commands.command(pass_context=True)
    async def report(self, ctx, id:int = None, description: str = None):
        if id is not None and description is not None:
            description = str(description)
            author = ctx.message.author.name
            name = self.client.get_user(id)
            channel = self.config["SETTINGS"]["admin_channel"]
            embed = discord.Embed(olour=discord.Color.red())
            embed.set_author(name="Report")
            embed.add_field(name=f"User {author}: send report to {name} : {id}", 
                            value=description, inline=True
                        )
            await ctx.send("Report has been sended")
            chan = self.client.get_channel(int(channel))
            await chan.send(embed=embed)
        else:
            await ctx.send("The variabe can not be empty")

    @commands.command()
    @has_permissions(administrator=True)
    async def find(self, ctx, id:int):
        chan = ctx.message.channel.id
        channel_id = self.config["SETTINGS"]["admin_channel"]
        if int(chan) == int(channel_id):
            if id:
                name = self.client.get_user(id)
                await ctx.send(f"Name: {name}")
            else:
                await ctx.send("You are not server administrator")


def setup(client):
    client.add_cog(AnyCog(client))