import discord
from discord.ext import commands
from discord.ext.commands import Bot
from src.lib.config_loader import config

class DiscordMultiBot(commands.Bot):

    async def on_ready(self):
        print("Bot is running")
    
    async def on_member_join(self, ctx, member):
        cfg = config()
        name = cfg["SETTINGS"]["bot_name"]
        self.client.say(""" 
            Hello, my name is {}, if you wont all commands enter !help command
        """.format(name))
        role = discord.utils.get(member.server.role, name='DICORD_ROLE')
        await client.add_roles(member, role)

