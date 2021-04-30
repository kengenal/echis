from discord.ext.commands import command, Context

from echis.model.filter_model import FilterModel
from echis.modules import mixins


class Filter(mixins.BaseCog, name="Filter"):
    @command(pass_context=True, aliases=["words-reload"])
    async def words_reload(self, ctx: Context):
        """ filter words"""
        FilterModel.generate_csv()
        return await ctx.send("List has been reloaded")


def setup(client):
    client.add_cog(Filter(client))
