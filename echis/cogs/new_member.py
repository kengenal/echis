import os

from discord.ext.commands import Context, command
from discord.utils import get

from echis.utils import mixins


class NewMember(mixins.BaseCog):
    @command(pass_context=True)
    async def register(self, ctx: Context):
        """ set register for new user """
        chan = ctx.message.channel.name
        if str(chan) == str(os.getenv("REGISTER_CHANNEL")):
            role = ctx.author.roles
            user = ctx.author
            check = list(filter(lambda x: x.name == os.getenv("REGISTER_ROLE"), role))
            if not check:
                await user.add_roles(get(user.guild.roles, name=os.getenv("REGISTER_ROLE")))
                await ctx.send("Register completed, have fun :nerd:")
            else:
                await ctx.send("You are already registered")
            await ctx.message.delete()


def setup(client):
    client.add_cog(NewMember(client))
