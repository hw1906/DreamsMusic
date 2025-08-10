# handlers/play.py

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from DreamsMusic.utils import maintenance_util, logger_util, yt_utils
from DreamsMusic.core import player

# Global dictionary to track control panel message IDs by chat for updating seekbar
playing_messages = {}

MAINTENANCE_IMAGE_URL = "https://telegra.ph/file/bc6c88ca11fd761bd7e79.jpg"

async def play(client, message: Message, lang, pytgcalls, assistant):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Check if the message is in a group
    if message.chat.type not in ["group", "supergroup"]:
        await message.reply("❌ This command only works in groups!")
        return
    
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

    # Send processing message
    process_msg = await message.reply("🔍 **Searching...**")

    try:
        # Search on YouTube
        video = yt_utils.yt_search(query)
        if not video:
            await process_msg.edit("❌ No results found!")
            return

        # Extract video information
        title = video['title']
        audio_url = video['url']
        webpage_url = video['webpage_url']
        duration = video['duration']
        thumbnail_url = video['thumbnail']

        # Create control buttons
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⏸ Pause", callback_data=f"pause_{chat_id}"),
                InlineKeyboardButton("⏹ Stop", callback_data=f"stop_{chat_id}"),
                InlineKeyboardButton("⏭ Skip", callback_data=f"skip_{chat_id}")
            ]
        ])

        # Try to join and play
        try:
            await assistant.join_chat(chat_id)
            await pytgcalls.join_group_call(
                chat_id,
                audio_url,
                join_as=assistant,
                stream_type="audio"
            )

            # Get thumbnail
            thumbnail = yt_utils.download_and_blur_thumbnail(thumbnail_url)
            
            # Send now playing message
            await process_msg.edit(
                f"🎵 **Now Playing**\n\n"
                f"**Title:** [{title}]({webpage_url})\n"
                f"**Duration:** {duration} seconds\n"
                f"**Requested By:** {message.from_user.mention}",
                reply_markup=buttons,
                disable_web_page_preview=True
            )

        except Exception as e:
            await process_msg.edit(f"❌ Error joining voice chat: {str(e)}")
            return

    except Exception as e:
        await process_msg.edit(f"❌ Error: {str(e)}")
        return

@Client.on_callback_query(filters.regex(pattern=r"^(pause|stop|skip)_(\d+)"))
async def handle_player_control(client, callback_query):
    action, chat_id = callback_query.data.split("_")
    chat_id = int(chat_id)
    user_id = callback_query.from_user.id
    
    try:
        if action == "pause":
            await pytgcalls.pause_stream(chat_id)
            await callback_query.answer("⏸ Paused")
            # Change button to resume
            buttons = callback_query.message.reply_markup.inline_keyboard
            buttons[0][0] = InlineKeyboardButton("▶️ Resume", callback_data=f"resume_{chat_id}")
            await callback_query.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
            
        elif action == "resume":
            await pytgcalls.resume_stream(chat_id)
            await callback_query.answer("▶️ Resumed")
            # Change button back to pause
            buttons = callback_query.message.reply_markup.inline_keyboard
            buttons[0][0] = InlineKeyboardButton("⏸ Pause", callback_data=f"pause_{chat_id}")
            await callback_query.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
            
        elif action == "stop":
            await pytgcalls.leave_group_call(chat_id)
            await callback_query.message.edit("⏹ Stopped playing")
            await callback_query.answer("⏹ Stopped")
            
        elif action == "skip":
            # For now just stop since we don't have queue yet
            await pytgcalls.leave_group_call(chat_id)
            await callback_query.message.edit("⏭ Skipped current song")
            await callback_query.answer("⏭ Skipped")
            
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)

MAINTENANCE_IMAGE_URL = "https://i.imgur.com/ZzqV1XY.png"  # Replace with your maintenance image URL
LOG_CHANNEL = -1001234567890  # Replace with your actual log channel ID

async def play(client, message: Message, lang, pytgcalls, assistant):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Check if the message is in a group
    if message.chat.type not in ["group", "supergroup"]:
        await message.reply("❌ This command only works in groups!")
        return
    
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

    # Send processing message
    process_msg = await message.reply("🔍 **Searching...**")

    try:
        # Search on YouTube
        video = yt_utils.yt_search(query)
        if not video:
            await process_msg.edit("❌ No results found!")
            return

        # Extract video information
        title = video['title']
        audio_url = video['url']
        webpage_url = video['webpage_url']
        duration = video['duration']
        thumbnail_url = video['thumbnail']

        # Create control buttons
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⏸ Pause", callback_data=f"pause_{chat_id}"),
                InlineKeyboardButton("⏹ Stop", callback_data=f"stop_{chat_id}"),
                InlineKeyboardButton("⏭ Skip", callback_data=f"skip_{chat_id}")
            ]
        ])

        # Try to join and play
        try:
            await assistant.join_chat(chat_id)
            await pytgcalls.join_group_call(
                chat_id,
                audio_url,
                join_as=assistant,
                stream_type="audio"
            )

            # Get thumbnail
            thumbnail = yt_utils.download_and_blur_thumbnail(thumbnail_url)
            
            # Send now playing message
            await process_msg.edit(
                f"🎵 **Now Playing**\n\n"
                f"**Title:** [{title}]({webpage_url})\n"
                f"**Duration:** {duration} seconds\n"
                f"**Requested By:** {message.from_user.mention}",
                reply_markup=buttons,
                disable_web_page_preview=True
            )

        except Exception as e:
            await process_msg.edit(f"❌ Error joining voice chat: {str(e)}")
            return

    except Exception as e:
        await process_msg.edit(f"❌ Error: {str(e)}")
        return
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
