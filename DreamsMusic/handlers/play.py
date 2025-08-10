# handlers/play.py

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from DreamsMusic.utils import maintenance_util, logger_util, yt_utils
from DreamsMusic.core import player

# Global dictionary to track control panel message IDs by chat for updating seekbar
playing_messages = {}

MAINTENANCE_IMAGE_URL = "https://i.imgur.com/ZzqV1XY.png"
LOG_CHANNEL = -1001234567890  # Replace with your actual log channel ID

async def play(client, message: Message, lang, pytgcalls, assistant):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
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
            # Get thumbnail
            thumbnail = yt_utils.download_and_blur_thumbnail(thumbnail_url)
            
            # Try to check assistant status
            try:
                # Try getting assistant's info to check if it's connected
                me = await assistant.get_me()
                if not me:
                    await process_msg.edit("❌ Assistant is starting up. Please try again in a few seconds.")
                    return
            except Exception as e:
                await process_msg.edit(f"❌ Assistant is not ready: {str(e)}\nPlease wait a moment and try again.")
                return
                
            try:
                # Try joining the chat first
                await assistant.join_chat(chat_id)
            except Exception as e:
                await process_msg.edit(f"❌ Assistant couldn't join the chat: {str(e)}")
                return
                
            try:
                # Then try joining the voice chat
                await pytgcalls.join_group_call(
                    chat_id,
                    audio_url,
                    join_as=assistant,
                    stream_type="audio"
                )
            except Exception as e:
                await process_msg.edit(f"❌ Error joining voice chat: {str(e)}\nMake sure a voice chat is active!")
                # Try to leave the chat if voice chat join failed
                try:
                    await assistant.leave_chat(chat_id)
                except:
                    pass
                return
            
            # Send now playing message
            await process_msg.delete()
            control_message = await message.reply_photo(
                photo=thumbnail,
                caption=f"🎵 **Now Playing**\n\n"
                        f"**Title:** [{title}]({webpage_url})\n"
                        f"**Duration:** {duration // 60}:{duration % 60:02d}\n"
                        f"**Requested By:** {message.from_user.mention}",
                reply_markup=buttons
            )

            # Save message ID for seekbar updates
            playing_messages[chat_id] = control_message.message_id

            # Start background task to update seekbar
            asyncio.create_task(update_seekbar(client, chat_id, duration))

            # Send log if enabled
            await logger_util.send_log(client, LOG_CHANNEL, message.chat, message.from_user, title, duration)

        except Exception as e:
            await process_msg.edit(f"❌ Error joining voice chat: {str(e)}")
            return

    except Exception as e:
        await process_msg.edit(f"❌ Error: {str(e)}")
        return

async def update_seekbar(client, chat_id, total_duration):
    current_time = 0
    while current_time <= total_duration:
        if chat_id not in playing_messages:
            break

        progress_units = int((current_time / total_duration) * 15)
        seekbar = "🔴" + "─" * progress_units + "○" + "─" * (15 - progress_units)

        buttons = [
            [
                InlineKeyboardButton("⏸", callback_data=f"pause_{chat_id}"),
                InlineKeyboardButton("⏭️", callback_data=f"skip_{chat_id}"),
                InlineKeyboardButton("⏹️", callback_data=f"stop_{chat_id}"),
            ],
            [InlineKeyboardButton(seekbar, callback_data="seekbar")],
            [InlineKeyboardButton("❌ Close", callback_data=f"close_panel_{chat_id}")]
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

@Client.on_callback_query(filters.regex(pattern=r"^(pause|resume|stop|skip|close_panel)_(\d+)"))
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
            buttons[0][0] = InlineKeyboardButton("▶️", callback_data=f"resume_{chat_id}")
            await callback_query.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
            
        elif action == "resume":
            await pytgcalls.resume_stream(chat_id)
            await callback_query.answer("▶️ Resumed")
            # Change button back to pause
            buttons = callback_query.message.reply_markup.inline_keyboard
            buttons[0][0] = InlineKeyboardButton("⏸", callback_data=f"pause_{chat_id}")
            await callback_query.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
            
        elif action == "stop":
            await pytgcalls.leave_group_call(chat_id)
            if chat_id in playing_messages:
                try:
                    await callback_query.message.delete()
                except:
                    pass
                playing_messages.pop(chat_id, None)
            await callback_query.answer("⏹ Stopped")
            
        elif action == "skip":
            # For now just stop since we don't have queue yet
            await pytgcalls.leave_group_call(chat_id)
            if chat_id in playing_messages:
                try:
                    await callback_query.message.delete()
                except:
                    pass
                playing_messages.pop(chat_id, None)
            await callback_query.answer("⏭ Skipped")
            
        elif action == "close_panel":
            if chat_id in playing_messages:
                try:
                    await callback_query.message.delete()
                except:
                    pass
                playing_messages.pop(chat_id, None)
            await callback_query.answer("❌ Closed")
            
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)
