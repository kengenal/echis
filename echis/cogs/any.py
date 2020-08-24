import os

import discord

from discord.ext import commands

from echis.utils import mixins
from echis.utils.config import config
from discord.ext.commands import has_permissions


class AnyCog(mixins.BaseCog):
    @commands.command(pass_context=True)
    async def help(self, ctx):
        author = ctx.message.author
        embed = discord.Embed(colour=discord.Color.blue())
        embed.set_author(name="Help - Commands")
        conf = config()
        for key in conf["HELP"]:
            embed.add_field(name=f"!{key}", value=conf["HELP"][key], inline=True)
        await ctx.send(author, embed=embed)

    @commands.command(pass_context=True)
    async def report(self, ctx, id: int = None, description: str = None):
        if id is not None and description is not None:
            description = str(description)
            author = ctx.message.author.name
            name = self.client.get_user(id)
            channel = os.getenv("ADMIN_CHANNEL")
            chan = discord.utils.get(self.client.get_all_channels(), name=channel)
            embed = discord.Embed(olour=discord.Color.red())
            embed.set_author(name="Report")
            embed.add_field(name=f"User {author}: send report to {name} : {id}",
                            value=description, inline=True
                            )
            await ctx.send("Report has been sended")
            chan = self.client.get_channel(int(chan.id))
            await chan.send(embed=embed)
        else:
            await ctx.send("The variabe can not be empty")

    @commands.command()
    @has_permissions(administrator=True)
    async def find(self, ctx, id: int):
        chan = ctx.message.channel.name
        channel_name = os.getenv("ADMIN_CHANNEL")
        if str(chan) == str(channel_name):
            if id:
                name = self.client.get_user(id)
                await ctx.send(f"Name: {name}")
            else:
                await ctx.send("Admin channel not found")


def setup(client):
    client.add_cog(AnyCog(client))
