# main.py
# Main entry: runs both bot and assistant user (string session) clients and PyTgCalls

import logging
import asyncio
import signal
import sys
from pyrogram import Client, filters, idle
from pyrogram.types import CallbackQuery
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.stream import StreamAudioEnded

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

# Add file handler for logging
file_handler = logging.FileHandler("bot.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Initialize clients
class DreamsMusicBot:
    def __init__(self):
        self.assistant = None
        self.app = None
        self.pytgcalls = None
        self.maintenance_mode = MAINTENANCE_MODE
        self.lang = language_util.load_language(DEFAULT_LANG)
        
    async def initialize(self):
        """Initialize clients asynchronously"""
        # Initialize the assistant first
        self.assistant = Client(
            "assistant",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=STRING_SESSION,
            no_updates=False,
            in_memory=True
        )
        
        # Initialize the main bot
        self.app = Client(
            "DreamsMusicBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            in_memory=True
        )
        
        # Initialize PyTgCalls with the assistant
        self.pytgcalls = PyTgCalls(self.assistant)
        
        # Set up PyTgCalls event handlers
        @self.pytgcalls.on_stream_end()
        async def on_stream_end(_, update: Update):
            if isinstance(update, StreamAudioEnded):
                chat_id = update.chat_id
                # Handle stream end - you can implement your logic here
                logger.info(f"Stream ended in chat {chat_id}")

# Create bot instance
bot = DreamsMusicBot()

# Make instances available at module level
assistant = None
app = None
pytgcalls = None
maintenance_mode = bot.maintenance_mode
lang = bot.lang

async def init_clients():
    """Initialize all clients"""
    global assistant, app, pytgcalls
    await bot.initialize()
    assistant = bot.assistant
    app = bot.app
    pytgcalls = bot.pytgcalls


# All handlers will be registered after client initialization
def register_handlers(client):
    """Register all message and callback handlers"""
    
    # Basic commands
    @client.on_message(filters.command("start") & filters.private)
    async def start_cmd(client, message):
        await start_handler.start(client, message, lang)

    @client.on_message(filters.command(["pause", "resume", "stop", "skip", "end"]) & filters.user(AUTH_USERS))
    async def admin_cmd(client, message):
        await admin_handler.handle_commands(client, message, lang)
        
    @client.on_message(filters.command("play"))
    async def play_cmd(client, message):
        await play_handler.play(client, message, lang, pytgcalls, assistant)
        
    @client.on_message(filters.command("stats") & filters.user(AUTH_USERS))
    async def stats_cmd(client, message):
        await stats_handler.stats(client, message, lang)
        
    @client.on_callback_query(filters.regex(r"stats_(general|overall|close)"))
    async def stats_callback(client: Client, callback_query: CallbackQuery):
        await stats_handler.stats_button_handler(client, callback_query)

    # Maintenance commands
    @client.on_message(filters.command(["maintenance", "unmaintenance"]) & filters.user(AUTH_USERS))
    async def maintenance_cmd(client, message):
        global maintenance_mode
        await maintenance_util.maintenance_toggle(client, message)
        maintenance_mode = maintenance_util.is_maintenance()

    # Chat events
    @client.on_message(filters.new_chat_members)
    async def welcome_new(client, message):
        await extra_handler.welcome(client, message, lang)

    # Logging commands
    @client.on_message(filters.command("logger") & filters.user(AUTH_USERS))
    async def logger_cmd(client, message):
        await logger_util.logger_toggle(client, message)

    @client.on_message(filters.command(["logs"]) & filters.user(AUTH_USERS))
    async def logs_cmd(client, message):
        await logger_util.logger_toggle(client, message)

    # Playlist handlers
    @client.on_message(filters.command("playlist") & filters.private)
    async def playlist_cmd(client, message):
        await playlist.playlist_cmd(client, message)

    @client.on_callback_query(filters.regex(r"playlist_"))
    async def playlist_cb(client, callback_query):
        await playlist.playlist_cb_handler(client, callback_query)

    # Add song flow handler
    @client.on_message(filters.private)
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

            await playlist.add_song_to_playlist(user_id, song_name, song_link)
            playlist.user_adding_song[user_id] = False
            await message.reply(f"✅ Added **{song_name}** to your playlist.")


async def shutdown():
    """Cleanup before shutdown"""
    logger.info("Shutting down...")
    
    try:
        # Cancel all pending tasks except current
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        if tasks:
            logger.info(f"Cancelling {len(tasks)} pending tasks...")
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            
        if bot.pytgcalls:
            # Stop all active calls first
            logger.info("Stopping active calls...")
            try:
                if hasattr(bot.pytgcalls, 'active_calls'):
                    for chat_id in bot.pytgcalls.active_calls:
                        try:
                            await bot.pytgcalls.leave_group_call(chat_id)
                        except Exception as e:
                            logger.error(f"Error leaving call in {chat_id}: {str(e)}")
                logger.info("All active calls stopped!")
            except Exception as e:
                logger.error(f"Error stopping calls: {str(e)}")
        
        if bot.app:
            # Stop main bot first
            logger.info("Stopping main bot...")
            try:
                await bot.app.stop()
                logger.info("Bot stopped successfully!")
            except Exception as e:
                logger.error(f"Error stopping main bot: {str(e)}")
        
        if bot.assistant:
            # Stop assistant next
            logger.info("Stopping assistant...")
            try:
                await bot.assistant.stop()
                logger.info("Assistant stopped successfully!")
            except Exception as e:
                logger.error(f"Error stopping assistant: {str(e)}")
        
        # PyTgCalls cleanup happens automatically with the assistant
        logger.info("Shutdown complete!")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")
    finally:
        try:
            # Get event loop but don't create a new one if it doesn't exist
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                return
            
            # Cancel any remaining tasks
            pending = asyncio.all_tasks(loop=loop)
            for task in pending:
                task.cancel()
            
            # Wait for tasks to cancel
            if pending:
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        except Exception as e:
            logger.error(f"Error in final cleanup: {str(e)}")
        finally:
            sys.exit(0)

async def start_bot():
    """Start the bot and its components"""
    logger.info("Starting DreamsMusic...")
    
    try:
        # Initialize all clients first
        await init_clients()
        
        # Start assistant first
        logger.info("Starting assistant...")
        await bot.assistant.start()
        me_assistant = await bot.assistant.get_me()
        logger.info(f"Assistant started successfully! Name: {me_assistant.first_name}")
        
        # Start the main bot
        logger.info("Starting main bot...")
        await bot.app.start()
        me_bot = await bot.app.get_me()
        logger.info(f"Bot started successfully! Name: {me_bot.first_name}")
        
        # Initialize and start PyTgCalls last
        logger.info("Starting PyTgCalls...")
        await bot.pytgcalls.start()
        logger.info("PyTgCalls started successfully!")
        
        # Make assistant and pytgcalls available to handlers
        bot.app.assistant = bot.assistant
        bot.app.pytgcalls = bot.pytgcalls
        
        # Register all handlers now that clients are initialized
        logger.info("Registering message handlers...")
        register_handlers(bot.app)
        
        logger.info("DreamsMusic is fully operational! 🎵")
        return True
        
    except Exception as e:
        logger.error(f"Error starting bot: {str(e)}")
        return False

async def main():
    """Main execution flow"""
    try:
        if not await start_bot():
            return
        
        # Set up signal handlers
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, lambda s, f: asyncio.create_task(shutdown()))
        
        # Wait for termination
        await idle()
        
    except (asyncio.CancelledError, KeyboardInterrupt):
        logger.info("Received shutdown signal...")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise
    finally:
        await shutdown()

if __name__ == "__main__":
    # Run with proper event loop management
    asyncio.run(main())
