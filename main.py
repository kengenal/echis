import discord
import unittest

from src.MainCog import DiscordMultiBot
from discord.ext.commands import Bot
from utils.config import config
from utils.cli import cli, run, plugins

config = config()

extensions = ["src.MemeCog", "src.AnyCog", "src.MusicCog"]

BOT_PREFIX = "!"
TOKEN = config["TOKENS"]["discord"]
prefix = config["SETTINGS"]["prefix"]


def register_extensions():
    return [
        "src.MemeCog",
        "src.AnyCog",
        "src.MusicCog"
    ]


def start_bot():
    ext = register_extensions()
    client = DiscordMultiBot(command_prefix=BOT_PREFIX)
    client.remove_command("help")
    for ext in extensions:
        try:
            client.load_extension(ext)
        except Exception as error:
            print(error)
    client.run(TOKEN)


@cli(desc="serve discord bot")
def serve():
    start_bot()


@cli(desc="Run unittest")
def tests():
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir)
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == "__main__":
    run(plugins)
