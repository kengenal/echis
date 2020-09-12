import os
from abc import ABC

import discord

from discord.ext import commands
from echis import BotClient


class BaseCog(commands.Cog):
    def __init__(self, client: BotClient):
        self.client = client

    async def send_to_admin(self, error: Exception):
        admin = os.getenv("ADMIN_CHANNEL")
        channel = discord.utils.get(self.client.get_all_channels(), name=admin)
        await channel.send(f'Error : {error}')
