# utils/logger_util.py

from pyrogram.types import Chat

logging_enabled = False

def is_logging_enabled():
    global logging_enabled
    return logging_enabled

async def logger_toggle(client, message):
    global logging_enabled
    text = message.text.lower()
    if text == "/logs enable":
        logging_enabled = True
        await message.reply("✅ Logs enabled.")
    elif text == "/logs disable":
        logging_enabled = False
        await message.reply("❌ Logs disabled.")

async def send_log(client, log_channel_id, chat: Chat, user, song_title, duration_sec):
    if not logging_enabled:
        return

    username = user.username if user.username else str(user.id)
    group_title = chat.title or "Private Chat"

    try:
        invite_link = await client.export_chat_invite_link(chat.id)
    except Exception:
        invite_link = None

    group_link_text = f"[{group_title}]({invite_link})" if invite_link else group_title

    minutes = duration_sec // 60
    seconds = duration_sec % 60

    text = (
        f"🎵 **Music Played**\n\n"
        f"• **Group:** {group_link_text}\n"
        f"• **User:** [{username}](tg://user?id={user.id})\n"
        f"• **Song:** `{song_title}`\n"
        f"• **Duration:** {minutes}:{seconds:02d}\n"
    )

    await client.send_message(log_channel_id, text, parse_mode="markdown")
