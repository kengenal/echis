import os
import sys

from echis.main import settings
from echis.main.main import BotClient
from echis.modules.mongo import mongo_init


def load_commands(client: BotClient, module_name: str):
    for ext in settings.COMMANDS:
        try:
            client.load_extension(f"{module_name}.commands.{ext}")
        except Exception as error:
            print(error)


def load_tasks(client: BotClient, module_name: str):
    for ext in settings.TASKS:
        try:
            client.load_extension(f"{module_name}.tasks.{ext}")
        except Exception as error:
            print(error)


def start_bot():
    TOKEN = settings.TOKEN
    MODULE_NAME = __name__
    BOT_PREFIX = settings.PREFIX

    if not TOKEN or not BOT_PREFIX:
        sys.exit("Token not found")
    client = BotClient(command_prefix=BOT_PREFIX)
    if os.getenv("MONGO_URL"):
        mongo_init()
    load_commands(client=client, module_name=MODULE_NAME)
    load_tasks(client=client, module_name=MODULE_NAME)
    client.run(TOKEN)
