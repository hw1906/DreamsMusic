# handlers/play.py
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from utils import maintenance_util
from utils import yt_utils
from core import player

from pyrogram.errors import FloodWait
import asyncio

# Global dictionary to store playing messages for editing seekbar later
playing_messages = {}


MAINTENANCE_IMAGE_URL = "https://i.imgur.com/ZzqV1XY.png"  # Replace with your maintenance image URL

async def play(client, message: Message, lang, pytgcalls, assistant):
    if maintenance_util.is_maintenance():
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🛠 Support Group", url="https://t.me/CloseFriendsCommunity"),
                InlineKeyboardButton("📢 Update Channel", url="https://t.me/CFCBots")
            ]
        ])
        await message.reply_photo(
            photo=MAINTENANCE_IMAGE_URL,
            caption="**Maintenance mode is enabled please check support group.**",
            reply_markup=buttons,
            parse_mode="markdown"
        )
        return

    # Your existing play logic here (search + play)

async def play(client, message: Message, lang, pytgcalls, assistant):
    query = " ".join(message.text.split()[1:])
    if not query:
        await message.reply(lang["no_query"])
        return

    # Search YouTube via yt-dlp (no API)
    try:
        video = yt_utils.yt_search(query)
    except Exception as e:
        await message.reply(f"Error finding video: {e}")
        return

    title = video['title']
    audio_url = video['url']
    webpage_url = video['webpage_url']
    duration = video['duration']
    thumbnail_url = video['thumbnail']

    # Download and blur thumbnail (30% blur ~ radius=10)
    thumb_file = yt_utils.download_and_blur_thumbnail(thumbnail_url)

    # Play audio in voice chat using PyTgCalls and assistant client
    # (You need to implement player.play logic with PyTgCalls to stream audio_url)
    await player.player_instance.play(message.chat.id, audio_url)

    # Build inline keyboard with symbols (pause, resume, skip, end)
    buttons = [
        [
            InlineKeyboardButton("⏸", callback_data="pause"),
            InlineKeyboardButton("▶️", callback_data="resume"),
            InlineKeyboardButton("⏭️", callback_data="skip"),
            InlineKeyboardButton("⏹️", callback_data="end"),
        ],
        # Seekbar row (just placeholder text)
        [InlineKeyboardButton("🔴─────────────", callback_data="seekbar")],
        # Close button
        [InlineKeyboardButton("❌ Close", callback_data="close_panel")]
    ]

    # Send the control panel with blurred thumbnail as photo
    control_message = await message.reply_photo(
        photo=thumb_file,
        caption=f"**Now Playing:** [{title}]({webpage_url})\nDuration: {duration // 60}:{duration % 60:02d}",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="markdown"
    )

    # Save the message id to update seekbar later
    playing_messages[message.chat.id] = control_message.message_id

    # Start background task to update seekbar
    asyncio.create_task(update_seekbar(client, message.chat.id, duration))

async def update_seekbar(client, chat_id, total_duration):
    # This function edits the seekbar every few seconds (simulate playback)
    current_time = 0
    while current_time <= total_duration:
        if chat_id not in playing_messages:
            break

        # Calculate seekbar progress (length 15 units)
        progress_units = int((current_time / total_duration) * 15)
        seekbar = "🔴" + "─" * progress_units + "○" + "─" * (15 - progress_units)

        # Build updated buttons with new seekbar
        buttons = [
            [
                InlineKeyboardButton("⏸", callback_data="pause"),
                InlineKeyboardButton("▶️", callback_data="resume"),
                InlineKeyboardButton("⏭️", callback_data="skip"),
                InlineKeyboardButton("⏹️", callback_data="end"),
            ],
            [InlineKeyboardButton(seekbar, callback_data="seekbar")],
            [InlineKeyboardButton("❌ Close", callback_data="close_panel")]
        ]

        # Edit the control panel message inline keyboard
        try:
            await client.edit_message_reply_markup(
                chat_id,
                playing_messages[chat_id],
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception:
            break  # Message deleted or no permission

        await asyncio.sleep(5)
        current_time += 5

# Add callback query handlers for the control buttons in your main.py or a handler file:

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from core import player

@Client.on_callback_query(filters.regex("pause|resume|skip|end|close_panel"))
async def control_buttons(client: Client, callback_query: CallbackQuery):
    cmd = callback_query.data

    if cmd == "pause":
        await player.player_instance.pause()
        await callback_query.answer("Paused ▶️")

    elif cmd == "resume":
        await player.player_instance.resume()
        await callback_query.answer("Resumed ⏸️")

    elif cmd == "skip":
        await player.player_instance.skip()
        await callback_query.answer("Skipped ⏭️")

    elif cmd == "end":
        await player.player_instance.stop()
        await callback_query.answer("Playback Ended ⏹️")

    elif cmd == "close_panel":
        chat_id = callback_query.message.chat.id
        if chat_id in playing_messages:
            try:
                await callback_query.message.delete()
            except:
                pass
            del playing_messages[chat_id]
        await callback_query.answer("Closed ❌")

