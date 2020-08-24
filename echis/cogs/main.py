import os

import discord
from discord import Message
from discord.ext import commands
from discord.ext.commands import Context, CommandNotFound

from echis.utils.filter import is_bad_word


class BotClient(commands.Bot):
    async def on_ready(self):
        print("---- BOT IS READY ----")
        await self.change_presence(status=discord.Status.online, activity=discord.Game(f"{self.command_prefix}help"))

    async def on_message(self, message: Message):
        messages = message.content.split(" ")
        path = os.path.abspath("./echis/csv/bad_words.csv")
        for mes in messages:
            is_bad = is_bad_word(mes, path=path)
            if is_bad:
                await message.delete()
                await message.channel.send("Dont't say that")
        await self.process_commands(message)

    async def on_command_error(self, ctx: Context, exception: CommandNotFound):
        await ctx.send("Don't do that")
