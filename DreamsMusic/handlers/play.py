# handlers/play.py

import asyncio
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils import maintenance_util, logger_util, yt_utils
from core import player

# Global dictionary to track control panel message IDs by chat for updating seekbar
playing_messages = {}

MAINTENANCE_IMAGE_URL = "https://i.imgur.com/ZzqV1XY.png"  # Replace with your maintenance image URL
LOG_CHANNEL = -1001234567890  # Replace with your actual log channel ID

async def play(client, message: Message, lang, pytgcalls, assistant):
    # Maintenance mode check
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

    # Extract query
    query = " ".join(message.text.split()[1:])
    if not query:
        await message.reply(lang.get("no_query", "Please provide a song name or link to play."))
        return

    # YouTube search (yt-dlp)
    try:
        video = yt_utils.yt_search(query)
    except Exception as e:
        await message.reply(f"❌ Error finding video: {e}")
        return

    title = video['title']
    audio_url = video['url']
    webpage_url = video['webpage_url']
    duration = video['duration']
    thumbnail_url = video['thumbnail']

    # Download and blur thumbnail (~30% blur)
    thumb_file = yt_utils.download_and_blur_thumbnail(thumbnail_url)

    # Play audio in voice chat (implement in your player module)
    await player.player_instance.play(message.chat.id, audio_url)

    # Send log if logging enabled
    await logger_util.send_log(client, LOG_CHANNEL, message.chat, message.from_user, title, duration)

    # Inline control panel buttons (pause, resume, skip, end)
    buttons = [
        [
            InlineKeyboardButton("⏸", callback_data="pause"),
            InlineKeyboardButton("▶️", callback_data="resume"),
            InlineKeyboardButton("⏭️", callback_data="skip"),
            InlineKeyboardButton("⏹️", callback_data="end"),
        ],
        [InlineKeyboardButton("🔴─────────────", callback_data="seekbar")],  # Seekbar placeholder
        [InlineKeyboardButton("❌ Close", callback_data="close_panel")]
    ]

    # Send control panel message with blurred thumbnail
    control_message = await message.reply_photo(
        photo=thumb_file,
        caption=f"**Now Playing:** [{title}]({webpage_url})\nDuration: {duration // 60}:{duration % 60:02d}",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="markdown"
    )

    # Save message ID to update seekbar
    playing_messages[message.chat.id] = control_message.message_id

    # Start background task to update seekbar progress
    asyncio.create_task(update_seekbar(client, message.chat.id, duration))


async def update_seekbar(client, chat_id, total_duration):
    current_time = 0
    while current_time <= total_duration:
        if chat_id not in playing_messages:
            break

        progress_units = int((current_time / total_duration) * 15)
        seekbar = "🔴" + "─" * progress_units + "○" + "─" * (15 - progress_units)

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

        try:
            await client.edit_message_reply_markup(
                chat_id,
                playing_messages[chat_id],
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception:
            break

        await asyncio.sleep(5)
        current_time += 5


# Callback query handlers for control buttons

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery


@Client.on_callback_query(filters.regex("pause|resume|skip|end|close_panel"))
async def control_buttons(client: Client, callback_query: CallbackQuery):
    cmd = callback_query.data
    chat_id = callback_query.message.chat.id

    if cmd == "pause":
        await player.player_instance.pause()
        await callback_query.answer("⏸️ Paused")

    elif cmd == "resume":
        await player.player_instance.resume()
        await callback_query.answer("▶️ Resumed")

    elif cmd == "skip":
        await player.player_instance.skip()
        await callback_query.answer("⏭️ Skipped")

    elif cmd == "end":
        await player.player_instance.stop()
        await callback_query.answer("⏹️ Playback Ended")
        if chat_id in playing_messages:
            try:
                await callback_query.message.delete()
            except:
                pass
            playing_messages.pop(chat_id, None)

    elif cmd == "close_panel":
        if chat_id in playing_messages:
            try:
                await callback_query.message.delete()
            except:
                pass
            playing_messages.pop(chat_id, None)
        await callback_query.answer("❌ Closed")
