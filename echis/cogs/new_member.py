import os

import discord
from discord.ext import commands
from discord.ext.commands import Context

from echis.utils import mixins


class NewMember(mixins.BaseCog):
    @commands.command(pass_context=True)
    async def register(self, ctx: Context):
        chan = ctx.message.channel.name
        if str(chan) == str(os.getenv("REGISTER_CHANNEL")):
            role = ctx.author.roles
            user = ctx.message.author
            check = list(filter(lambda x: x.name == os.getenv("REGISTER_ROLE"), role))
            if not check:
                await user.add_roles(discord.utils.get(user.guild.roles, name=os.getenv("REGISTER_ROLE")))
                await ctx.send("Register completed, have fun :nerd:")
            else:
                await ctx.send("You are already registered")
            await ctx.message.delete()


def setup(client):
    client.add_cog(NewMember(client))
