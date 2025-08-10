# main.py
# Main entry: runs both bot and assistant user (string session) clients and PyTgCalls

import logging
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import CallbackQuery
from pytgcalls import PyTgCalls

from config import *
from DreamsMusic.handlers import (
    start as start_handler,
    admin as admin_handler,
    play as play_handler,
    stats as stats_handler,
    auth as auth_handler,
    broadcast as broadcast_handler,
    extra as extra_handler,
    playlist
)
from DreamsMusic.utils import logger_util, language_util, maintenance_util
from DreamsMusic.handlers import (
    start,
    play,
    admin,
    auth,
    broadcast,
    extra,
    playlist,
    settings,
    stats
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize bot and assistant clients
app = Client(
    "DreamsMusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

assistant = Client(
    "assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,
)

pytgcalls = PyTgCalls(assistant)

maintenance_mode = MAINTENANCE_MODE
lang = language_util.load_language(DEFAULT_LANG)


# Register handlers

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    await start_handler.start(client, message, lang)


@app.on_message(filters.command(["pause", "resume", "stop", "skip", "end"]) & filters.user(AUTH_USERS))
async def admin_cmd(client, message):
    await admin_handler.handle_commands(client, message, lang)


@app.on_message(filters.command("play"))
async def play_cmd(client, message):
    await play_handler.play(client, message, lang, pytgcalls, assistant)


@app.on_message(filters.command("stats") & filters.user(AUTH_USERS))
async def stats_cmd(client, message):
    await stats_handler.stats(client, message, lang)


@app.on_callback_query(filters.regex(r"stats_(general|overall|close)"))
async def stats_callback(client: Client, callback_query: CallbackQuery):
    await stats_handler.stats_button_handler(client, callback_query)


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


@app.on_message(filters.command(["maintenance"]) & filters.user(AUTH_USERS))
async def maintenance_cmd2(client, message):
    # This was duplicated - can be removed or kept if different logic needed
    await maintenance_util.maintenance_toggle(client, message)


@app.on_message(filters.command(["logs"]) & filters.user(AUTH_USERS))
async def logs_cmd(client, message):
    await logger_util.logger_toggle(client, message)


# Playlist Handlers

@app.on_message(filters.command("playlist") & filters.private)
async def playlist_cmd(client, message):
    await playlist.playlist_cmd(client, message)


@app.on_callback_query(filters.regex(r"playlist_"))
async def playlist_cb(client, callback_query):
    await playlist.playlist_cb_handler(client, callback_query)


# Add song flow handler
@app.on_message(filters.private)
async def handle_add_song_flow(client, message):
    user_id = message.from_user.id
    if hasattr(playlist, "user_adding_song") and user_id in playlist.user_adding_song and playlist.user_adding_song[user_id]:
        text = message.text
        if "-" not in text:
            await message.reply("Invalid format! Send as: `Song Name - Song Link`", parse_mode="markdown")
            return
        song_name, song_link = map(str.strip, text.split("-", 1))
        if not song_name or not song_link:
            await message.reply("Both name and link are required.")
            return

        # Call playlist's function to add song (you should implement this inside playlist.py)
        await playlist.add_song_to_playlist(user_id, song_name, song_link)

        playlist.user_adding_song[user_id] = False
        await message.reply(f"✅ Added **{song_name}** to your playlist.")


async def main():
    """Main execution flow"""
    logger.info("Starting DreamsMusic...")
    
    try:
        await assistant.start()
        logger.info("Assistant started")
        
        await pytgcalls.start()
        logger.info("PyTgCalls started")
        
        logger.info("DreamsMusic is running...")
        await idle()
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
    finally:
        # Cleanup
        if pytgcalls.is_running:
            await pytgcalls.stop()
        await assistant.stop()

if __name__ == "__main__":
    app.run()
