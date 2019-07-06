import discord

from src.Main import DiscordMultiBot
from discord.ext.commands import Bot
from libs.config_loader import config

config = config()

extensions = ["src.MemeCog", "src.AnyCog", "src.MusicCog"]

BOT_PREFIX = "!"
TOKEN = config["TOKENS"]["discord"]
prefix = config["SETTINGS"]["prefix"]

if __name__ == "__main__":
    client = DiscordMultiBot(command_prefix=BOT_PREFIX)
    client.remove_command("help")
    for ext in extensions:
        try:
            client.load_extension(ext)
        except Exception as error:
            print(error)
    client.run(TOKEN)
