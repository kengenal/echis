import os
import sys
from typing import List

from echis.main.main import BotClient


def get_extensions() -> List[str]:
    return [
        "meme",
        "report",
        "music",
        "new_member",
    ]


def start_bot():
    TOKEN = os.getenv("TOKEN")
    MODULE_NAME = __name__
    BOT_PREFIX = os.getenv("PREFIX")

    if not TOKEN or not BOT_PREFIX:
        sys.exit("Token not found")
    client = BotClient(command_prefix=BOT_PREFIX)
    # client.remove_command("help")
    for ext in get_extensions():
        try:
            client.load_extension(f"{MODULE_NAME}.cogs.{ext}")
        except Exception as error:
            print(error)
    client.run(TOKEN)
