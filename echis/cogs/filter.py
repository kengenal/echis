import posixpath

from discord.ext.commands import command, Context

from echis.main import settings
from echis.modules import mixins


class Filter(mixins.BaseCog, name="Filter"):
    @command(pass_context=True)
    async def reload(self, ctx: Context):
        """ filter words"""
        path = settings.FILTER


def setup(client):
    client.add_cog(Filter(client))
