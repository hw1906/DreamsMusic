# handlers/play.py

import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from DreamsMusic.utils import maintenance_util, logger_util, yt_utils
from DreamsMusic.core import player

# Set up logging for the play handler
logger = logging.getLogger("DreamsMusic.play")

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
                # Check if assistant is None or not initialized
                if assistant is None:
                    logger.error("Assistant client is None")
                    await process_msg.edit("❌ Assistant is not initialized. Please report this to the bot owner.")
                    return
                    
                # Try getting assistant's info to check if it's connected
                logger.info(f"Checking assistant status for chat {chat_id}")
                me = await assistant.get_me()
                if not me:
                    logger.warning("Assistant get_me() returned None")
                    await process_msg.edit("❌ Assistant is starting up. Please try again in a few seconds.")
                    return
                logger.info(f"Assistant is ready: {me.first_name} ({me.id})")
            except Exception as e:
                logger.error(f"Error checking assistant status: {str(e)}")
                await process_msg.edit(
                    "❌ Assistant is not ready. Please wait a moment and try again.\n"
                    "If this persists, the bot might need to be restarted."
                )
                return
                
            try:
                # Check if assistant is a member of the group
                assistant_member = None
                try:
                    assistant_member = await assistant.get_chat_member(chat_id, (await assistant.get_me()).id)
                except Exception:
                    pass
                if not assistant_member or assistant_member.status == "left":
                    chat = await client.get_chat(chat_id)
                    if chat.username:
                        # Public group: join by username
                        logger.info(f"Assistant attempting to join public group @{chat.username}")
                        await assistant.join_chat(chat.username)
                        logger.info(f"Assistant successfully joined public group @{chat.username}")
                    else:
                        # Private group: need invite link
                        bot_member = await client.get_chat_member(chat_id, (await client.get_me()).id)
                        if bot_member.status != "administrator":
                            await process_msg.edit(
                                "❌ Bot needs to be an admin to fetch the invite link and add assistant to private group.\n"
                                "Please grant admin rights."
                            )
                            return
                        try:
                            invite_link = await client.export_chat_invite_link(chat_id)
                        except Exception as e:
                            logger.error(f"Error exporting invite link: {str(e)}")
                            await process_msg.edit(
                                "❌ Failed to fetch invite link for private group. Please make sure the bot is an admin and the group allows invite link export."
                            )
                            return
                        logger.info(f"Assistant attempting to join private group {chat_id} via invite link")
                        await assistant.join_chat(invite_link)
                        logger.info(f"Assistant successfully joined private group {chat_id}")
                else:
                    logger.info(f"Assistant already a member of chat {chat_id}")
            except Exception as e:
                logger.error(f"Error joining chat {chat_id}: {str(e)}")
                await process_msg.edit(
                    "❌ Assistant couldn't join the chat.\n"
                    "Make sure the assistant isn't banned and has proper permissions."
                )
                return
                
            try:
                # Then try joining the voice chat
                logger.info(f"Attempting to join voice chat in {chat_id}")
                from pytgcalls.types.input_stream import InputStream, AudioPiped
                from pytgcalls.types.stream import StreamType
                await pytgcalls.join_group_call(
                    chat_id,
                    InputStream(
                        AudioPiped(audio_url)
                    ),
                    join_as=assistant,
                    stream_type=StreamType().local_stream
                )
                logger.info(f"Successfully joined voice chat in {chat_id}")
            except Exception as e:
                logger.error(f"Error joining voice chat in {chat_id}: {str(e)}")
                error_msg = str(e).lower()
                if "not found" in error_msg:
                    await process_msg.edit("❌ No active voice chat found. Please start a voice chat first!")
                elif "already in" in error_msg:
                    await process_msg.edit("❌ Assistant is already in this voice chat. Try /stop first!")
                else:
                    await process_msg.edit(
                        "❌ Error joining voice chat.\n"
                        "Make sure:\n"
                        "1. A voice chat is active\n"
                        "2. The bot has permission to join\n"
                        "3. The assistant isn't already in another voice chat"
                    )
                # Try to leave the chat if voice chat join failed
                try:
                    logger.info(f"Leaving chat {chat_id} after voice chat join failure")
                    await assistant.leave_chat(chat_id)
                except Exception as cleanup_error:
                    logger.error(f"Error leaving chat after failed join: {cleanup_error}")
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
