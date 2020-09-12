import os
from typing import List

import discord
from discord.ext import tasks
from discord.utils import get

from echis import BotClient
from echis.model.share import SharedSongs
from echis.modules.mixins import BaseCog
from echis.modules.share_playlist import Share


class shareTask(BaseCog):
    def __init__(self, client: BotClient):
        super().__init__(client)
        self.share_task.start()

    def cog_unload(self):
        self.share_task.cancel()

    @tasks.loop(minutes=5.0)
    async def share_task(self):
        shared_channel = os.getenv("SHARED_CHANNEL")
        channel = get(self.client.get_all_channels(), name=shared_channel)
        try:
            song_list: List[Share] = SharedSongs.fetch_playlist()
            if song_list:
                for song in song_list:
                    embed = discord.Embed(
                        title=f"{song.artist} - {song.title}",
                        description=f'Album - "{song.album}"',
                        color=discord.Color.green(),
                    )
                    embed.set_author(name=f"Share by {song.added_by}")
                    embed.set_image(url=song.cover)
                    embed.set_footer(text=f"Rank on {song.api} - {song.rank}")
                    await channel.send(embed=embed)
        except Exception as error:
            await self.send_to_admin(error=error)

    @share_task.before_loop
    async def wait_for_bot(self):
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(shareTask(client))
