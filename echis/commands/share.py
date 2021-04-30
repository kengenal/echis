import inspect

from echis.model.share import Playlists
from echis.modules import mixins
from discord.ext.commands import Context, group


class Share(mixins.BaseCog):
    @group(pass_context=True)
    async def share(self, ctx: Context):
        """ Share your playlist (DEEZER, SPOTIFY) """
        if ctx.invoked_subcommand is None:
            return await ctx.send("press !help for more information's")

    @share.group(pass_context=True)
    async def remove(self, ctx: Context, api: str, playlist_id: str):
        """ Stop sharing playlist on deezer, you need provide name of streaming playlist and playlist id """
        available_api = ["spotify", "deezer", "youtube"]
        if not api and not playlist_id and api not in available_api:
            return await ctx.send("provide name of your streaming platform and id of playlist")
        return await ctx.send(Playlists.remove_playlist(playlist_id=playlist_id, api=api, username=ctx.author.name))

    @share.group(pass_context=True)
    async def add(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            return await ctx.send("Missing streaming service, available is deezer, spotify and youtube")

    @add.command(pass_context=True)
    async def deezer(self, ctx: Context, playlist_id: str):
        if not playlist_id:
            return await ctx.send("Provide your playlist id")
        func_name = inspect.stack()[0][3]
        user = ctx.author.name
        return await ctx.send(self._add_playlist(api=func_name, playlist_id=playlist_id, username=user))

    @add.command(pass_context=True)
    async def spotify(self, ctx: Context, playlist_id: str):
        if not playlist_id:
            await ctx.send("Provide your playlist id")
        func_name = inspect.stack()[0][3]
        user = ctx.author.name
        return await ctx.send(self._add_playlist(api=func_name, playlist_id=playlist_id, username=user))

    @add.command(pass_context=True)
    async def youtube(self, ctx: Context, playlist_id: str):
        if not playlist_id:
            await ctx.send("Provide your playlist id")
        func_name = inspect.stack()[0][3]
        user = ctx.author.name
        return await ctx.send(self._add_playlist(api=func_name, playlist_id=playlist_id, username=user))

    @add.command(pass_context=True, aliases=["apple-music"])
    async def apple_music(self, ctx: Context, playlist_id: str):
        if not playlist_id:
            await ctx.send("Provide your playlist id")
        func_name = inspect.stack()[0][3]
        user = ctx.author.name
        return await ctx.send(self._add_playlist(api=func_name, playlist_id=playlist_id, username=user))

    def _add_playlist(self, api: str, playlist_id: str, username: str) -> str:
        try:
            return Playlists.add_playlist(api=api, playlist_id=playlist_id, username=username)
        except Exception as err:
            print(err)
            raise Exception("Api is unavailable")


def setup(client):
    client.add_cog(Share(client))
