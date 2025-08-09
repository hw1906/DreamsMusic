# main.py
# Main entry: runs both bot and assistant user (string session) clients and PyTgCalls

import logging
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from config import *
from handlers import (
    start_handler,
    admin_handler,
    play_handler,
    stats_handler,
    auth_handler,
    broadcast_handler,
    extra_handler,
)
from utils import logger_util, language_util, maintenance_util


# maintenance command
@app.on_message(filters.command(["maintenance"]) & filters.user(AUTH_USERS))
async def maintenance_cmd(client, message):
    await maintenance_util.maintenance_toggle(client, message)
# Logger command
@app.on_message(filters.command(["logs"]) & filters.user(AUTH_USERS))
async def logs_cmd(client, message):
    await logger_util.logger_toggle(client, message)
    
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot client using bot token
app = Client(
    "DreamsMusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# Assistant user client using string session (must be a user account string session)
assistant = Client(
    "assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,
)

# PyTgCalls runs on the assistant user client
pytgcalls = PyTgCalls(assistant)

maintenance_mode = MAINTENANCE_MODE
lang = language_util.load_language(DEFAULT_LANG)

# Event handlers

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    await start_handler.start(client, message, lang)

@app.on_message(filters.command(["pause", "resume", "stop", "skip", "end"]) & filters.user(AUTH_USERS))
async def admin_cmd(client, message):
    await admin_handler.handle_commands(client, message, lang)

@app.on_message(filters.command("play") & filters.private)
async def play_cmd(client, message):
    await play_handler.play(client, message, lang, pytgcalls, assistant)

@app.on_message(filters.command("stats") & filters.user(AUTH_USERS))
async def stats_cmd(client, message):
    await stats_handler.stats(client, message, lang)

@app.on_message(filters.command(["maintenance", "unmaintenance"]) & filters.user(AUTH_USERS))
async def maintenance_cmd(client, message):
    global maintenance_mode
    await maintenance_util.maintenance_toggle(client, message)
    maintenance_mode = maintenance_util.is_maintenance()

@app.on_message(filters.new_chat_members)
async def welcome_new(client, message):
    await extra_handler.welcome(client, message, lang)

@app.on_message(filters.command("logger") & filters.user(AUTH_USERS))
async def logger_cmd(client, message):
    await logger_util.logger_toggle(client, message)

async def start_clients():
    await app.start()
    logger.info("Bot client started.")

    await assistant.start()
    logger.info("Assistant client started.")

    await pytgcalls.start()
    logger.info("PyTgCalls started on assistant client.")

from pyrogram import idle
import asyncio

async def main():
    await start_clients()
    logger.info("DreamsMusic is running...")
    await idle()
    await app.stop()
    await assistant.stop()

if __name__ == "__main__":
    asyncio.run(main())
