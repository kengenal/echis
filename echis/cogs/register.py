import inspect
import os

from discord.ext.commands import Context, group
from discord.utils import get

from echis.main.settings import REGISTER_CHANNEL
from echis.modules import mixins


class Register(mixins.BaseCog):
    @group(pass_context=True)
    async def register(self, ctx: Context):
        """ set register for new user """
        if ctx.invoked_subcommand is None:
            func_name = inspect.stack()[0][3]
            return await self._add_role(ctx=ctx, role_name=func_name)

    @register.command(pass_context=True)
    async def share(self, ctx: Context):
        """ Register and get share music """
        func_name = inspect.stack()[0][3]
        return await self._add_role(ctx=ctx, role_name=func_name)

    async def _add_role(self, ctx: Context, role_name: str):
        """ function check and add role if user don't have it """
        channel = ctx.message.channel.name
        if str(channel) == str(REGISTER_CHANNEL):
            role = ctx.author.roles
            user = ctx.author
            check = list(filter(lambda x: x.name == role_name, role))
            if not check:
                await user.add_roles(get(user.guild.roles, name=role_name))
                return await ctx.send("Register completed, have fun :nerd:")
            else:
                await ctx.send("You are already registered")
            return await ctx.message.delete()


def setup(client):
    client.add_cog(Register(client))
