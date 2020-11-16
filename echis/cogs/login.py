import posixpath
from urllib.parse import urljoin

from discord.ext.commands import command, Context

from echis.main import settings
from echis.modules import mixins
from echis.modules.token import create_token


class Login(mixins.BaseCog, name="Login"):
    @command(pass_context=True)
    async def login(self, ctx: Context):
        """ login to web interface """
        await ctx.message.delete()
        roles = "|".join([str(r.name) for r in ctx.guild.roles if r.name != "@everyone"])
        data = {
            "discord_id": ctx.author.id,
            "username": ctx.author.name,
            "permissions": roles,
            "avatar": str(ctx.author.avatar_url)
        }
        token = create_token(data=data)
        url = posixpath.join(settings.WEB, token)

        return await ctx.author.send(f"""
            Your link to login in web interface
            {url}
        """)


def setup(client):
    client.add_cog(Login(client))
