# config.py
# Bot & assistant configuration

import os

API_ID = int(os.getenv("API_ID", "1234567"))
API_HASH = os.getenv("API_HASH", "your_api_hash_here")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here")

# String session of assistant user (must be generated)
STRING_SESSION = os.getenv("STRING_SESSION", "")

MONGO_DB_URI = os.getenv("MONGO_DB_URI", "mongodb+srv://username:password@cluster0.mongodb.net/dbname?retryWrites=true&w=majority")

AUTH_USERS = list(set(int(x) for x in os.getenv("AUTH_USERS", "").split() if x.strip().isdigit()))

LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1001234567890"))

DURATION_LIMIT = int(os.getenv("DURATION_LIMIT", "180"))

GROUP_CALL = os.getenv("GROUP_CALL", "DreamsMusic VC")

DEFAULT_LANG = os.getenv("DEFAULT_LANG", "en")

MAINTENANCE_MODE = False

PLAYBACK_CONTROL = os.getenv("PLAYBACK_CONTROL", "admins")

# config.py or constants.py

STATS_IMAGE_URL = "https://i.imgur.com/YourStatsImage.png"

