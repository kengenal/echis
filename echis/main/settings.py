import os

QUEUE_LIMIT = os.getenv("QUEUE_LIMIT", 1)
DEFAULT_VOLUME = os.getenv("DEFAULT_QUEUE", 0.5)
SHARE_DATE_SORTED = "-created_at"

COMMANDS = [
    "meme",
    "report",
    "music",
    "register",
    "share",
]

TASKS = [
    "share_task",
]
