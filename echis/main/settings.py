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
    "login",
]

TASKS = [
    "share_task",
]

TOKEN_SECRET = os.getenv("TOKEN_SECRET", default="7xdhbjn!silr%7mk_694^gufxry-m*!kif!4+e%x6haf2$#p+o")
TOKEN_ALGORITHM = os.getenv("TOKEN_ALGORITHM", default="HS512")
EXP = os.getenv("EXP", default=4)
WEB = os.getenv("WEB", default="http://localhost:8000/auth")
