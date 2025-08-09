# config.py
# Configuration and credentials for DreamsMusic bot

import os

# Telegram API credentials (get from https://my.telegram.org)
API_ID = int(os.getenv("API_ID", "1234567"))
API_HASH = os.getenv("API_HASH", "your_api_hash_here")

# Telegram bot token from BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here")

# MongoDB connection string (for storing users, blacklists, etc.)
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "mongodb+srv://username:password@cluster0.mongodb.net/dbname?retryWrites=true&w=majority")

# Authorized user IDs (admins) separated by space in env variable
AUTH_USERS = list(set(int(x) for x in os.getenv("AUTH_USERS", "").split() if x.strip().isdigit()))

# Telegram channel ID to send logs (optional)
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1001234567890"))

# Max duration limit for songs (seconds)
DURATION_LIMIT = int(os.getenv("DURATION_LIMIT", "180"))

# Group call title (voice chat name)
GROUP_CALL = os.getenv("GROUP_CALL", "DreamsMusic VC")

# Default language ('en' for English, 'hi' for Hindi)
DEFAULT_LANG = os.getenv("DEFAULT_LANG", "en")

# Maintenance mode flag
MAINTENANCE_MODE = False

# Playback control setting: "everyone", "admins", or "owner"
PLAYBACK_CONTROL = os.getenv("PLAYBACK_CONTROL", "admins")
