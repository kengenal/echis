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
MONGO_URL = os.getenv("MONGO_URL")

PREFIX = os.getenv("PREFIX", "!")
BOT_NAME = os.getenv("BOT_NAME", "Echis")

# API URLS
REDDIT = "https://www.reddit.com/r/memes/random.json"

# API VARIABLES
SPOTIFY_LIMIT = 1
SPOTIFY_MARKET = os.getenv("SPOTIFY_MARKET", "PL")

# API SECRET
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# CHANNELS
ADMIN_CHANNEL = "admin"
MEME_CHANNEL = "meme"
REGISTER_ROLE = "registered"
REGISTER_CHANNEL = "start"
SHARED_CHANNEL = "share"


